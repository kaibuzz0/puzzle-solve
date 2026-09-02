# Known Solutions - GSMG.IO 5 BTC Puzzle

## Phase 1: The Binary Spiral
- **URL:** https://gsmg.io/puzzle
- **Method:** 14x14 binary matrix, read counterclockwise spiral from upper-left
- **Result:** `gsmg.io/theseedisplanted`

## Phase 2: The Warning
- **URL:** https://gsmg.io/theseedisplanted
- **Method:** Hidden POST form with password `theflowerblossomsthroughwhatseemstobeaconcretesurface`
- **Reference:** Logic - "The Warning" (war + ning, LO + gic)

## Phase 3: Causality
- **URL:** https://gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself
- **Password:** SHA256 of concatenated 7 parts
  1. `causality`
  2. `Safenet`
  3. `Luna`
  4. `HSM`
  5. `11110`
  6. `0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854`
  7. `B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1`
- **SHA256 Password:** `1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5`
- **Decrypted hint:** References to Jacque Fresco, Alice in Wonderland, Heisenberg uncertainty principle

## Phase 3.2: The Architect's Riddle
- **Password:** SHA256(`jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple`)
  = `250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c`
- **First clue:** "... am I here? Wake up, you..." → Matrix reference ("Why am I here? Wake up, Neo.")
- **Second clue:** "One for one, four for one" → IBM EBCDIC 1141 encoding
- **Third clue:** "beautiful strategic position" → Beaufort cipher

### Phase 3.2.1: Beaufort Cipher
- **Ciphertext:** Box-drawing character blob (╬╚,╬°%...)
- **Encoding:** IBM EBCDIC 1141
- **Key:** `THEMATRIXHASYOU`
- **Result:** Long text from The Architect (Matrix Reloaded), ending with "CIAO BELLA O"
- **Key hint in text:** "THE FUNCTION OF THE YOU IS NOW TO RETURN TO THE SOURCE CODES"
- **Key hint:** "OVER TWENTY-THREE CIPHERS, SIXTEEN ENCRYPTIONS AND OR SEVEN INTERTWINED PASSWORDS"

### Phase 3.2.2: VIC Cipher
- **Ciphertext:** `15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112`
- **Alphabet:** `FUBCDORA.LETHINGKYMVPSJQZXW`
- **Digits:** 1 and 4
- **Result:** `IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE`

## SalPhaseion (Cosmic Duality)
- **Entry:** SHA256(`GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`)
  = `89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32`
- **URL:** https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32

### SalPhaseion Decoded Elements:
1. **Binary section (a=0, b=1):** `matrixsumlist`
2. **Binary section (a=0, b=1):** `enter`
3. **A1Z26 with o=0 substitution:** `lastwordsbeforearchichoice`
4. **A1Z26 with o=0 substitution:** `thispassword`
5. **AES blob:** Remains encrypted (needs password)
6. **Text:** `shabefans too` (shabef = sha256 reference)
7. **English hint:** `our first hint is your last command`

### Key Mappings Discovered:
- `shabef` → `sha256` (s=s, h=h, a=2, b=2, e=5, f=6)
- `a=1, b=2, ..., i=9, o=0` for numeric sections
