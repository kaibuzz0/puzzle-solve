# Remaining Unsolved Puzzles - GSMG.IO 5 BTC

## Active Mystery 1: SalPhaseion AES Blob

After decoding `matrixsumlist`, `enter`, `lastwordsbeforearchichoice`, `thispassword`,
an AES-encrypted blob remains:

```
U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSx
bRD3wNsGWVHefvdrd9zQvX0t8v3jPB4okpspxebRi6sE1BMl
5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ
```

**Possible passwords to try:**
- `matrixsumlist` (decoded binary)
- `enter` (decoded binary)
- `lastwordsbeforearchichoice` (decoded A1Z26)
- `thispassword` (decoded A1Z26)
- SHA256 of any of the above
- SHA256 of combinations (e.g., `matrixsumlistenter`)
- `shabefans too` / `sha256fans too`

**Hypothesis:** The "abba" binary sections and decoded strings may form the password
or point to a specific hashing sequence.

## Active Mystery 2: The "abba" Separator Meaning

In SalPhaseion, two "abba" sequences decode to `matrixsumlist` and `enter`.
The text says `our first hint is your last command`.

Could `matrixsumlist` + `enter` be a command to do something with a matrix sum list?
Or is `enter` the command to enter something?

## Active Mystery 3: Decentraland Audio Hint

Creator hint from Decentraland coordinates (shown in photo):
- Audio file contains hidden message
- Technique: Split stereo, invert one channel, mix to mono, spectrogram
- **Result:** `HASHTHETEXT`

This suggests we need to hash some remaining text. But which text?

## Active Mystery 4: Poem Hint

```
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.

It might have shown you only one door, beware that the rabbits nest may contain a whole lot more.

Hush hush.
```

This led to the SHA256 hash path (already found). But there may be additional layers.

## Active Mystery 5: Chess Clues Throughout

Multiple chess references:
- Phase 3: Buddhist move puzzle (chess position)
- Phase 3.2: "A fubcd-king & oracle-queen, thingky mvps, on a sad board but as wide as the first one seen."
- The first board was 14x14 (binary matrix), but "as wide as the first one seen" could hint at board dimensions
- "sad board" → "sad" = S.A.D. or could reference a specific chess variant

## Active Mystery 6: Private Key Format

The puzzle creator said there are "OVER TWENTY-THREE CIPHERS, SIXTEEN ENCRYPTIONS
AND OR SEVEN INTERTWINED PASSWORDS" protecting the private key.

The VIC cipher result says keys belong to "HALF AND BETTER HALF" - this could mean:
- Two private keys (split?)
- Reference to "better half" as a clue word
- Or the Bitcoin is split between two addresses

## Active Mystery 7: Source Code Reference

From Phase 3 decrypted text:
"THE FUNCTION OF THE YOU IS NOW TO RETURN TO THE SOURCE CODES"

This references the Bitcoin source code (main.cpp line 1616 was used earlier).
Could there be another line or file in the Bitcoin source that's relevant?

The "prime basics" reference and "REINSERTING THE PRIME BASICS" suggests we need
to work with prime numbers or the prime basics of Bitcoin (secp256k1 curve parameters?).

## Strategic Questions

1. Is the SalPhaseion AES blob password derived from `matrixsumlist` + `enter`?
2. Does `HASHTHETEXT` tell us to hash the SalPhaseion text or the VIC result?
3. What does "HALF AND BETTER HALF" tell us about key structure?
4. Is there a hidden page beyond SalPhaseion?
