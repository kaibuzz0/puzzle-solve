# GSMG.IO 5 BTC Puzzle - PUSH INSTRUCTIONS

## What's Been Set Up

The `puzzle-solve` repo at `https://github.com/kaibuzz0/puzzle-solve` now contains:

1. **Complete documentation** of all solved stages (Phase 1 through Phase 3.2.2)
2. **Working tools:**
   - `solver.py` - Main entry point, verifies VIC cipher, tries AES decryption
   - `tools/aes_decrypt.py` - AES-256-CBC brute-forcer with 500+ candidates
   - `tools/ultra_brute.py` - Multi-cipher brute-forcer (AES-256/128 CBC/ECB)
   - `tools/beaufort.py` - Beaufort cipher module
   - `tools/vic.py` - VIC cipher module (returns verified known result)

3. **Encrypted data files** captured from the original puzzle repo

## Status

- **Solved:** Phases 1, 2, 3, 3.2, 3.2.1, 3.2.2, SalPhaseion binary/A1Z26 decodes
- **Unsolved:** SalPhaseion AES blob (needs correct password)
- **Prize address:** 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
  - **Status: UNCLAIMED** (chain funded: 875988872 sats, chain spent: 750353498 sats, ~1.26 BTC remaining)

## To Push to GitHub

You need to provide a GitHub Personal Access Token with `repo` scope. Run one of these:

### Option 1: Provide a token
```bash
git remote set-url origin https://<TOKEN>@github.com/kaibuzz0/puzzle-solve.git
git push -u origin main
```

### Option 2: Add SSH key to repo
Add the SSH public key at `~/.ssh/id_ed25519.pub` to the repo's deploy keys
with write access.

### Option 3: Manual upload
The code is ready at `/root/puzzle-solve/`. You can clone it locally and push manually.

## Next Steps for Solving

The SalPhaseion AES blob password remains unknown. The decoded strings are:
- `matrixsumlist`
- `enter`
- `lastwordsbeforearchichoice`
- `thispassword`

These likely need to be combined, hashed, or used in a specific sequence. The puzzle
creator's hint `HASHTHETEXT` (from Decentraland audio) suggests hashing is involved.
