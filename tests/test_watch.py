import json

import pytest

from vesres import watch


def _sources(feed):
    return {"a": (lambda: list(feed["a"]), "officiel"), "b": (lambda: (_ for _ in ()).throw(OSError("réseau")) if feed.get("fail") else list(feed["b"]), "auteur")}


def _it(i):
    return {"id": i, "title": f"t{i}", "url": f"u{i}", "date": None}


def test_idempotent_and_incremental(tmp_path):
    feed = {"a": [_it("1"), _it("2")], "b": [_it("x")]}
    r1 = watch.run(tmp_path, sources=_sources(feed), today="d1")
    assert r1["new"] == {}  # premier passage : initialisation, pas de faux « nouveau »
    r2 = watch.run(tmp_path, sources=_sources(feed), today="d2")
    assert r2["new"] == {}  # idempotent
    feed["a"].append(_it("3"))
    r3 = watch.run(tmp_path, sources=_sources(feed), today="d3")
    assert r3["new"] == {"a": 1}
    r4 = watch.run(tmp_path, sources=_sources(feed), today="d4")
    assert r4["new"] == {}  # pas de doublon
    assert (tmp_path / "watch" / "reports" / "d3.md").read_text(encoding="utf-8").count("t3") == 1


def test_source_error_isolated_and_retried(tmp_path):
    feed = {"a": [_it("1")], "b": [_it("x")]}
    watch.run(tmp_path, sources=_sources(feed), today="d1")
    feed["fail"] = True
    feed["b"].append(_it("y"))
    r = watch.run(tmp_path, sources=_sources(feed), today="d2")
    assert "b" in r["errors"] and r["new"] == {}
    feed["fail"] = False
    r = watch.run(tmp_path, sources=_sources(feed), today="d3")
    assert r["new"] == {"b": 1}  # l'élément apparu pendant la panne n'est pas perdu
    st = json.loads((tmp_path / "watch" / "state.json").read_text(encoding="utf-8"))
    assert st["sources"]["b"]["last_error"] is None


def test_lock_prevents_concurrent_run(tmp_path):
    (tmp_path / "watch").mkdir()
    (tmp_path / "watch" / ".lock").write_text("1")
    with pytest.raises(RuntimeError):
        watch.run(tmp_path, sources=_sources({"a": [], "b": []}), today="d")


def test_fail_streak_flagged_and_reset(tmp_path):
    feed = {"a": [_it("1")], "b": [_it("x")]}
    watch.run(tmp_path, sources=_sources(feed), today="d1")
    feed["fail"] = True
    watch.run(tmp_path, sources=_sources(feed), today="d2")
    r = watch.run(tmp_path, sources=_sources(feed), today="d3")
    assert "Défaillance persistante" in r["report"]
    feed["fail"] = False
    watch.run(tmp_path, sources=_sources(feed), today="d4")
    st = json.loads((tmp_path / "watch" / "state.json").read_text(encoding="utf-8"))
    assert st["sources"]["b"]["fail_streak"] == 0


def test_page_fingerprint_ignores_markup_and_scripts():
    a = "<html><script>var t=1;</script><p>Prize  rules</p></html>"
    b = "<div><script>var t=2;</script><span>Prize rules</span></div>"
    assert watch.page_fingerprint(a) == watch.page_fingerprint(b)
    assert watch.page_fingerprint(a) != watch.page_fingerprint("<p>Prize rules changed</p>")
