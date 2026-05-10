from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

VAULT = '.neon-vault'


def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canon(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True, indent=2).encode('utf-8')


def vault() -> Path:
    return Path.cwd() / VAULT


def db() -> Path:
    return vault() / 'ledger.sqlite'


def connect():
    return sqlite3.connect(db())


def init_db(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS artifacts (artifact_id TEXT PRIMARY KEY, title TEXT, path TEXT, hash TEXT, created_at TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS edges (source_id TEXT, target_id TEXT, edge_type TEXT, created_at TEXT)')
    conn.commit()


def init_cmd(args):
    v = vault()
    for p in ['artifacts', 'exports', 'indexes']:
        (v / p).mkdir(parents=True, exist_ok=True)
    conn = connect()
    init_db(conn)
    conn.close()
    print('initialized', v)


def artifact_id(title: str):
    return '.N/' + hashlib.sha256(f'{title}|{now()}'.encode()).hexdigest()[:16]


def register_cmd(args):
    aid = artifact_id(args.title)
    data = {
        'neon_version': '0.1.0',
        'kind': 'artifact',
        'artifact_id': aid,
        'title': args.title,
        'artifact_type': args.type,
        'creator': {'name': args.creator},
        'origin': {'created_at': now(), 'statement': args.statement},
        'lineage': {'parents': [], 'events': [{'event_type': 'originated'}]},
        'proof': {'hash_algorithm': 'sha256', 'anchors': []}
    }
    out = vault() / 'artifacts' / (args.title.lower().replace(' ', '-') + '.neon')
    out.write_bytes(canon(data))
    digest = sha256(out)
    conn = connect()
    init_db(conn)
    conn.execute('INSERT INTO artifacts VALUES (?, ?, ?, ?, ?)', (aid, args.title, str(out), digest, now()))
    conn.commit()
    conn.close()
    print(aid)
    print(out)


def derive_cmd(args):
    parent = Path(args.parent)
    pdata = json.loads(parent.read_text())
    aid = artifact_id(args.title)
    data = {
        'neon_version': '0.1.0',
        'kind': 'artifact',
        'artifact_id': aid,
        'title': args.title,
        'artifact_type': args.type,
        'creator': {'name': args.creator},
        'origin': {'created_at': now(), 'statement': args.statement},
        'lineage': {
            'parents': [pdata['artifact_id']],
            'events': [{'event_type': 'derived_from', 'parent': pdata['artifact_id']}]
        },
        'proof': {'hash_algorithm': 'sha256', 'anchors': []}
    }
    out = vault() / 'artifacts' / (args.title.lower().replace(' ', '-') + '.neon')
    out.write_bytes(canon(data))
    digest = sha256(out)
    conn = connect()
    init_db(conn)
    conn.execute('INSERT INTO artifacts VALUES (?, ?, ?, ?, ?)', (aid, args.title, str(out), digest, now()))
    conn.execute('INSERT INTO edges VALUES (?, ?, ?, ?)', (pdata['artifact_id'], aid, 'derived_from', now()))
    conn.commit()
    conn.close()
    print(aid)
    print('derived from', pdata['artifact_id'])


def export_cmd(args):
    artifact = Path(args.artifact)
    data = json.loads(artifact.read_text())
    out = vault() / 'exports' / (artifact.stem + '-proof')
    out.mkdir(parents=True, exist_ok=True)
    shutil.copy2(artifact, out / artifact.name)
    manifest = {
        'artifact_id': data['artifact_id'],
        'hash': sha256(artifact),
        'exported_at': now()
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print(out)


def verify_cmd(args):
    target = Path(args.target)
    if target.is_dir():
        manifest = json.loads((target / 'manifest.json').read_text())
        artifact = target / next(p.name for p in target.glob('*.neon'))
        ok = sha256(artifact) == manifest['hash']
        print('verified' if ok else 'failed')
        return
    conn = connect()
    row = conn.execute('SELECT hash FROM artifacts WHERE path = ?', (str(target),)).fetchone()
    conn.close()
    if not row:
        print('not found')
        return
    ok = sha256(target) == row[0]
    print('verified' if ok else 'failed')


def graph_cmd(args):
    artifact = Path(args.artifact)
    data = json.loads(artifact.read_text())
    print('graph TD')
    for parent in data['lineage']['parents']:
        print(f'  {parent.replace(".N/", "N_")} --> {data["artifact_id"].replace(".N/", "N_")}')


def main():
    parser = argparse.ArgumentParser(prog='neon')
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser('init')
    p.set_defaults(func=init_cmd)

    p = sub.add_parser('register')
    p.add_argument('--title', required=True)
    p.add_argument('--creator', required=True)
    p.add_argument('--type', default='workflow')
    p.add_argument('--statement', default='')
    p.set_defaults(func=register_cmd)

    p = sub.add_parser('derive')
    p.add_argument('--parent', required=True)
    p.add_argument('--title', required=True)
    p.add_argument('--creator', required=True)
    p.add_argument('--type', default='workflow')
    p.add_argument('--statement', default='')
    p.set_defaults(func=derive_cmd)

    p = sub.add_parser('export')
    p.add_argument('artifact')
    p.set_defaults(func=export_cmd)

    p = sub.add_parser('verify')
    p.add_argument('target')
    p.set_defaults(func=verify_cmd)

    p = sub.add_parser('graph')
    p.add_argument('artifact')
    p.set_defaults(func=graph_cmd)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
