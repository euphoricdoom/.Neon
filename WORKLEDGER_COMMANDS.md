# WorkLedger Command Surface v0.1

The first WorkLedger implementation must prove the `.neon` primitive before expanding into apps, markets, or integrations.

## Required Commands

```bash
neon init
neon register
neon validate
neon derive
neon log
neon export
neon verify
neon status
```

## Command Meaning

### init
Create a local creator-owned vault.

### register
Create a new `.neon` artifact.

### validate
Check `.neon` structure.

### derive
Create a child artifact from a parent artifact.

### log
Show lineage events for an artifact.

### export
Create a portable proof packet.

### verify
Check artifact or proof packet integrity.

### status
Show vault health.

## v0.1 Rule

Every command must preserve or reveal one of:

- origin
- lineage
- proof
- portability
- creator continuity

If a command does not strengthen one of those, it does not belong in v0.1.
