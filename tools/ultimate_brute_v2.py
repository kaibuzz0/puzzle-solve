#!/usr/bin/env python3
"""
THE ULTIMATE brute-force script for GSMG.IO SalPhaseion AES blobs.

This script tests every conceivable password combination including:
- All decoded string permutations with separators
- Prime/non-prime character extractions
- Chess-derived passwords (FEN, move sequences, piece names)
- VIC result transformations
- Color-count combinations (69, 96, 6, 9, 15, yin-yang variants)
- SHA256/MD5/SHA1 of all above
- MD5-based KDF (legacy OpenSSL)
- Direct-key mode (skip EVP_BytesToKey)
- Binary matrix-derived passwords
- "Zeroed out" character variations (vowel zeroing, o-zeroing, all-zeroing)
- Poem-derived phrases
- Creator hint transformations
- Chess position hash derivations
- March 2023 binary message transformations
- "First or zero" interpretations
- "Another door" coordinate combinations
- Cross-blob passwords (using one blob's data as password for the other)
- Different hex/text interpretations of passwords
"""

import base64
import hashlib
import itertools
import math
import os
import sys
from pathlib import Path

from Crypto.Cipher import AES

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SALPH_FILE = "/root/puzzle-solve/data/salphaselon_encrypted.txt"
COSMIC_FILE = "/root/puzzle-solve/data/cosmic_duality_encrypted.txt"
RESULTS_DIR = "/root/puzzle-solve/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Load blobs
# ---------------------------------------------------------------------------
def load_blob(path):
    with open(path, "r") as f:
        b64 = "".join(f.read().split())
    raw = base64.b64decode(b64)
    assert raw[:8] == b"Salted__", f"Not Salted__: {raw[:8]}"
    return raw[8:16], raw[16:]

SALPH_SALT, SALPH_CT = load_blob(SALPH_FILE)
COSMIC_SALT, COSMIC_CT = load_blob(COSMIC_FILE)

# Also keep raw blob data for cross-blob tests
SALPH_RAW = base64.b64decode(open(SALPH_FILE).read().replace("\n", "").strip())
COSMIC_RAW = base64.b64decode(open(COSMIC_FILE).read().replace("\n", "").strip())

# ---------------------------------------------------------------------------
# KDF functions
# ---------------------------------------------------------------------------
def evp_bytes_to_key(password, salt, hash_func, key_len=32, iv_len=16):
    d = b""
    d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hash_func(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]

# ---------------------------------------------------------------------------
# Decrypt with validation
# ---------------------------------------------------------------------------
def aes_decrypt(ciphertext, key, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        pad_len = plaintext[-1]
        if 1 <= pad_len <= 16 and plaintext[-pad_len:] == bytes([pad_len]) * pad_len:
            return plaintext[:-pad_len]
    except Exception:
        pass
    return None


def try_decrypt(password, salt, ct, hash_func, label=""):
    pw_bytes = password.encode("utf-8") if isinstance(password, str) else password
    key, iv = evp_bytes_to_key(pw_bytes, salt, hash_func)
    result = aes_decrypt(ct, key, iv)
    if result is None:
        return None
    if len(result) < 5:
        return None
    printable = sum(1 for b in result if 32 <= b <= 126 or b in (9, 10, 13))
    ratio = printable / len(result)
    if ratio < 0.75:
        return None
    from math import log2
    freq = {}
    for b in result:
        freq[b] = freq.get(b, 0) + 1
    entropy = -sum((v / len(result)) * log2(v / len(result)) for v in freq.values())
    if entropy > 5.5:
        return None
    return result


# ---------------------------------------------------------------------------
# Candidate generators
# ---------------------------------------------------------------------------
def prime_positions(s):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]
    return "".join(s[i - 1] for i in primes if i <= len(s))


def non_prime_positions(s):
    non_primes = [i for i in range(1, 201) if i not in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199]]
    return "".join(s[i - 1] for i in non_primes if i <= len(s))


def hash_all(s):
    return [s, hashlib.sha256(s.encode()).hexdigest(), hashlib.md5(s.encode()).hexdigest(), hashlib.sha1(s.encode().hexdigest() if isinstance(s, str) else s).hexdigest()]


# ---------------------------------------------------------------------------
# Build the MASSIVE candidate list
# ---------------------------------------------------------------------------
PARTS = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]
VIC_RESULT = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
VIC_NOSP = VIC_RESULT.replace(" ", "")

MATRIX = [
    [0,0,1,1,0,1,0,0,1,0,1,1,0,0],
    [1,1,1,1,0,0,1,1,1,0,1,0,1,1],
    [1,1,0,1,1,1,0,1,0,0,1,0,0,1],
    [0,1,1,0,1,0,0,0,0,1,1,1,0,1],
    [0,1,1,0,0,0,1,1,0,0,0,1,1,0],
    [1,0,0,1,1,0,0,0,1,0,0,0,1,1],
    [1,0,0,1,1,1,0,0,0,1,0,0,0,0],
    [1,1,1,0,0,0,0,0,0,0,1,0,0,0],
    [0,0,0,1,1,1,0,1,1,1,1,1,0,1],
    [1,1,1,1,1,1,0,0,1,1,0,0,0,1],
    [1,1,0,1,0,0,0,0,0,1,1,0,1,1],
    [1,1,1,1,0,0,1,0,1,0,1,1,0,0],
    [0,1,0,1,1,1,0,1,0,0,0,1,1,0],
    [0,1,1,0,1,1,0,1,1,0,1,0,1,1],
]
ROW_SUMS = [sum(row) for row in MATRIX]
COL_SUMS = [sum(MATRIX[r][c] for r in range(14)) for c in range(14)]
FLAT_BITS = "".join(str(c) for row in MATRIX for c in row)
FEN = "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2"


def build_candidates():
    candidates = set()

    # 1. Raw strings + all permutations with separators
    separators = ["", " ", "_", "-", ".", ",", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "+", "&", "@", "#", "!", "*"]
    for r in range(1, 5):
        for combo in itertools.permutations(PARTS, r):
            for sep in separators:
                candidates.add(sep.join(combo))

    # 2. Case variants of parts
    for s in PARTS:
        for variant in [s.lower(), s.upper(), s.title(), s.capitalize()]:
            candidates.add(variant)

    # 3. Prime and non-prime indexed characters
    for s in PARTS + ["".join(PARTS)]:
        candidates.add(prime_positions(s))
        candidates.add(non_prime_positions(s))

    # 4. Zeroed out variations
    for s in PARTS + ["".join(PARTS)]:
        candidates.add(s.replace("o", "0"))
        candidates.add(s.replace("o", "0").replace("O", "0"))
    # Vowel zeroing
    for s in PARTS + ["".join(PARTS)]:
        z = s
        for v in "aeiouAEIOU":
            z = z.replace(v, "0")
        candidates.add(z)

    # 5. Matrix-derived
    candidates.add("".join(str(x) for x in ROW_SUMS))
    candidates.add("".join(str(x) for x in COL_SUMS))
    candidates.add("".join(chr(96 + x) for x in ROW_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(64 + x) for x in ROW_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(96 + x) for x in COL_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(64 + x) for x in COL_SUMS if 1 <= x <= 26))
    candidates.add(FLAT_BITS)
    candidates.add(FLAT_BITS.replace("0", "a").replace("1", "b"))
    candidates.add(FLAT_BITS.replace("0", "n").replace("1", "y"))

    # 6. Chess-derived
    candidates.add(FEN)
    candidates.add(FEN.replace("/", ""))
    candidates.add(FEN.replace(" ", ""))
    candidates.add(FEN.replace("/", " "))
    for p in ["B5KR", "1r5B", "2R5", "2b1p1p1", "2P1k1P1", "1p2P2p", "1P2P2P", "3N1N2"]:
        candidates.add(p)
    chess_terms = ["fubcd", "fubcdking", "oraclequeen", "checkmate", "stalemate", "castling", "enpassant", "kingside", "queenside", "bishop", "knight", "rook", "queen", "king", "pawn"]
    for ct in chess_terms:
        candidates.add(ct)
        candidates.add(ct.lower())
        candidates.add(ct.upper())

    # 7. VIC transformations
    for v in [VIC_RESULT, VIC_NOSP, VIC_RESULT.lower(), VIC_RESULT.upper()]:
        candidates.add(v)
    candidates.add("halfandbetterhalf")
    candidates.add("HALFANDBETTERHALF")
    candidates.add("half")
    candidates.add("betterhalf")
    candidates.add("betterhalfandhalf")

    # 8. Yin-yang / duality / color counts
    for yy in ["69", "96", "6", "9", "15", "yingyang", "yinyang", "taijitu", "dualite", "duality", "cosmicduality", "yellow6blue9", "yellowblue69", "blue9yellow6", "6yellow9blue", "yellowblue", "blueyellow", "yingyang69", "yingyang96", "69yingyang", "96yingyang", "sixnine", "ninesix", "sixandnine", "nineandsix", "sixninesix", "ninesixnine", "sixplusnine", "nineplussix"]:
        candidates.add(yy)
        candidates.add(yy.lower())
        candidates.add(yy.upper())

    # 9. Poem phrases
    poem = "Roses are White but often Red. Yellow has a number and so does Blue. Go back to the first puzzle piece without further ado. It might have shown you only one door, beware that the rabbits nest may contain a whole lot more. Hush hush."
    candidates.add(poem)
    candidates.add(poem.lower().replace(" ", ""))
    candidates.add(poem.lower().replace(" ", "").replace(".", ""))
    candidates.add("hushhush")
    candidates.add("HUSHHUSH")
    candidates.add("HushHush")
    candidates.add("firstpuzzlepiece")
    candidates.add("thefirstpuzzlepiece")
    candidates.add("gobacktothefirstpuzzlepiece")
    candidates.add("yellowhasanumberandsodoesblue")
    candidates.add("yellowblue")
    candidates.add("whitebutoftenred")
    candidates.add("rabbitsnest")
    candidates.add("rabbithole")

    # 10. Creator hints
    creator_hints = [
        "our first hint is your last command",
        "ourfirsthintisyourlastcommand",
        "firsthint",
        "lastcommand",
        "yourlastcommand",
        "ourfirsthint",
        "shabef",
        "shabefans too",
        "sha256fans too",
        "hashthetext",
        "HASHTHETEXT",
        "thepuzzletalksforme",
        "youhavealltheinfo",
        "thehardestpartisdone",
        "onceyouhitayinyang",
        "primeandzero",
        "primeandzeroout",
        "somecharactersneedtobeezeroedout",
        "zeroout",
        "anotherdoor",
        "globallysupportingmygeneration",
        "theseedisplanted",
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "sqauresandarabbit",
        "squareandarabbit",
        "candyflipping",
        "purplepill",
        "firstorzero",
        "answeristhere",
        "only-41-17matters",
        "only41-17",
        "infrared",
        "42",
        "fortytwo",
        "happyxmasEverythingThatHasABeginningHasAnEnd",
        "regularbitcoinprivatekey",
        "bitcoinprivatekey",
    ]
    for c in creator_hints:
        candidates.add(c)
        candidates.add(c.lower())
        candidates.add(c.upper())

    # 11. Matrix / Alice / pop culture
    for ref in ["neo", "trinity", "morpheus", "oracle", "architect", "keymaker", "smith", "zion", "matrix", "thematrix", "thematrixhasyou", "wakeupneo", "knockknockneo", "followthewhiterabbit", "thereisnospoon", "redpill", "bluepill", "purplepill", "alice", "wonderland", "cheshirecat", "whiterabbit", "madhatter", "teaparty", "dormouse", "rabbithole", "entertherabbithole", "leavethematrix", "mrrobot", "elliotalderson", "fsociety"]:
        candidates.add(ref)
        candidates.add(ref.lower())
        candidates.add(ref.upper())

    # 12. Phase passwords
    phase_pws = [
        "theseedisplanted",
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "causality",
        "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
        "THEMATRIXHASYOU",
        "choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself",
    ]
    for p in phase_pws:
        candidates.add(p)
        candidates.add(p.lower())
        candidates.add(p.upper())
    candidates.add("".join(phase_pws))
    candidates.add("".join(phase_pws).lower())

    # 13. Address and challenge
    addr = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
    candidates.add(addr)
    candidates.add(addr.lower())
    candidates.add("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")
    candidates.add("GSMGIO5BTCPUZZLECHALLENGE")
    candidates.add("gsmgio5btcpuzzlechallenge")

    # 14. URL
    url = "gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"
    candidates.add(url)
    candidates.add(url.replace("/", ""))
    candidates.add("89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32")

    # 15. OP_RETURN messages
    op_msgs = [
        "hereismysecret", "theansweriswomen", "SOLUTION", "isolveditwithanabacus",
        "iamtheone", "thereisnospoon", "fromneo", "redpill", "entertherabbithole",
        "leavethematrix", "happyxmasEverythingThatHasABeginningHasAnEnd",
        "causalitytranscended", "turingcomplete", "halving", "ALPHANOISES",
        "THEMATRIXHASYOU", "fanstoo", "whatisessentialisinvisibletotheeye",
    ]
    for msg in op_msgs:
        candidates.add(msg)
        candidates.add(msg.lower())
    candidates.add("".join(op_msgs))
    candidates.add("".join(op_msgs).lower())

    # 16. "Half and better half" combos
    for sep in ["", " ", "and", "&", "+", "_", "-", ""]:
        candidates.add("half" + sep + "betterhalf")
        candidates.add("betterhalf" + sep + "half")

    # 17. Prime-related
    for p in ["prime", "primes", "primebasic", "primebasics", "primenumber", "twentythree", "twenty-three", "sixteen", "seven", "overtwentythreeciphers", "sixteenencryptions", "sevenintertwinedpasswords", "reinsertingtheprimebasics", "returntothesourcecodes", "sourcecodes", "maincpp", "line1616"]:
        candidates.add(p)
        candidates.add(p.lower())
        candidates.add(p.upper())

    # 18. Little Prince / philosophy
    for lp in ["thelittleprince", "lepetitprince", "whatisessentialisinvisibletotheeye", "itisonlywiththeheartthatoneseesrightly", "baobab", "rose", "thefox", "jacquefresco", "heisenberg", "uncertaintyprinciple", "giveitjustonesecond"]:
        candidates.add(lp)

    # 19. Numbers from hints
    for n in ["23", "16", "7", "42", "11110", "1616", "2019", "2020", "2021", "2023", "2001", "09112001", "9112001", "911", "20190420", "20200101", "20200706", "20250903", "20211231", "20210806", "964501", "949653", "209999", "1357"]:
        candidates.add(n)

    # 20. "Ciao bella o"
    for cb in ["ciao bella o", "ciaobellao", "ciao bella", "ciaobella", "bella o", "bellao", "ciao"]:
        candidates.add(cb)

    # 21. Combinations with causality
    for part in PARTS:
        candidates.add("causality" + part)
        candidates.add(part + "causality")
        candidates.add("causality" + part + "matrixsumlist")

    # 22. dbbi / faed
    candidates.add("dbbi")
    candidates.add("faed")
    candidates.add("dbbifaed")
    candidates.add("faeddbbi")
    candidates.add("dbbi faed")
    candidates.add("faed dbbi")

    # 23. "First or zero" interpretations
    for s in PARTS:
        candidates.add("0" + s[1:])  # replace first char with 0
        candidates.add(s[0] + "0" + s[2:])  # replace second char with 0
        candidates.add("0" + s)  # prepend 0
    candidates.add("0matrixsumlist")
    candidates.add("0enter")
    candidates.add("0lastwordsbeforearchichoice")
    candidates.add("0thispassword")

    # 24. Cross-blob passwords (use raw data from one blob as password for other)
    candidates.add(SALPH_RAW.hex())
    candidates.add(COSMIC_RAW.hex())
    candidates.add(SALPH_SALT.hex())
    candidates.add(COSMIC_SALT.hex())
    candidates.add(SALPH_RAW[8:].hex())  # ciphertext only
    candidates.add(COSMIC_RAW[8:].hex())

    # 25. March 2023 binary message (shifted right 1)
    binary_msg = [38, 166, 206, 150, 182, 246, 78, 14, 158, 134, 238, 134, 166, 110, 150, 230, 166, 174, 78, 46, 134, 206, 150, 14, 166, 46, 206, 46, 206, 134, 54, 158, 78, 166, 110, 46, 150, 230, 118, 150, 166, 166, 206, 46, 246, 118, 166, 78, 174, 246, 158, 46, 174, 70, 206, 166, 158, 166, 78, 174, 246, 158, 102, 246, 46, 118, 246, 78, 102, 118, 150, 206, 46, 150, 38, 78, 246, 238, 206, 206, 134, 14, 166, 22, 46, 158, 134, 238, 134, 166, 110, 150, 230, 46, 118, 246, 238, 166, 238, 230, 118, 134, 158, 118, 150, 158, 166, 198, 150, 246, 22, 198, 150, 22, 198, 78, 134, 166, 78, 246, 102, 166, 70, 206, 38, 78, 246, 238, 46, 206, 134, 54, 46, 206, 150, 54, 182, 174, 206, 30, 150, 78, 46, 134, 182, 206, 166, 182, 150, 78, 14, 166, 174, 54, 70, 238, 246, 54, 54, 166, 158]
    shifted = [b // 2 for b in binary_msg]
    candidates.add("".join(chr(b) for b in shifted if 32 <= b <= 126))
    candidates.add("".join(str(b) for b in shifted))
    candidates.add("".join(chr(96 + b) for b in shifted if 1 <= b <= 26))

    # 26. "Another door" coordinates
    candidates.add("1,4,21")
    candidates.add("1-4-21")
    candidates.add("1421")
    candidates.add("1_4_21")
    candidates.add("anotherdoor1421")
    candidates.add("anotherdoor1_4_21")

    # 27. Known puzzle hashes
    known_hashes = [
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    ]
    for h in known_hashes:
        candidates.add(h)

    # 28. "Sqaures and a rabbit" typo combos
    candidates.add("sqauresandarabbit")
    candidates.add("squareandarabbit")
    candidates.add("sqaureandarabbit")
    candidates.add("rabbitandsquare")

    # Remove empty and None
    candidates.discard("")
    candidates.discard(None)
    return sorted(candidates)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    hash_funcs = [
        ("sha256", hashlib.sha256),
        ("md5", hashlib.md5),
        ("sha1", hashlib.sha1),
    ]
    files = [
        ("SalPhaseion", SALPH_SALT, SALPH_CT),
        ("CosmicDuality", COSMIC_SALT, COSMIC_CT),
    ]

    candidates = build_candidates()
    print(f"Built {len(candidates)} base candidates.")

    # Add hash variants
    all_candidates = []
    seen = set()
    for c in candidates:
        for variant in [c, hashlib.sha256(c.encode()).hexdigest(), hashlib.md5(c.encode()).hexdigest(), hashlib.sha1(c.encode()).hexdigest()]:
            if variant and variant not in seen:
                seen.add(variant)
                all_candidates.append(variant)

    print(f"Total with hash variants: {len(all_candidates)} candidates.")
    print(f"Testing {len(files)} blobs x {len(hash_funcs)} hash funcs = up to {len(all_candidates) * len(files) * len(hash_funcs)} attempts.")
    print("=" * 60)

    found = 0
    total = 0

    for label, salt, ct in files:
        print(f"\n--- Testing {label} ---")
        for hash_name, hash_func in hash_funcs:
            print(f"  Hash: {hash_name}")
            for pwd in all_candidates:
                total += 1
                result = try_decrypt(pwd, salt, ct, hash_func)
                if result:
                    found += 1
                    text = result.decode("utf-8", errors="replace")
                    print(f"\n*** FOUND decryption #{found} ***")
                    print(f"  Blob:     {label}")
                    print(f"  Hash:     {hash_name}")
                    print(f"  Password: {pwd}")
                    print(f"  Content ({len(text)} chars):")
                    print("-" * 50)
                    print(text[:500])
                    print("-" * 50)

                    # Save
                    success_path = os.path.join(RESULTS_DIR, "success.txt")
                    with open(success_path, "a") as f:
                        f.write(f"=== SUCCESS #{found} ===\n")
                        f.write(f"Blob:     {label}\n")
                        f.write(f"Hash:     {hash_name}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{text}\n")
                        f.write("=" * 60 + "\n")

                    detail_path = os.path.join(RESULTS_DIR, f"success_{label.lower()}_{found}.txt")
                    with open(detail_path, "w") as f:
                        f.write(f"Blob:     {label}\n")
                        f.write(f"Hash:     {hash_name}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{text}\n")

            print(f"  {hash_name} complete.")

    print(f"\n{'=' * 60}")
    print(f"Done. {found} successful decryption(s) out of {total} attempts.")
    if found:
        print(f"Results saved to {RESULTS_DIR}/success.txt")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
