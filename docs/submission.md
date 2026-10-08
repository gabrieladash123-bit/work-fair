# Builder -> Intelligent Contracts

Title: WorkFair: Consensus-priced deficit admission scheduler

## Notes / Description

WorkFair is a bounded GenLayer admission scheduler with persistent tenant credits. Anyone submits commit-pinned job specifications from a fixed publisher repository. Leader and validators independently fetch full texts, check SHA-256 and classify readiness plus lookup, transformation or independent crosscheck work. Exact class agreement sets 1/2/4 policy costs; missing prerequisites and ambiguous jobs are excluded. FIFO queues share an eight-unit round budget under 1/2/1 tenant weights. Credits accumulate for expensive heads; empty queues discard credits, caps expose clipping, and start priority rotates. Admissions remove queued jobs and record conserved credit accounting. StudioNet proofs cover exclusions, weighted admission, idle credit accumulation and expensive-head FIFO completion across five rounds. The repo includes 20 direct tests and 729 queue configurations. Synthetic specifications demonstrate the mechanism, not execution or real compute cost.

## Evidence

- Repository: https://github.com/gabrieladash123-bit/work-fair
- GenLayer contract source: https://github.com/gabrieladash123-bit/work-fair/blob/main/contracts/work_fair.py
- Live receipts and states: https://github.com/gabrieladash123-bit/work-fair/blob/main/proofs/README.md

StudioNet contract: `0xb0b8f82B427f4dc296C0c58C0Ecf7311bA2804Ba`.

[Deploy transaction](https://explorer-studio.genlayer.com/tx/0x2b5ba85833e510d522ede18fbd62d4c2833d1e6b8c17080005b7ce97ec431634). All seven receipts finalized with MAJORITY_AGREE. The intake includes one dissenting vote, preserved in the proof set.
