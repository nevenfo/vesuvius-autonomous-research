"""Veille scientifique incrémentale, déterministe et idempotente.

Usage : python -m vesres.watch [--root <dépôt>] [--dry-run]

- Chaque source renvoie une liste d'éléments {id, title, url, date, fiabilité}. Seuls les ids jamais vus sont
  rapportés ; l'état (`watch/state.json`) garde les ids vus par source, l'heure du dernier succès et la dernière erreur.
- Une source en erreur réseau n'empêche pas les autres ; ses ids ne sont pas perdus (réessai au prochain passage).
- Verrou `watch/.lock` (anti-exécution concurrente, périmé après 2 h) ; écritures atomiques.
- Le rapport `watch/reports/YYYY-MM-DD.md` liste les nouveautés à analyser (analyse de pertinence → docs/hypotheses.md
  faite ensuite par Claude Code, pas par ce script). Aucun téléchargement de données lourdes.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

UA = {"User-Agent": "vesres-watch/0.1 (research)"}
TIMEOUT = 60
COMMUNITY_REPOS = ["DomRusso2/reader-v2", "Hob3rMallow/scrollfiesta_public", "jonmarrs/vesuvius-autoresearch",
                   "mojomast/vesuvius-autoresearch", "WillStevens/scrollreading", "schillij95/ThaumatoAnakalyptor"]


def _gh(path: str) -> object:
    """API GitHub via `gh` (authentifié) si disponible, sinon REST anonyme."""
    try:
        out = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8", timeout=TIMEOUT, check=True)
        return json.loads(out.stdout)
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        r = requests.get(f"https://api.github.com/{path.lstrip('/')}", headers=UA, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()


def src_villa_commits() -> list[dict]:
    items = []
    for c in _gh("repos/ScrollPrize/villa/commits?sha=main&per_page=100"):
        msg = c["commit"]["message"].splitlines()[0]
        items.append({"id": c["sha"], "title": msg[:160], "url": c["html_url"], "date": c["commit"]["committer"]["date"]})
    return items


def src_villa_releases() -> list[dict]:
    return [{"id": f"{r['tag_name']}@{r.get('published_at')}", "title": r.get("name") or r["tag_name"],
             "url": r["html_url"], "date": r.get("published_at")}
            for r in _gh("repos/ScrollPrize/villa/releases?per_page=30")
            if not r["tag_name"].startswith("vc3d-archive-latest")]  # builds automatiques quotidiennes : bruit


def src_villa_prs() -> list[dict]:
    return [{"id": f"pr{p['number']}", "title": p["title"][:160], "url": p["html_url"], "date": p["merged_at"]}
            for p in _gh("repos/ScrollPrize/villa/pulls?state=closed&sort=updated&direction=desc&per_page=50")
            if p.get("merged_at")]


def src_community_repos() -> list[dict]:
    items = []
    for full in COMMUNITY_REPOS:
        r = _gh(f"repos/{full}")
        items.append({"id": f"{full}@{r['pushed_at']}", "title": f"{full} mis à jour", "url": r["html_url"], "date": r["pushed_at"]})
    return items


def _hf(kind: str) -> list[dict]:
    r = requests.get(f"https://huggingface.co/api/{kind}", params={"author": "scrollprize", "limit": 500, "full": "true"},
                     headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    base = "https://huggingface.co/" + ("datasets/" if kind == "datasets" else "")
    return [{"id": f"{m['id']}@{m.get('lastModified') or m.get('sha')}", "title": m["id"], "url": base + m["id"],
             "date": m.get("lastModified")} for m in r.json()]


def src_hf_models() -> list[dict]:
    return _hf("models")


def src_hf_datasets() -> list[dict]:
    return _hf("datasets")


def src_catalog() -> list[dict]:
    """Nouveaux échantillons/segments/volumes dans le catalogue officiel (ids stables)."""
    url = "https://vesuvius-challenge-open-data.s3.us-east-1.amazonaws.com/metadata.min.json"
    r = requests.get(url, headers=UA, timeout=180)
    r.raise_for_status()
    meta = r.json()
    items = []
    for sid, s in meta["samples"].items():
        items.append({"id": f"sample:{sid}", "title": f"échantillon {sid}", "url": url, "date": None})
        for kind in ("volumes", "segments"):
            for k, v in (s.get(kind) or {}).items():
                types = sorted({d.get("type", "?") for d in v.get("data", [])})
                items.append({"id": f"{kind}:{sid}:{k}:{','.join(types)}", "title": f"{sid} {kind[:-1]} {v.get('long_id', k)} [{', '.join(types)}]",
                              "url": url, "date": None})
    return items


def src_arxiv() -> list[dict]:
    q = 'all:"Herculaneum" OR all:"Vesuvius Challenge" OR (all:"ink detection" AND all:papyrus) OR all:"virtual unwrapping"'
    r = requests.get("https://export.arxiv.org/api/query",
                     params={"search_query": q, "sortBy": "submittedDate", "sortOrder": "descending", "max_results": 50},
                     headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for e in ET.fromstring(r.text).findall("a:entry", ns):
        aid = e.findtext("a:id", default="", namespaces=ns)
        items.append({"id": aid.rsplit("/", 1)[-1].split("v")[0], "title": " ".join(e.findtext("a:title", "", ns).split()),
                      "url": aid, "date": e.findtext("a:published", default="", namespaces=ns)})
    return items


def src_substack() -> list[dict]:
    r = requests.get("https://scrollprize.substack.com/feed", headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    items = []
    for it in ET.fromstring(r.content).iter("item"):
        link = it.findtext("link", "")
        items.append({"id": link, "title": it.findtext("title", ""), "url": link, "date": it.findtext("pubDate", "")})
    return items


# fiabilité : primaire-officiel > primaire-auteur > secondaire
SOURCES = {
    "villa_releases": (src_villa_releases, "officiel"),
    "villa_merged_prs": (src_villa_prs, "officiel"),
    "villa_commits": (src_villa_commits, "officiel"),
    "catalog": (src_catalog, "officiel"),
    "hf_models": (src_hf_models, "officiel"),
    "hf_datasets": (src_hf_datasets, "officiel"),
    "substack": (src_substack, "officiel (annonces)"),
    "arxiv": (src_arxiv, "primaire (non relu par nous)"),
    "community_repos": (src_community_repos, "auteur (auto-déclaré)"),
}


def _atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def run(root: Path, dry_run: bool = False, sources: dict | None = None, today: str | None = None) -> dict:
    sources = sources or SOURCES
    wdir = root / "watch"
    wdir.mkdir(exist_ok=True)
    lock = wdir / ".lock"
    if lock.exists() and time.time() - lock.stat().st_mtime < 7200:
        raise RuntimeError(f"veille déjà en cours (verrou {lock})")
    lock.write_text(str(os.getpid()))
    try:
        state_p = wdir / "state.json"
        state = json.loads(state_p.read_text(encoding="utf-8")) if state_p.exists() else {"sources": {}}
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        today = today or time.strftime("%Y-%m-%d")
        new, errors = {}, {}
        for name, (fn, reliability) in sources.items():
            st = state["sources"].setdefault(name, {"seen": [], "last_ok": None, "last_error": None, "first_run": True})
            try:
                items = fn()
            except Exception as e:  # réseau, quota, format : isolé par source
                st["last_error"] = f"{now} {type(e).__name__}: {str(e)[:200]}"
                errors[name] = st["last_error"]
                continue
            seen = set(st["seen"])
            fresh = [dict(it, reliability=reliability) for it in items if it["id"] not in seen]
            # premier passage : on initialise la base sans tout signaler comme « nouveau »
            if not st.get("first_run"):
                if fresh:
                    new[name] = fresh
            st["seen"] = sorted(seen | {it["id"] for it in items})
            st["last_ok"], st["last_error"], st["first_run"] = now, None, False
        state["last_run"] = now
        report = _report(today, now, new, errors, state)
        if not dry_run:
            _atomic_write(wdir / "reports" / f"{today}.md", report)
            _atomic_write(state_p, json.dumps(state, indent=1, ensure_ascii=False))
        return {"new": {k: len(v) for k, v in new.items()}, "errors": errors, "report": report}
    finally:
        lock.unlink(missing_ok=True)


def _report(today: str, now: str, new: dict, errors: dict, state: dict) -> str:
    lines = [f"# Veille {today}", "", f"Passage : {now}. Nouveautés : {sum(len(v) for v in new.values())}.", ""]
    if errors:
        lines += ["## Erreurs (réessai au prochain passage)", *[f"- `{k}` : {v}" for k, v in errors.items()], ""]
    initialized = [k for k, s in state["sources"].items() if s.get("last_ok") == now and k not in new]
    for name, items in new.items():
        lines += [f"## {name} ({len(items)}, fiabilité : {items[0]['reliability']})"]
        lines += [f"- [{it['title']}]({it['url']}) — {it.get('date') or ''}" for it in items[:60]]
        if len(items) > 60:
            lines.append(f"- … {len(items) - 60} autres")
        lines.append("")
    lines += ["## À faire par l'analyse", "- Trier : pertinence pour la lecture intégrale, qualité de preuve, reproductibilité, coût.",
              "- Toute piste retenue → hypothèse `H-NNN` dans `docs/hypotheses.md` (jamais intégrée sans gain démontré).", ""]
    if initialized:
        lines += [f"Sources sans nouveauté ou initialisées : {', '.join(initialized)}.", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    res = run(Path(a.root), a.dry_run)
    print(json.dumps({"new": res["new"], "errors": res["errors"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
