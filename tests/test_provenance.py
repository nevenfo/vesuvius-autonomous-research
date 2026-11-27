"""Cohérence du graphe de provenance (`docs/data/provenance.csv`, P1.1)."""
import csv
from pathlib import Path

PROV = Path(__file__).parents[1] / "docs" / "data" / "provenance.csv"
RELATIONS = {"trained_on", "initialized_from", "distilled_from", "pseudo_labeled_by", "aligned_on", "produced_by",
             "same_volume_other_resolution", "selected_with", "consulted_by"}
EVALUATED = {"reader-v2", "reader-v2-LO", "ink_9um", "hecate", "canon_2.4um", "reader-v3", "argus-v3"}
TEST_OBJECTS = {"PHerc0841", "PHerc0009B", "PHerc0500P2"}


def rows():
    with PROV.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_vocabulary_and_status():
    for r in rows():
        assert r["relation"] in RELATIONS, r
        assert r["statut"] in {"V", "A", "NV"}, r
        assert r["preuve"].strip(), r


def test_every_evaluated_model_has_training_provenance():
    trained = {r["source"] for r in rows() if r["relation"] == "trained_on"}
    assert EVALUATED <= trained, EVALUATED - trained


def test_inherited_parentage_lo_has_no_test_object():
    """reader-v2-LO et ses parents (init, distillation) : aucun objet de test vu directement."""
    rs = rows()
    parents = {"reader-v2-LO"} | {r["cible"] for r in rs if r["source"] == "reader-v2-LO"
                                  and r["relation"] in {"initialized_from"}}
    seen = {r["cible"] for r in rs if r["source"] in parents and r["relation"] == "trained_on"}
    assert not (seen & TEST_OBJECTS), seen & TEST_OBJECTS
