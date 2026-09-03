#!/usr/bin/env python3
"""
ULTIMATE brute-force script for GSMG.IO SalPhaseion and Cosmic Duality AES blobs.

Tests:
1. ALL combinations of decoded SalPhaseion strings with separators + hash variants
2. Prime-indexed characters from decoded strings
3. Chess-derived passwords (FEN, move sequences)
4. VIC result transformations
5. Color-count combinations (69, 96, 6, 9, 15)
6. SHA256/MD5/SHA1 of all above
7. MD5-based KDF (legacy OpenSSL)
8. Direct-key mode (skip EVP_BytesToKey)
9. Binary matrix-derived passwords
10. "Zeroed out" character variations
11. Poem-derived phrases
12. Creator hint transformations
13. Chess position hash derivations

Save successful results to /root/puzzle-solve/results/success.txt
"""

import base64
import hashlib
import itertools
import math
import os
import struct
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

# ---------------------------------------------------------------------------
# KDF functions
# ---------------------------------------------------------------------------
def evp_bytes_to_key_sha256(password, salt, key_len=32, iv_len=16):
    """OpenSSL EVP_BytesToKey with SHA256."""
    d = b""
    d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hashlib.sha256(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def evp_bytes_to_key_md5(password, salt, key_len=32, iv_len=16):
    """Legacy OpenSSL EVP_BytesToKey with MD5."""
    d = b""
    d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hashlib.md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


def evp_bytes_to_key_sha1(password, salt, key_len=32, iv_len=16):
    """EVP_BytesToKey with SHA1."""
    d = b""
    d_i = b""
    while len(d) < key_len + iv_len:
        d_i = hashlib.sha1(d_i + password + salt).digest()
        d += d_i
    return d[:key_len], d[key_len:key_len + iv_len]


# ---------------------------------------------------------------------------
# Decrypt functions
# ---------------------------------------------------------------------------
def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    pad_len = plaintext[-1]
    if 1 <= pad_len <= 16 and plaintext[-pad_len:] == bytes([pad_len]) * pad_len:
        return plaintext[:-pad_len]
    return None


def try_decrypt(password, salt, ct, kdf="sha256", label=""):
    """Try a password with given KDF. Returns decrypted bytes or None."""
    pw_bytes = password.encode("utf-8") if isinstance(password, str) else password
    if kdf == "sha256":
        key, iv = evp_bytes_to_key_sha256(pw_bytes, salt)
    elif kdf == "md5":
        key, iv = evp_bytes_to_key_md5(pw_bytes, salt)
    elif kdf == "sha1":
        key, iv = evp_bytes_to_key_sha1(pw_bytes, salt)
    elif kdf == "direct":
        # Skip KDF; use password directly as key+iv
        key = pw_bytes[:32].ljust(32, b"\x00")
        iv = pw_bytes[32:48].ljust(16, b"\x00")
    elif kdf == "direct-sha256":
        h = hashlib.sha256(pw_bytes).digest()
        key = h[:32]
        iv = h[16:32] if len(h) >= 32 else h.ljust(32, b"\x00")
    elif kdf == "direct-md5":
        h = hashlib.md5(pw_bytes).digest()
        key = h.ljust(32, b"\x00")[:32]
        iv = h.ljust(16, b"\x00")[:16]
    else:
        return None

    result = aes_decrypt(ct, key, iv)
    if result is None:
        return None

    # Validate: mostly printable ASCII, reasonable entropy
    if len(result) < 5:
        return None
    printable = sum(1 for b in result if 32 <= b <= 126 or b in (9, 10, 13))
    ratio = printable / len(result)
    if ratio < 0.75:
        return None

    # Entropy check
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
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    return "".join(s[i - 1] for i in primes if i <= len(s))


def non_prime_positions(s):
    non_primes = [1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]
    return "".join(s[i - 1] for i in non_primes if i <= len(s))


def zero_out(s, chars="o"):
    return s.replace(chars, "0")


def zero_out_all_vowels(s):
    for v in "aeiouAEIOU":
        s = s.replace(v, "0")
    return s


def sha256_str(s):
    return hashlib.sha256(s.encode()).hexdigest()


def md5_str(s):
    return hashlib.md5(s.encode()).hexdigest()


def sha1_str(s):
    return hashlib.sha1(s.encode()).hexdigest()


def add_hashes(candidates, source):
    """Add SHA256, MD5, SHA1 of each candidate."""
    result = []
    for c in candidates:
        result.append(c)
        result.append(sha256_str(c))
        result.append(md5_str(c))
        result.append(sha1_str(c))
    return result


# ---------------------------------------------------------------------------
# Core strings
# ---------------------------------------------------------------------------
PARTS = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]
VIC_RESULT = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
VIC_NOSP = VIC_RESULT.replace(" ", "")
VIC_LOWER = VIC_RESULT.lower()
VIC_UPPER = VIC_RESULT.upper()

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

# Chess FEN
FEN = "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2"

# ---------------------------------------------------------------------------
# Build candidate list
# ---------------------------------------------------------------------------
def build_candidates():
    candidates = set()

    # 1. Raw decoded strings + case variants
    for s in PARTS:
        candidates.add(s)
        candidates.add(s.lower())
        candidates.add(s.upper())
        candidates.add(s.title())

    # 2. ALL permutations with ALL separators
    separators = ["", " ", "_", "-", ".", ",", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "+"]
    for r in range(1, 5):
        for combo in itertools.permutations(PARTS, r):
            for sep in separators:
                candidates.add(sep.join(combo))

    # 3. Prime-indexed characters
    for s in PARTS:
        candidates.add(prime_positions(s))
        candidates.add(prime_positions(s).lower())
        candidates.add(non_prime_positions(s))

    # 4. Zeroed out variations
    for s in PARTS:
        candidates.add(zero_out(s, "o"))
        candidates.add(zero_out_all_vowels(s))
    candidates.add(zero_out("".join(PARTS), "o"))
    candidates.add(zero_out_all_vowels("".join(PARTS)))

    # 5. Matrix-derived passwords
    candidates.add("".join(str(x) for x in ROW_SUMS))
    candidates.add("".join(str(x) for x in COL_SUMS))
    candidates.add("".join(chr(96 + x) for x in ROW_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(64 + x) for x in ROW_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(96 + x) for x in COL_SUMS if 1 <= x <= 26))
    candidates.add("".join(chr(64 + x) for x in COL_SUMS if 1 <= x <= 26))
    candidates.add(FLAT_BITS)
    candidates.add(FLAT_BITS.replace("0", "a").replace("1", "b"))

    # 6. Chess-derived
    candidates.add(FEN)
    candidates.add(FEN.replace("/", ""))
    candidates.add(FEN.replace(" ", ""))
    candidates.add("fubcd")
    candidates.add("fubcdking")
    candidates.add("oraclequeen")
    candidates.add("checkmate")
    candidates.add("stalemate")
    candidates.add("castling")
    candidates.add("enpassant")
    for p in ["B5KR", "1r5B", "2R5", "2b1p1p1", "2P1k1P1", "1p2P2p", "1P2P2P", "3N1N2"]:
        candidates.add(p)

    # 7. VIC result transformations
    candidates.add(VIC_RESULT)
    candidates.add(VIC_NOSP)
    candidates.add(VIC_LOWER)
    candidates.add(VIC_UPPER)
    for s in VIC_NOSP.split("AND"):
        candidates.add(s.strip())
    candidates.add("halfandbetterhalf")
    candidates.add("half")
    candidates.add("betterhalf")
    candidates.add("betterhalfandhalf")
    candidates.add("HALFANDBETTERHALF")

    # 8. Color counts / yin-yang
    for yy in ["69", "96", "6", "9", "15", "yingyang", "yinyang", "taijitu", "dualite", "duality", "cosmicduality", "yellow6blue9", "yellowblue69", "blue9yellow6", "6yellow9blue", "yellowblue", "blueyellow", "yingyang69", "yingyang96", "69yingyang", "96yingyang", "sixnine", "ninesix", "sixandnine", "nineandsix", "sixplnine", "nineplsix", "6plus9", "9plus6", "sixninesix", "ninesixnine"]:
        candidates.add(yy)

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

    # 10. Creator hints
    creator = [
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
        "thepreviousthereisanotherdoorhintisstillathing",
        "anotherdoor",
        "globallysupportingmygeneration",
    ]
    for c in creator:
        candidates.add(c)
        candidates.add(c.lower())
        candidates.add(c.upper())

    # 11. Matrix / Alice references
    for ref in ["neo", "trinity", "morpheus", "oracle", "architect", "keymaker", "smith", "zion", "matrix", "thematrix", "thematrixhasyou", "wakeupneo", "knockknockneo", "followthewhiterabbit", "thereisnospoon", "redpill", "bluepill", "purplepill", "alice", "wonderland", "cheshirecat", "whiterabbit", "madhatter", "teaparty", "dormouse", "rabbithole", "entertherabbithole", "leavethematrix"]:
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

    # 13. Combinations with causality
    for part in PARTS:
        candidates.add("causality" + part)
        candidates.add(part + "causality")
        candidates.add("causality" + part + "matrixsumlist")

    # 14. Address and hash
    addr = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
    candidates.add(addr)
    candidates.add(addr.lower())
    candidates.add("GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe")
    candidates.add("GSMGIO5BTCPUZZLECHALLENGE")
    candidates.add("gsmgio5btcpuzzlechallenge")

    # 15. URL
    url = "gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"
    candidates.add(url)
    candidates.add(url.replace("/", ""))
    candidates.add("89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32")

    # 16. OP_RETURN messages
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

    # 17. "Half and better half" combos
    for sep in ["", " ", "and", "&", "+", "_", "-"]:
        candidates.add("half" + sep + "betterhalf")
        candidates.add("betterhalf" + sep + "half")
        candidates.add("half" + sep + "better" + sep + "half")

    # 18. Prime-related
    for p in ["prime", "primes", "primebasic", "primebasics", "primenumber", "twentythree", "twenty-three", "sixteen", "seven", "overtwentythreeciphers", "sixteenencryptions", "sevenintertwinedpasswords", "reinsertingtheprimebasics", "returntothesourcecodes", "sourcecodes"]:
        candidates.add(p)
        candidates.add(p.lower())
        candidates.add(p.upper())

    # 19. Little Prince
    for lp in ["thelittleprince", "lepetitprince", "whatisessentialisinvisibletotheeye", "itisonlywiththeheartthatoneseesrightly", "baobab", "rose", "thefox"]:
        candidates.add(lp)

    # 20. Numbers from poem / hints
    for n in ["23", "16", "7", "42", "11110", "1616", "2019", "2020", "2021", "2023", "2001", "09112001", "9112001", "911"]:
        candidates.add(n)

    # 21. "Ciao bella o" variants
    for cb in ["ciao bella o", "ciaobellao", "ciao bella", "ciaobella", "bella o", "bellao"]:
        candidates.add(cb)

    # 22. Square and rabbit
    for sr in ["squareandarabbit", "sqaureandarabbit", "rabbitandsquare", "rabbitsnest", "squaresandrabbits", "squaresandrabbit"]:
        candidates.add(sr)

    # 23. Safenet Luna HSM
    for slh in ["SafenetLunaHSM11110", "SafenetLunaHSM", "safenetlunahsm", "safenet", "luna", "hsm", "11110"]:
        candidates.add(slh)

    # 24. Date hints
    for d in ["20190420", "20200101", "20200706", "20250903", "20211231", "20210806"]:
        candidates.add(d)

    # 25. Block heights
    for bh in ["964501", "949653", "209999", "1357"]:
        candidates.add(bh)

    # 26. Dbbi / faed
    candidates.add("dbbi")
    candidates.add("faed")
    candidates.add("dbbifaed")
    candidates.add("faeddbbi")

    # 27. All phases concatenated
    candidates.add("".join(phase_pws))
    candidates.add("".join(phase_pws).lower())

    # Remove empty and return sorted for determinism
    candidates.discard("")
    candidates.discard(None)
    return sorted(candidates)


# ---------------------------------------------------------------------------
# Main brute-force loop
# ---------------------------------------------------------------------------
def main():
    kdfs = ["sha256", "md5", "sha1", "direct", "direct-sha256", "direct-md5"]
    files = [
        ("SalPhaseion", SALPH_SALT, SALPH_CT),
        ("CosmicDuality", COSMIC_SALT, COSMIC_CT),
    ]

    candidates = build_candidates()
    print(f"Built {len(candidates)} base candidates.")

    # Add hash variants (SHA256, MD5, SHA1 of each candidate)
    hash_candidates = []
    for c in candidates:
        hash_candidates.append(c)
        hash_candidates.append(sha256_str(c))
        hash_candidates.append(md5_str(c))
        hash_candidates.append(sha1_str(c))

    # Deduplicate
    seen = set()
    all_candidates = []
    for c in hash_candidates:
        if c and c not in seen:
            seen.add(c)
            all_candidates.append(c)

    print(f"Total with hash variants: {len(all_candidates)} candidates.")
    print(f"Testing {len(files)} blobs x {len(kdfs)} KDFs = up to {len(all_candidates) * len(files) * len(kdfs)} attempts.")
    print("=" * 60)

    found = 0
    total = 0

    for label, salt, ct in files:
        print(f"\n--- Testing {label} ---")
        for kdf in kdfs:
            print(f"  KDF: {kdf}")
            for pwd in all_candidates:
                total += 1
                result = try_decrypt(pwd, salt, ct, kdf=kdf)
                if result:
                    found += 1
                    text = result.decode("utf-8", errors="replace")
                    print(f"\n*** FOUND decryption #{found} ***")
                    print(f"  Blob:    {label}")
                    print(f"  KDF:     {kdf}")
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
                        f.write(f"KDF:      {kdf}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{text}\n")
                        f.write("=" * 60 + "\n")

                    # Also save individual file
                    detail_path = os.path.join(RESULTS_DIR, f"success_{label.lower()}_{found}.txt")
                    with open(detail_path, "w") as f:
                        f.write(f"Blob:     {label}\n")
                        f.write(f"KDF:      {kdf}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{text}\n")

            print(f"  {kdf} complete.")

    print(f"\n{'=' * 60}")
    print(f"Done. {found} successful decryption(s) out of {total} attempts.")
    if found:
        print(f"Results saved to {RESULTS_DIR}/success.txt")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
