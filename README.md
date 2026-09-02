# GSMG.IO 5 BTC Puzzle Solver

This repository contains tools and analysis for solving the GSMG.IO 5 BTC puzzle.
The prize address is: **1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe**

## Puzzle Overview

The puzzle is a multi-stage cryptographic challenge referencing The Matrix, chess,
cryptography, and various pop culture and technical references. Each stage reveals
clues to decrypt the next using AES-256-CBC with SHA256-derived passwords.

## Project Structure

```
puzzle-solve/
├── README.md                          # This file
├── solver.py                          # Main solver script
├── known_solutions.md                 # Documented solved stages
├── remaining_puzzles.md               # Active unsolved stages
├── tools/
│   ├── beaufort.py                    # Beaufort cipher
│   ├── vic.py                         # VIC cipher
│   ├── a1z26.py                       # A1Z26 encoder/decoder
│   └── aes_decrypt.py                 # AES decryption helpers
├── data/
│   ├── phase2_encrypted.txt           # Encrypted blobs from each phase
│   ├── phase3_encrypted.txt
│   ├── phase3_2_encrypted.txt
│   └── salphaselon_encrypted.txt
└── results/                           # Decrypted outputs
```

## Solved Stages

| Stage | Solution |
|-------|----------|
| Phase 1 | `gsmg.io/theseedisplanted` |
| Phase 2 | Password: `theflowerblossomsthroughwhatseemstobeaconcretesurface` |
| Phase 3 | Password: `causalitySafenetLunaHSM11110...` |
| Phase 3.2 | Password: `jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple` |
| Phase 3.2.1 | Beaufort key: `THEMATRIXHASYOU` |
| Phase 3.2.2 | VIC cipher → `IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE` |
| SalPhaseion | `matrixsumlist`, `enter`, `lastwordsbeforearchichoice`, `thispassword` |

## Active Unsolved Stages

1. **SalPhaseion AES blob** - Encrypted data after `matrixsumlist`/`enter`
2. **SHA256 hash path** - `gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`
3. **Final private key** - Multiple layered encryptions remain

## How to Run

```bash
python3 solver.py
```

## Contributing

This is an open collaborative effort. If you discover new clues or solve additional
stages, please document them and submit updates.
