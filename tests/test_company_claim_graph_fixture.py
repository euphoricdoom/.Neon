import json
from pathlib import Path
from neon.graph_integrity import validate_graph

def write_artifact(root: Path, name: str, artifact_id: str, parents: list[str]) -> None:
    (root/name).write_text(json.dumps({
        "neon_version":"0.1.0-alpha",
        "kind":"artifact",
        "artifact_id":artifact_id,
        "title":artifact_id,
        "artifact_type":"company_claim_fixture",
        "creator":{"name":"Euphoric Doom fixture"},
        "origin":{"created_at":"2026-09-22T00:00:00+00:00","statement":"bounded claim-lineage fixture"},
        "lineage":{"parents":parents,"events":[]},
        "proof":{"hash_algorithm":"sha256","anchors":[]}
    }),encoding="utf-8")

def build_serval_fixture(root: Path):
    write_artifact(root,"gmail.neon",".N/observation/serval-gmail",[])
    write_artifact(root,"prospect-claim.neon",".N/claim/serval-ack",[".N/observation/serval-gmail"])
    write_artifact(root,"brm.neon",".N/observation/serval-brm",[])
    write_artifact(root,"brm-claim.neon",".N/claim/serval-engaged",[".N/observation/serval-brm"])
    write_artifact(root,"contradiction.neon",".N/contradiction/serval-stage",[
        ".N/claim/serval-ack",".N/claim/serval-engaged"
    ])
    write_artifact(root,"flight.neon",".N/observation/serval-review",[])
    write_artifact(root,"superseding.neon",".N/claim/serval-ack-v2",[
        ".N/claim/serval-engaged",".N/observation/serval-review"
    ])

def test_company_claim_graph_is_native_neon_valid(tmp_path):
    build_serval_fixture(tmp_path)
    r=validate_graph(tmp_path)
    assert r.valid
    assert r.artifact_count==7
    assert not r.missing_parents
    assert not r.cycles

def test_company_claim_graph_missing_parent_fails_native_neon(tmp_path):
    build_serval_fixture(tmp_path)
    p=tmp_path/"superseding.neon"
    d=json.loads(p.read_text())
    d["lineage"]["parents"].append(".N/claim/missing")
    p.write_text(json.dumps(d))
    r=validate_graph(tmp_path)
    assert not r.valid
    assert any(x["missing_parent"]==".N/claim/missing" for x in r.missing_parents)

def test_company_claim_graph_cycle_fails_native_neon(tmp_path):
    build_serval_fixture(tmp_path)
    # prospect claim already points to Gmail observation; point Gmail back to
    # that claim to create an actual two-node cycle.
    p=tmp_path/"gmail.neon"
    d=json.loads(p.read_text())
    d["lineage"]["parents"]=[".N/claim/serval-ack"]
    p.write_text(json.dumps(d))
    r=validate_graph(tmp_path)
    assert not r.valid
    assert r.cycles
