# .NeoN CAS

CAS means content-addressable storage.

In .NeoN, an object can be found by the hash of its canonical bytes.

## Address Format

```text
.neon://sha256/<digest>
```

## Local Layout

```text
.neon-vault/
├── objects/
│   └── sha256/
├── artifacts/
├── exports/
├── indexes/
└── ledger.sqlite
```

## Rule

If bytes change, the address changes.

If the address is the same, the bytes are the same.

## Purpose

The artifact should survive the platform that created it.

## v0.1 Commands

```bash
neon hash artifact.neon
neon store artifact.neon
neon fetch .neon://sha256/<digest>
```
