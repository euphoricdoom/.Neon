# WorkLedger Alpha Smoke Test

```bash
python -m src.neon.cli init

python -m src.neon.cli register \
  --title "Invoice Workflow" \
  --creator "Carl Sowers"

python -m src.neon.cli derive \
  --parent .neon-vault/artifacts/invoice-workflow.neon \
  --title "AI Assisted Workflow" \
  --creator "Carl Sowers"

python -m src.neon.cli graph \
  .neon-vault/artifacts/ai-assisted-workflow.neon

python -m src.neon.cli export \
  .neon-vault/artifacts/ai-assisted-workflow.neon

python -m src.neon.cli verify \
  .neon-vault/exports/ai-assisted-workflow-proof
```

Expected outcome:

- vault initialized
- two valid `.neon` artifacts created
- derivation edge preserved
- proof packet exported
- verification succeeds
- lineage graph prints
