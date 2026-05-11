# NeoN Roadmap Links

## Source-of-Truth Split

This project uses a three-layer governance model:

| Layer | Role | Location |
|-------|------|----------|
| **Workbook** | Operational brain — tasks, status, roadmap | [NeoN Professional Roadmap — Control Board](https://docs.google.com/spreadsheets/d/1NTBiZnfmFfomY4usrMO_LbOwoVJyKkvvClGW0UKPWQw) |
| **Drive** | Canonical document archive — long-form specs until stable | [NeoN Drive Folder](https://drive.google.com/drive/folders/1wrFbkJAemSqedrQ1PgoyEUsecGE3IaPo) |
| **GitHub** | Executable/versioned body — specs, examples, tests, CI, release artifacts | [euphoricdoom/.Neon](https://github.com/euphoricdoom/.Neon) |

Planning and backlog belong in the workbook. Long-form canonical docs live in Drive until stable. The repo contains only what is versioned, testable, and executable.

## Workbook

[NeoN Professional Roadmap — Control Board](https://docs.google.com/spreadsheets/d/1NTBiZnfmFfomY4usrMO_LbOwoVJyKkvvClGW0UKPWQw)

Active workbook tasks related to this refactor:

- N-025: Repo Structure Refactor
- N-026: Drive Consolidation

## Drive Archive

[NeoN Drive Folder](https://drive.google.com/drive/folders/1wrFbkJAemSqedrQ1PgoyEUsecGE3IaPo)

Long-form canonical documents live here until they are stable enough to export into the repo.

## Active GitHub Issues

- [#15](https://github.com/euphoricdoom/.Neon/issues/15)
- [#16](https://github.com/euphoricdoom/.Neon/issues/16)
- [#17](https://github.com/euphoricdoom/.Neon/issues/17)

## v0.1 Release Gates

The following blockers must be resolved before v0.1 is released:

- **RIGHTS_SCHEMA_v0.1** — missing
- **DISCLOSURE_BUNDLE_FORMAT** — missing
- **Employee Automation Example** — missing

See [docs/release/v0.1_release_manifest.md](docs/release/v0.1_release_manifest.md) for full release tracking.

Before major repo/agent changes, run [docs/release/preflight_checklist.md](docs/release/preflight_checklist.md).
