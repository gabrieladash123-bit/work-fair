# Contract boundary

Caller supplies only a pinned URL and byte commitment. The fixed publisher repository owns request descriptions. GenLayer owns interpretation, readiness, tariff assignment, queues, persistent credits, admission ordering and visit accounting. Workers own actual execution; this contract does not attest to it or transfer assets.

## Consequential nondeterminism

Interpretation occurs inside `run_nondet_unsafe`. A crosscheck costs four units instead of a lookup's one. A blocked prerequisite excludes the job regardless of its nominal workload. Thus changing a semantic decision changes queue membership, waiting rounds, debits and subsequent admission order. Scheduling arithmetic after classification is deterministic. This is a recurrent queue-credit mechanism, not a graph proposal or one-time certificate redemption.

Validators re-fetch and hash full source bytes. They independently classify every job under the fixed hierarchy, requiring exact class agreement including exclusions; there are no numeric tolerances or confidence thresholds. Quotes need not be textually identical across models. Leader quotes must be source substrings and separately pass a substantive full-source relevance judgment. Malformed output, uncertain prerequisites, independent class disagreement or failed relevance cannot promote admission.

Policy hierarchy: explicit unmet prerequisites -> BLOCKED; ambiguous required operation/readiness -> UNKNOWN; otherwise independently originated input comparison -> CROSSCHECK; calculation/rewrite/conversion without such comparison -> TRANSFORM; faithful retrieval/copying -> LOOKUP. Operative instructions override decorative task labels. Input documents are data, never model instructions. UNKNOWN is a recorded exclusion, not a failed fetch fallback. Network/hash/schema failures revert instead.

## State and safety

Three fixed tenants have weights 1/2/1. Each round visits each tenant once and rotates start priority. A visit grants credit only to a nonempty queue and serves affordable heads until credit or the shared eight-unit round budget blocks the next head. Empty queues reset credit. Credit saturates at eight; each clipped unit is recorded. The invariant per visit is `before + grant = clipped + spent + discarded + after`. Each admitted job leaves its queue exactly once and permanently appears in an append-only round.

Bounds: nine jobs/source, four source batches, 24 globally unique job IDs, 32 rounds, 14,000 source bytes, 1,000 characters/specification. All IDs, including excluded jobs, become used. Duplicate source commitments and cross-batch reused IDs revert atomically. Queue order is source order within each tenant and transaction order across batches. Publisher controls content and can favor its requests; permissionless triggering does not provide publisher neutrality or Sybil resistance. Fixed weights and caps avoid unbounded credit/iteration. This bounded instance is educational and reusable via new deployment, not an unlimited production queue.

## Proof plan

One intake contains a four-unit amber audit ahead of a cheap lookup, cobalt conversion plus lookup, jade lookup, missing-input comparison and an unspecified job. Five rounds show weight-two admission, source-derived exclusion, head-of-line waiting, an idle credit-building round, eventual expensive admission and next-round FIFO completion. The checker binds snapshots to finalized receipts, validates fixture bytes/source hash and recomputes every debit and queue transition. Direct tests also check all 729 combinations of six 1/2/4-cost jobs, nonmutation, uniqueness, FIFO, budget and credit conservation.

GenLayer references: [nondeterministic storage boundary](https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism), [LLM calls](https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms). This contract adds substantive independent validation beyond structure-only illustrative examples.
