# WorkFair

A standalone GenLayer admission scheduler with consensus-derived policy costs and persistent deficit credits. It allocates admission order across three tenants; it never claims to execute work or certify service delivery.

## Mechanism

Anyone submits a commit-pinned job document from the publisher repository fixed at deployment. Leader and validators fetch complete bytes, verify SHA-256, and independently interpret every specification. Exact agreement on `LOOKUP`, `TRANSFORM`, `CROSSCHECK`, `BLOCKED` or `UNKNOWN` controls both readiness and debit. Validators additionally check source quotes against the full specification and policy. Cost classes map to fixed 1/2/4 policy units; these are not measured compute estimates.

Accepted jobs join FIFO tenant queues. `advance()` traverses all tenants, granting amber/cobalt/jade 1/2/1 units respectively. Credits persist for queued expensive jobs. A job can leave only when the tenant has credit and the round's shared eight-unit budget can pay its full cost. No later job bypasses a waiting head. Empty queues discard credits; credits cap at eight with explicit clipping records. Start priority rotates each round. Every visit records grant, debit, clipping and discarded credit.

## Repository

- `contracts/work_fair.py`: pinned standalone contract.
- `docs/architecture.md`: policy, equivalence rule, bounds and limitations.
- `records/intake.json`: synthetic publisher specifications.
- `tests/direct/`: actual GenVM direct execution, validator replay and 729 queue configurations.
- `scripts/`: genuine CLI deployment and saved-receipt verification.
- `proofs/`: deployment, receipts and state snapshots after live execution.

## Verify

```sh
pip install -r requirements.txt
genvm-lint download --version v0.2.16
genvm-lint check contracts/work_fair.py --json
pytest tests/direct -q
npm ci
node scripts/verify-proofs.cjs
```

Dispatch **StudioNet proof** for gasless development-chain deployment. The workflow creates a masked ephemeral signing account. Resumption checks exact deployed source and reuses a finalized deployment hash. Local proof checking requires downloaded live receipts.

The scheduling primitive and fixtures are purpose-built. Generic CLI, workflow and Windows test scaffolding are adapted from NettingDesk; no previous contract mechanism or transaction proof is reused. Deficit round robin is established scheduling mathematics, not a claim of a newly invented algorithm.

Synthetic specifications demonstrate consensus and scheduling. Source commitments prove byte identity, not real input availability or publisher truthfulness. `BLOCKED`/`UNKNOWN` jobs are recorded and excluded permanently; this instance has no edit/reclassification API. Use fresh job IDs for new requests.
