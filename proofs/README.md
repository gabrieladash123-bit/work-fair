# WorkFair live StudioNet proofs

Contract: `0xb0b8f82B427f4dc296C0c58C0Ecf7311bA2804Ba` on gasless **StudioNet**, chain **61999**. This is GenLayer's development chain.

[Contract source](../contracts/work_fair.py) | [CLI proof run](https://github.com/gabrieladash123-bit/work-fair/actions/runs/37734419907) | [Deployment manifest](deployment.json)

All seven transactions finalized with `MAJORITY_AGREE` and successful execution. The semantic intake received three agree votes, one disagree and one idle. Receipts preserve these votes; majority agreement is not unanimity. Five deterministic scheduling calls use the already consensus-priced jobs.

| Action | Verified state | Transaction |
|---|---|---|
| Deploy | Fixed publisher repository; empty queues and credits | [deploy](https://explorer-studio.genlayer.com/tx/0x2b5ba85833e510d522ede18fbd62d4c2833d1e6b8c17080005b7ce97ec431634) |
| Enqueue | Five queued jobs; missing prerequisites BLOCKED and unspecified work UNKNOWN | [intake](https://explorer-studio.genlayer.com/tx/0x5c6d6b1770d5fbcc7ce05fc255eff67adb5d845d09715d28c101fbbe74435dbf) |
| Round 1 | Cobalt conversion and jade copy admitted; amber accumulates one credit | [round 1](https://explorer-studio.genlayer.com/tx/0xd7bd7f7d54113337e1bba5c42e9f92a0824497650cbfeece961c1950617c13d8) |
| Round 2 | Cobalt copy admitted; amber head still waits with two credits | [round 2](https://explorer-studio.genlayer.com/tx/0x433552ef184f98166d217385dbd6774feb95ac12e840cb25291f6a09df1df848) |
| Round 3 | No admissions; amber reaches three credits without bypassing its head | [round 3](https://explorer-studio.genlayer.com/tx/0xd7f7906bd37c87bc51257db28c80aa383d42bbda434d82ce3f74699cb36a96b2) |
| Round 4 | Four-unit amber crosscheck admitted; cheap following lookup stays queued | [round 4](https://explorer-studio.genlayer.com/tx/0x61b80b235e43262719c3611fda5b67b8842b9ef7a975ffe2b9574c3bb80cd18a) |
| Round 5 | Amber lookup admitted; queues empty and credits reset | [round 5](https://explorer-studio.genlayer.com/tx/0x60dbe1a9528aef2017564d38c98fb75d258a80d7c3ce381aee78dbeb7f32225b) |

Each action has a `<label>-receipt.json`; each call has a matching `<label>.json` state snapshot. `pool-deploy` is the generic CLI deployment label, not a liquidity pool.

Source SHA-256: `0da3e6fbf5eb2be9d09f608ad2d0f2a07576360b34b1c7e128d223d95497d5b8`. The CLI checked exact deployed bytes before calls and again afterward. Fixture commit: `32b560570c4baed3f2375403b9924c9ebdfc1ff8`. Source byte commitment and classification quotes are recorded in intake state.

`node scripts/verify-proofs.cjs` binds all receipt hashes, execution outcomes, destinations, source commitments, exclusions, admissions and 15 conserved credit visits. Twenty direct tests additionally cover validator disagreement, changed fetched bytes, malformed reports, duplicate IDs, shared-budget exhaustion, capped credit and all 729 six-job tariff configurations.

Synthetic publisher requests demonstrate protocol behavior. Neither hash commitments nor consensus prove real input availability, actual work completion or measured compute costs. No token transfers, legal rights or service-delivery certificates are claimed.
