#!/usr/bin/env python3
"""
Advanced brute-forcer for remaining GSMG.IO puzzle AES blobs
Tests various passwords and cipher modes
"""

import subprocess
import hashlib
import os
import sys

sys.path.insert(0, '/root/puzzle-solve/tools')

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

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
    
    # Direct strings and their SHA256
    strings = [
        "matrixsumlist",
        "enter",
        "lastwordsbeforearchichoice", 
        "thispassword",
        "matrixsumlistenter",
        "entermatrixsumlist",
        "lastwordsbeforearchichoicethispassword",
        "thispasswordlastwordsbeforearchichoice",
        "matrixsumlistenterlastwordsbeforearchichoicethispassword",
        "matrixsumlistenterthispassword",
        "shabefans too",
        "sha256fans too",
        "hashthetext",
        "HASHTHETEXT",
        "thematrixhasyou",
        "THEMATRIXHASYOU",
        "halfandbetterhalf",
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
        "sixteenencryptions",
        "sevenintertwinedpasswords",
        "causality",
        "Safenet",
        "Luna",
        "HSM",
        "11110",
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
        "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
        "in case you manage to crack this the private keys belong to half and better half and they also need funds to live",
        "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE",
        "INCASEYOUMANAGETOCRACKTHISTHEPRIVATEKEYSBELONGTOHALFANDBETTERHALFANDTHEYALSONEEDFUNDSTOLIVE",
        # Chess move
        "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 w - - 0 1",
    ]
    
    for s in strings:
        candidates.append(s)
        candidates.append(sha256(s))
        # Lowercase version
        candidates.append(s.lower())
        candidates.append(sha256(s.lower()))
        # Uppercase version  
        candidates.append(s.upper())
        candidates.append(sha256(s.upper()))
    
    # Matrix-derived
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
    
    # Matrix sums as strings
    row_sums = [sum(row) for row in MATRIX]
    col_sums = [sum(MATRIX[r][c] for r in range(14)) for c in range(14)]
    
    for sums in [row_sums, col_sums]:
        candidates.append(''.join(str(s) for s in sums))
        candidates.append(sha256(''.join(str(s) for s in sums)))
        candidates.append(''.join(chr(96 + s) for s in sums if 1 <= s <= 26))
        candidates.append(''.join(chr(64 + s) for s in sums if 1 <= s <= 26))
    
    # Known passwords
    known = [
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    ]
    candidates.extend(known)
    
    # Concatenations of decoded strings
    combos = [
        "matrixsumlist" + "enter" + "lastwordsbeforearchichoice" + "thispassword",
        "matrixsumlist" + "enter",
        "enter" + "matrixsumlist",
        "lastwordsbeforearchichoice" + "thispassword",
        "thispassword" + "lastwordsbeforearchichoice",
        "matrixsumlist" + "enter" + "thispassword",
        "matrixsumlist" + "thispassword",
    ]
    for c in combos:
        candidates.append(c)
        candidates.append(sha256(c))
    
    # Hash the VIC result
    vic_result = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
    candidates.append(sha256(vic_result))
    candidates.append(sha256(vic_result.replace(" ", "")))
    candidates.append(sha256(vic_result.lower()))
    
    # Unique and non-empty
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
        "des-cbc",
        "des-ecb",
        "bf-cbc",
        "bf-ecb",
    ]
    
    print("Generating candidates...")
    candidates = generate_candidates()
    print(f"Generated {len(candidates)} candidates")
    print(f"Testing {len(files)} file(s) with {len(ciphers)} cipher(s)")
    print(f"Total attempts: {len(candidates) * len(files) * len(ciphers)}")
    
    found = 0
    total = 0
    for filepath in files:
        print(f"\n--- File: {os.path.basename(filepath)} ---")
        for cipher in ciphers:
            for pwd in candidates:
                total += 1
                result = try_decrypt(filepath, pwd, cipher)
                if result:
                    print(f"  [SUCCESS] cipher={cipher}, pwd={pwd[:50]}...")
                    print(f"  Content: {result[:200]}...")
                    found += 1
                    with open(f"/root/puzzle-solve/results/decrypt_{found}.txt", "w") as f:
                        f.write(f"File: {filepath}\n")
                        f.write(f"Cipher: {cipher}\n")
                        f.write(f"Password: {pwd}\n")
                        f.write(f"Content:\n{result}\n")
            if total > 10000:
                print(f"  Progress: {total} attempts...")
    
    print(f"\nDone. {found} decryption(s) found out of {total} attempts.")

if __name__ == "__main__":
    main()
