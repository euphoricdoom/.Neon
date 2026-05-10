from __future__ import annotations

import argparse, hashlib, json, shutil, sqlite3
from datetime import datetime, timezone
from pathlib import Path

VAULT='.neon-vault'
VERSION='0.1.0'
REQUIRED=['neon_version','kind','artifact_id','title','artifact_type','creator','origin','lineage','proof']

def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def root(): return Path.cwd()/VAULT
def db(): return root()/'ledger.sqlite'
def canon(d): return json.dumps(d, sort_keys=True, indent=2).encode()
def h(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def slug(s): return ''.join(c.lower() if c.isalnum() else '-' for c in s).strip('-') or 'artifact'
def nid(title): return '.N/'+hashlib.sha256(f'{title}|{now()}'.encode()).hexdigest()[:16]
def read(p): return json.loads(Path(p).read_text())

def conn():
    if not db().exists(): raise SystemExit('No vault. Run: neon init')
    c=sqlite3.connect(db()); init_db(c); return c

def init_db(c):
    c.execute('CREATE TABLE IF NOT EXISTS artifacts (artifact_id TEXT PRIMARY KEY,title TEXT,path TEXT,hash TEXT,created_at TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS edges (source_id TEXT,target_id TEXT,edge_type TEXT,created_at TEXT)')
    c.commit()

def validate_data(d):
    e=[]
    for k in REQUIRED:
        if k not in d: e.append('missing '+k)
    if d.get('kind')!='artifact': e.append('kind must be artifact')
    if not str(d.get('artifact_id','')).startswith('.N/'): e.append('artifact_id must start .N/')
    if not isinstance(d.get('lineage',{}).get('parents',[]),list): e.append('lineage.parents must be list')
    return e

def make(title, creator, typ, statement, parents=None):
    aid=nid(title); parents=parents or []
    ev='derived_from' if parents else 'originated'
    return {'neon_version':VERSION,'kind':'artifact','artifact_id':aid,'title':title,'artifact_type':typ,'creator':{'name':creator},'origin':{'created_at':now(),'statement':statement},'lineage':{'parents':parents,'events':[{'event_type':ev,'created_at':now()}]},'proof':{'hash_algorithm':'sha256','anchors':[]}}

def save_artifact(d):
    out=root()/'artifacts'/(slug(d['title'])+'.neon')
    out.write_bytes(canon(d)); digest=h(out)
    c=conn(); c.execute('INSERT OR REPLACE INTO artifacts VALUES (?,?,?,?,?)',(d['artifact_id'],d['title'],str(out),digest,now())); c.commit(); c.close()
    return out,digest

def init(args):
    for p in ['artifacts','exports','indexes','proofs']:(root()/p).mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(db()); init_db(c); c.close(); print(root())

def register(args):
    d=make(args.title,args.creator,args.type,args.statement); out,digest=save_artifact(d); print(d['artifact_id']); print(out); print(digest)

def derive(args):
    p=read(args.parent); d=make(args.title,args.creator,args.type,args.statement,[p['artifact_id']]); out,digest=save_artifact(d)
    c=conn(); c.execute('INSERT INTO edges VALUES (?,?,?,?)',(p['artifact_id'],d['artifact_id'],'derived_from',now())); c.commit(); c.close()
    print(d['artifact_id']); print('parent',p['artifact_id']); print(out)

def validate(args):
    d=read(args.artifact); e=validate_data(d)
    if e:
        print('INVALID'); [print('-',x) for x in e]; raise SystemExit(1)
    print('VALID'); print(d['artifact_id']); print(h(Path(args.artifact)))

def status(args):
    c=conn(); a=c.execute('SELECT COUNT(*) FROM artifacts').fetchone()[0]; e=c.execute('SELECT COUNT(*) FROM edges').fetchone()[0]; c.close(); print('vault',root()); print('artifacts',a); print('edges',e)

def list_cmd(args):
    c=conn(); rows=c.execute('SELECT title,artifact_id,path FROM artifacts ORDER BY created_at').fetchall(); c.close()
    for title,aid,path in rows: print(f'{aid} | {title} | {path}')

def log(args):
    d=read(args.artifact); print(d['title']); print(d['artifact_id']); print('parents', ', '.join(d['lineage']['parents']) or 'none')
    for ev in d['lineage']['events']: print('-',ev.get('event_type'),ev.get('created_at',''))

def graph(args):
    d=read(args.artifact); print('graph TD')
    if not d['lineage']['parents']: print('  '+d['artifact_id'].replace('.N/','N_'))
    for p in d['lineage']['parents']: print(f'  {p.replace(".N/","N_")} --> {d["artifact_id"].replace(".N/","N_")}')

def export(args):
    art=Path(args.artifact); d=read(art); out=root()/'exports'/(art.stem+'-proof'); out.mkdir(parents=True,exist_ok=True)
    shutil.copy2(art,out/art.name); digest=h(art)
    manifest={'neon_version':VERSION,'kind':'proof_packet','artifact_id':d['artifact_id'],'artifact_file':art.name,'artifact_sha256':digest,'exported_at':now(),'parents':d['lineage']['parents']}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)); (out/'hashes.txt').write_text(f'{digest}  {art.name}\n')
    (out/'SUMMARY.md').write_text(f'# .NeoN Proof Packet\n\nArtifact: {d["title"]}\n\nID: {d["artifact_id"]}\n\nSHA-256: {digest}\n')
    print(out)

def verify(args):
    t=Path(args.target)
    if t.is_dir():
        m=json.loads((t/'manifest.json').read_text()); art=t/m['artifact_file']; ok=h(art)==m['artifact_sha256']; print('verified' if ok else 'failed'); raise SystemExit(0 if ok else 1)
    d=read(t); e=validate_data(d); print('verified' if not e else 'failed'); raise SystemExit(0 if not e else 1)

def main():
    p=argparse.ArgumentParser(prog='neon-v2'); s=p.add_subparsers(required=True)
    for name,fn in [('init',init),('status',status),('list',list_cmd)]: q=s.add_parser(name); q.set_defaults(func=fn)
    q=s.add_parser('register'); q.add_argument('--title',required=True); q.add_argument('--creator',required=True); q.add_argument('--type',default='workflow'); q.add_argument('--statement',default=''); q.set_defaults(func=register)
    q=s.add_parser('derive'); q.add_argument('--parent',required=True); q.add_argument('--title',required=True); q.add_argument('--creator',required=True); q.add_argument('--type',default='workflow'); q.add_argument('--statement',default=''); q.set_defaults(func=derive)
    for name,fn in [('validate',validate),('log',log),('graph',graph),('export',export),('verify',verify)]: q=s.add_parser(name); q.add_argument('artifact' if name!='verify' else 'target'); q.set_defaults(func=fn)
    a=p.parse_args(); a.func(a)

if __name__=='__main__': main()
