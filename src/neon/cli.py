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
    for p in ['artifacts', 'exports', 'indexes', 'objects/sha256']:
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
    if not artifact.exists():
        print("not found")
        return
    data = json.loads(artifact.read_text())
    digest = sha256(artifact)
    out = vault() / 'exports' / (artifact.stem + '-proof')
    out.mkdir(parents=True, exist_ok=True)

    shutil.copy2(artifact, out / artifact.name)

    manifest = {
        'artifact_id': data['artifact_id'],
        'hash': digest,
        'exported_at': now()
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))

    (out / 'hashes.txt').write_text(digest + "  " + artifact.name + "\\n")

    summary = "# .NeoN Proof Packet\\n\\nArtifact: " + data['title'] + "\\nID: " + data['artifact_id'] + "\\nHash: " + digest + "\\nExported: " + now() + "\\n"
    (out / 'SUMMARY.md').write_text(summary)

    (out / 'lineage.json').write_text(json.dumps(data.get('lineage', {}), indent=2))

    verification = {
        "status": "unverified",
        "hash_algorithm": "sha256",
        "expected_hash": digest
    }
    (out / 'verification.json').write_text(json.dumps(verification, indent=2))

    print(out)

def verify_cmd(args):
    target = Path(args.target)
    if target.is_dir():
        manifest_path = target / 'manifest.json'
        if not manifest_path.exists():
            print("invalid proof packet")
            return
        manifest = json.loads(manifest_path.read_text())
        artifact = target / next(p.name for p in target.glob('*.neon'))
        digest = sha256(artifact)
        ok = digest == manifest['hash']

        verification_path = target / 'verification.json'
        if verification_path.exists():
            verification = json.loads(verification_path.read_text())
            verification['status'] = "verified" if ok else "failed"
            verification['actual_hash'] = digest
            verification['verified_at'] = now()
            verification_path.write_text(json.dumps(verification, indent=2))

        print('verified' if ok else 'failed')
        return

    # Verify a single file against the DB
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

def validate_artifact(data: dict) -> list[str]:
    errors = []
    if data.get('kind') != 'artifact':
        errors.append("kind must be 'artifact'")
    if not data.get('artifact_id', '').startswith('.N/'):
        errors.append("artifact_id must start with '.N/'")
    if not isinstance(data.get('creator'), dict):
        errors.append("creator must be an object")
    if not isinstance(data.get('origin'), dict):
        errors.append("origin must be an object")

    lineage = data.get('lineage', {})
    if not isinstance(lineage.get('parents'), list):
        errors.append("lineage.parents must be a list")
    if not isinstance(lineage.get('events'), list):
        errors.append("lineage.events must be a list")

    proof = data.get('proof', {})
    if not isinstance(proof, dict):
        errors.append("proof must be an object")
    elif proof.get('hash_algorithm') != 'sha256':
        errors.append("proof.hash_algorithm must be 'sha256'")

    return errors

def validate_cmd(args):
    path = Path(args.path)
    if not path.exists():
        print("not found")
        return
    data = json.loads(path.read_text())
    errors = validate_artifact(data)
    if errors:
        for err in errors:
            print(f"Error: {err}")
        import sys
        sys.exit(1)
    print("valid")

def hash_cmd(args):
    path = Path(args.path)
    if not path.exists():
        print("not found")
        return
    print(sha256(path))

def store_cmd(args):
    path = Path(args.path)
    if not path.exists():
        print("not found")
        return
    digest = sha256(path)
    dest = vault() / 'objects' / 'sha256' / digest
    if not dest.exists():
        dest.write_bytes(path.read_bytes())
    print(f".neon://sha256/{digest}")

def fetch_cmd(args):
    uri = args.uri
    if not uri.startswith('.neon://sha256/'):
        print("invalid uri")
        return
    digest = uri.split('/')[-1]
    src = vault() / 'objects' / 'sha256' / digest
    if not src.exists():
        print("not found")
        return

    if args.out:
        Path(args.out).write_bytes(src.read_bytes())
        print(f"fetched to {args.out}")
    else:
        print(src.read_text())

def log_cmd(args):
    conn = connect()
    rows = conn.execute('SELECT artifact_id, title, created_at FROM artifacts ORDER BY created_at DESC').fetchall()
    conn.close()
    for r in rows:
        print(f"{r[2]}  {r[0]}  {r[1]}")

def list_cmd(args):
    artifacts_dir = vault() / 'artifacts'
    if not artifacts_dir.exists():
        return
    for p in artifacts_dir.glob('*.neon'):
        print(p.name)

def status_cmd(args):
    v = vault()
    print(f"Vault: {v}")

    artifacts = list((v / 'artifacts').glob('*.neon')) if (v / 'artifacts').exists() else []
    print(f"Artifacts: {len(artifacts)}")

    objects = list((v / 'objects' / 'sha256').glob('*')) if (v / 'objects' / 'sha256').exists() else []
    print(f"Objects: {len(objects)}")

    conn = connect()
    edges = conn.execute('SELECT COUNT(*) FROM edges').fetchone()[0]
    conn.close()
    print(f"Edges: {edges}")

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

    p = sub.add_parser('validate')
    p.add_argument('path')
    p.set_defaults(func=validate_cmd)

    p = sub.add_parser('hash')
    p.add_argument('path')
    p.set_defaults(func=hash_cmd)

    p = sub.add_parser('store')
    p.add_argument('path')
    p.set_defaults(func=store_cmd)

    p = sub.add_parser('fetch')
    p.add_argument('uri')
    p.add_argument('--out')
    p.set_defaults(func=fetch_cmd)

    p = sub.add_parser('log')
    p.set_defaults(func=log_cmd)

    p = sub.add_parser('list')
    p.set_defaults(func=list_cmd)

    p = sub.add_parser('status')
    p.set_defaults(func=status_cmd)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
