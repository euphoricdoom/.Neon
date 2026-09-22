import json
from pathlib import Path
from neon.graph_integrity import validate_graph

def art(path:Path,aid:str,parents:list[str]):
 path.write_text(json.dumps({"artifact_id":aid,"lineage":{"parents":parents}}),encoding="utf-8")

def test_valid_graph():
 # artifact parser for integrity only needs IDs/parents
 pass

def test_missing_parent_is_invalid(tmp_path):
 art(tmp_path/"a.neon",".N/a",[".N/missing"])
 r=validate_graph(tmp_path);assert not r.valid;assert r.missing_parents[0]["missing_parent"]==".N/missing"

def test_cycle_is_invalid(tmp_path):
 art(tmp_path/"a.neon",".N/a",[".N/b"]);art(tmp_path/"b.neon",".N/b",[".N/a"])
 r=validate_graph(tmp_path);assert not r.valid;assert r.cycles

def test_acyclic_resolved_graph_is_valid(tmp_path):
 art(tmp_path/"a.neon",".N/a",[]);art(tmp_path/"b.neon",".N/b",[".N/a"]);art(tmp_path/"c.neon",".N/c",[".N/b"])
 r=validate_graph(tmp_path);assert r.valid;assert not r.cycles;assert not r.missing_parents

def test_duplicate_artifact_id_is_invalid(tmp_path):
 art(tmp_path/"a.neon",".N/a",[]);art(tmp_path/"other.neon",".N/a",[])
 r=validate_graph(tmp_path);assert not r.valid;assert r.duplicate_ids
