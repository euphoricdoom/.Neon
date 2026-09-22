"""Integrity validation for .NeoN lineage graphs.

Traversal remains tolerant for inspection. This module answers the stricter
question: is the indexed lineage graph structurally valid?
"""
from __future__ import annotations
from dataclasses import asdict,dataclass,field
from pathlib import Path
from typing import Any
from neon.topology import index_neon_files,read_neon

@dataclass
class GraphIntegrity:
 valid: bool
 artifact_count: int
 missing_parents: list[dict[str,str]]=field(default_factory=list)
 cycles: list[list[str]]=field(default_factory=list)
 duplicate_ids: list[dict[str,Any]]=field(default_factory=list)
 def to_dict(self):return asdict(self)

def validate_graph(root:Path)->GraphIntegrity:
 paths=list(root.rglob("*.neon"));by_id:dict[str,list[Path]]={}
 for p in paths:
  try:d=read_neon(p)
  except SystemExit:continue
  aid=d.get("artifact_id")
  if isinstance(aid,str):by_id.setdefault(aid,[]).append(p)
 duplicates=[{"artifact_id":aid,"paths":[str(p) for p in ps]} for aid,ps in sorted(by_id.items()) if len(ps)>1]
 index=index_neon_files(root);parents={}
 missing=[]
 for aid,p in index.items():
  d=read_neon(p);ps=list(d.get("lineage",{}).get("parents",[]));parents[aid]=ps
  for parent in ps:
   if parent not in index:missing.append({"artifact_id":aid,"missing_parent":parent})
 cycles=[];state={};stack=[]
 def visit(aid):
  state[aid]=1;stack.append(aid)
  for parent in parents.get(aid,[]):
   if parent not in parents:continue
   if state.get(parent,0)==0:visit(parent)
   elif state.get(parent)==1:
    i=stack.index(parent);cycle=stack[i:]+[parent]
    if cycle not in cycles:cycles.append(cycle)
  stack.pop();state[aid]=2
 for aid in sorted(parents):
  if state.get(aid,0)==0:visit(aid)
 return GraphIntegrity(valid=not(missing or cycles or duplicates),artifact_count=len(index),
  missing_parents=missing,cycles=cycles,duplicate_ids=duplicates)
