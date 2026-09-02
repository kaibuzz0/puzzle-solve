#!/usr/bin/env python3
"""
Ultra-comprehensive brute-forcer for GSMG.IO remaining AES blobs
"""

import subprocess
import hashlib
import os
import sys
import itertools

def sha256(text):
    if isinstance(text, bytes):
        return hashlib.sha256(text).hexdigest()
    return hashlib.sha256(text.encode()).hexdigest()

def try_decrypt(filepath, password, cipher="aes-256-cbc", outpath="/tmp/test.dec"):
    try:
        result = subprocess.run(
            ["openssl", "enc", f"-{cipher}", "-d", "-a",
             "-in", filepath, "-out", outpath,
             "-pass", "pass:" + password],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and os.path.exists(outpath):
            size = os.path.getsize(outpath)
            if size > 0:
                with open(outpath, 'rb') as f:
                    data = f.read()
                try:
                    text = data.decode('utf-8')
                    printable = sum(c.isprintable() or c in '\n\r\t' for c in text)
                    if len(text) > 0 and printable / len(text) > 0.6:
                        return text
                except:
                    try:
                        text = data.decode('latin-1')
                        printable = sum(c.isprintable() or c in '\n\r\t' for c in text)
                        if len(text) > 0 and printable / len(text) > 0.6:
                            return text
                    except:
                        pass
        if os.path.exists(outpath):
            os.remove(outpath)
    except Exception:
        pass
    return None

def generate_candidates():
    candidates = []
    
    # === RAW STRINGS (not hashed) ===
    raw_strings = [
        "causality",
        "matrixsumlist",
        "enter",
        "lastwordsbeforearchichoice",
        "thispassword",
        "matrixsumlistenter",
        "entermatrixsumlist",
        "matrixsumlistenterlastwordsbeforearchichoicethispassword",
        "matrixsumlistenterthispassword",
        "lastwordsbeforearchichoicethispassword",
        "thispasswordlastwordsbeforearchichoice",
        "shabefans too",
        "sha256fans too",
        "hashthetext",
        "HASHTHETEXT",
        "thematrixhasyou",
        "THEMATRIXHASYOU",
        "halfandbetterhalf",
        "half",
        "betterhalf",
        "ciao bella o",
        "ciaobellao",
        "return to the source codes",
        "returntothesourcecodes",
        "sourcecodes",
        "prime basics",
        "primebasics",
        "reinserting the prime basics",
        "reinsertingtheprimebasics",
        "overtwentythreeciphers",
        "twentythreeciphers",
        "sixteenencryptions",
        "sevenintertwinedpasswords",
        "jacquefresco",
        "giveitjustonesecond",
        "heisenbergsuncertaintyprinciple",
        "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
        "our first hint is your last command",
        "ourfirsthintisyourlastcommand",
        "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
        "GSMGIO5BTCPUZZLECHALLENGE",
        "gsmg.io/theseedisplanted",
        "theseedisplanted",
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself",
        "11110",
        "Safenet",
        "Luna", 
        "HSM",
        "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
        "B5KR/1r5B/6R1/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1",
        "in case you manage to crack this the private keys belong to half and better half and they also need funds to live",
        "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE",
        "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE",
        # VIC result variants
        "halfandbetterhalf",
        "HalfAndBetterHalf",
        "HALFANDBETTERHALF",
        # Other combinations
        "causalityenter",
        "entercausality",
        "causalitymatrixsumlist",
        "causalitylastwords",
        "causalitythispassword",
        "causalitySafenetLunaHSM11110",
        # Chess terms
        "chess",
        "bishop",
        "knight",
        "rook",
        "queen",
        "king",
        "checkmate",
        "stalemate",
        # Matrix references
        "neo",
        "trinity",
        "morpheus",
        "oracle",
        "architect",
        "merovingian",
        "keymaker",
        "smith",
        "zion",
        "matrix",
        "thematrix",
        # Alice in Wonderland
        "alice",
        "wonderland",
        "cheshire",
        "whiterabbit",
        "keyhole",
        "madhatter",
        # GSMG references
        "gsmg",
        "gsmgio",
        "5btc",
        "puzzle",
        # Source code references
        "bitcoin",
        "satoshi",
        "genesis",
        "main.cpp",
        "primebasics",
        "sourcecodes",
    ]
    
    # Add raw strings and their SHA256
    for s in raw_strings:
        candidates.append(s)
        candidates.append(sha256(s))
        candidates.append(s.lower())
        candidates.append(sha256(s.lower()))
        candidates.append(s.upper())
        candidates.append(sha256(s.upper()))
    
    # === KNOWN PASSWORDS ===
    known_passwords = [
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    ]
    candidates.extend(known_passwords)
    
    # === MATRIX DERIVED ===
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
    
    row_sums = [sum(row) for row in MATRIX]
    col_sums = [sum(MATRIX[r][c] for r in range(14)) for c in range(14)]
    
    # Various sum encodings
    candidates.append(''.join(str(s) for s in row_sums))
    candidates.append(sha256(''.join(str(s) for s in row_sums)))
    candidates.append(''.join(str(s) for s in col_sums))
    candidates.append(sha256(''.join(str(s) for s in col_sums)))
    candidates.append(''.join(chr(96+s) for s in row_sums if 1<=s<=26))
    candidates.append(sha256(''.join(chr(96+s) for s in row_sums if 1<=s<=26)))
    candidates.append(''.join(chr(64+s) for s in row_sums if 1<=s<=26))
    candidates.append(sha256(''.join(chr(64+s) for s in row_sums if 1<=s<=26)))
    candidates.append(''.join(chr(96+s) for s in col_sums if 1<=s<=26))
    candidates.append(sha256(''.join(chr(96+s) for s in col_sums if 1<=s<=26)))
    candidates.append(''.join(chr(64+s) for s in col_sums if 1<=s<=26))
    candidates.append(sha256(''.join(chr(64+s) for s in col_sums if 1<=s<=26)))
    
    # Matrix as hex/bytes
    flat = ''.join(str(c) for row in MATRIX for c in row)
    candidates.append(flat)
    candidates.append(sha256(flat))
    
    # === VIC RESULT HASHES ===
    vic_plain = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
    candidates.append(sha256(vic_plain))
    candidates.append(sha256(vic_plain.replace(" ", "")))
    candidates.append(sha256(vic_plain.lower()))
    candidates.append(sha256(vic_plain.upper()))
    candidates.append(sha256("half and better half"))
    candidates.append(sha256("half"))
    candidates.append(sha256("better half"))
    
    # === COMBINATIONS OF DECODED SALPHASEION STRINGS ===
    salpha_strings = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]
    for r in range(1, 5):
        for combo in itertools.permutations(salpha_strings, r):
            s = ''.join(combo)
            candidates.append(s)
            candidates.append(sha256(s))
    
    # === COMBINATIONS WITH CAUSALITY ===
    for s in ["causality", "matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]:
        candidates.append("causality" + s)
        candidates.append(sha256("causality" + s))
        candidates.append(s + "causality")
        candidates.append(sha256(s + "causality"))
    
    # Remove empty and dedupe
    seen = set()
    result = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            result.append(c)
    return result

def main():
    files = [
        "/root/puzzle-solve/data/salphaselon_encrypted.txt",
        "/root/puzzle-solve/data/phase3_2_second_blob.txt",
    ]
    
    ciphers = [
        "aes-256-cbc",
        "aes-256-ecb",
        "aes-128-cbc", 
        "aes-128-ecb",
    ]
    
    print("Generating password candidates...")
    candidates = generate_candidates()
    print(f"Generated {len(candidates)} unique candidates")
    print(f"Testing {len(files)} file(s) x {len(ciphers)} cipher(s) = up to {len(candidates) * len(files) * len(ciphers)} attempts")
    print("=" * 60)
    
    found = 0
    total = 0
    
    for filepath in files:
        print(f"\n--- File: {os.path.basename(filepath)} ---")
        for cipher in ciphers:
            print(f"  Cipher: {cipher}")
            for pwd in candidates:
                total += 1
                result = try_decrypt(filepath, pwd, cipher)
                if result:
                    print(f"\n*** DECRYPTION FOUND! ***")
                    print(f"  File: {filepath}")
                    print(f"  Cipher: {cipher}")
                    print(f"  Password: {pwd[:60]}{'...' if len(pwd)>60 else ''}")
                    print(f"  Content ({len(result)} chars):")
                    print(f"  {'='*50}")
                    print(result[:500])
                    print(f"  {'='*50}")
                    found += 1
                    
                    with open(f"/root/puzzle-solve/results/decrypt_found_{found}.txt", "w") as f:
                        f.write(f"File: {filepath}\n")
                        f.write(f"Cipher: {cipher}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{result}\n")
    
    print(f"\n{'='*60}")
    print(f"Done. {found} decryption(s) found out of {total} total attempts.")
    if found:
        print(f"Results saved to /root/puzzle-solve/results/")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
