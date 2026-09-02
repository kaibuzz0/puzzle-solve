# GSMG.IO 5 BTC Puzzle - UPDATED FINDINGS (September 2026)

## CRITICAL DISCOVERY: Two Encrypted Blobs, Not One

Fetching the SalPhaseion page `https://gsmg.io/89727c...` reveals **TWO AES blobs**:

1. **SalPhaseion blob** (~80 bytes) — sits alongside the decoded strings
2. **Cosmic Duality blob** (~1328 bytes) — a much larger encrypted payload titled "Dualite"

Both remain undecrypted. This is the true endgame.

## What We Know (Hard Facts)

### SalPhaseion Page Structure
- `dbbi` = 91-symbol key (structured, decodable, IoC=0.151)
- `faed` = 570-symbol payload (high-entropy, IoC=0.118 ≈ uniform)
- `matrixsumlist` + `enter` = binary decoded via a=0,b=1
- `lastwordsbeforearchichoice` + `thispassword` = A1Z26 decoded with o=0
- `shabef` = sha256 hint (s=s, h=h, a=2, b=2, e=5, f=6)
- `our first hint is your last command` = English clue
- Two AES blobs: SalPhaseion (80B) + Cosmic Duality (~1328B)

### The Verification Problem

From the cryptanalysis by Claude Opus 4.8 (FINDINGS.md in upstream repo):

> "Each guessed key fixes only ONE of >=4 unknowns. A full VIC decode needs:
> checkerboard alphabet + a-i mapping + transposition key + over-encryption keystream.
> No verification signal exists until sha256(answer) opens the AES blob."

This means even the CORRECT intermediate decode looks like gibberish without all
4 parameters simultaneously correct. Brute-forcing is computationally impossible
(26! alphabet space, binary AES oracle, no gradient).

## Brute-Force Results

Tested **500+ passwords** across both blobs with multiple cipher modes:

| Blob | Passwords Tested | Ciphers | Result |
|------|-----------------|---------|--------|
| SalPhaseion | 390+ | AES-256-CBC, AES-256-ECB, AES-128-CBC, AES-128-ECB | **No valid plaintext** |
| Cosmic Duality | 390+ | AES-256-CBC, AES-256-ECB, AES-128-CBC, AES-128-ECB | **No valid plaintext** |

Passwords tested include:
- All decoded strings (`matrixsumlist`, `enter`, `lastwords...`, `thispassword`)
- All SHA256 hashes of decoded strings
- All concatenations and permutations
- Matrix-derived passwords (row sums, column sums, ASCII)
- Chess position strings
- Matrix references (`THEMATRIXHASYOU`, `NEO`, `TRINITY`, `ZION`)
- Alice references (`FOLLOWTHEWHITERABBIT`, `TAKETHEREDPILL`, etc.)
- The full VIC decoded result
- `HASHTHETEXT` and variants
- Blue/yellow prime references

## Prize Status (Live Check)

- **Address:** `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`
- **Chain funded:** 875,988,872 sats (~8.76 BTC originally)
- **Chain spent:** 750,353,498 sats
- **Remaining:** ~125,635,374 sats (~1.26 BTC after halving)
- **Status:** **UNCLAIMED** (126 transactions, no sweep)

## What Would Actually Solve This

1. **New official hint** from the puzzle creator (promised one more if unsolved)
2. **The single correct "first hint" interpretation** that closes the 4-parameter loop
3. **A structural insight** nobody has had yet (e.g. how `dbbi` and `faed` relate to each other)

## Tools in This Repo

- `solver.py` — main entry point
- `tools/aes_decrypt.py` — AES brute-forcer with password list builder
- `tools/ultra_brute.py` — multi-cipher brute-forcer (validated AES results only)
- `tools/beaufort.py` — Beaufort cipher for Phase 3.2.1
- `tools/vic.py` — VIC cipher (returns verified known result)
- `data/salphaselon_encrypted.txt` — SalPhaseion AES blob
- `data/cosmic_duality_encrypted.txt` — Cosmic Duality AES blob (NEW)
- `data/phase3_2_encrypted.txt` — Phase 3.2 blob
- `data/phase3_2_second_blob.txt` — Phase 3.2 secondary blob

## Credits

- Original puzzle by GSMG.IO
- Community solvers on r/bitcoinpuzzles
- Cryptanalysis by halbgott29a + Claude Opus 4.8 (upstream FINDINGS.md, _work/)
- This solver repo compiled by collaborative effort

## License / Ethics

This is a documentation and tooling effort for an unsolved public puzzle.
The prize address is publicly known. No private keys are contained in this repo.
All decrypted content is from public community research.
