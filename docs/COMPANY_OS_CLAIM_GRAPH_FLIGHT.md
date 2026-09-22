# Company OS claim-graph native Flight

This fixture exercises the exact structural pattern discovered in Connection Forge using the native .NeoN graph-integrity runtime:

observation -> scoped claim
observation -> conflicting scoped claim
both claims -> contradiction
old claim + reviewed observation -> superseding claim

Expected:
- valid graph passes;
- missing parent fails;
- cycle fails.

This is provenance-structure proof only. .NeoN does not choose the winning claim, determine freshness, or authorize execution.
