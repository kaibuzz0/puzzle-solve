#!/usr/bin/env python3
"""
Comprehensive password brute-forcer for GSMG.IO SalPhaseion AES blob
"""

import subprocess
import hashlib
import itertools
import os
import sys

# The 14x14 binary matrix from Phase 1
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

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def row_sums():
    return [sum(row) for row in MATRIX]

def col_sums():
    return [sum(MATRIX[r][c] for r in range(14)) for c in range(14)]

def matrix_as_string():
    """Matrix as space-separated binary string"""
    return '\n'.join(' '.join(str(c) for c in row) for row in MATRIX)

def matrix_flat():
    """Matrix as continuous bit string"""
    return ''.join(str(c) for row in MATRIX for c in row)

def generate_password_candidates():
    """Generate all possible password candidates"""
    candidates = set()
    
    # Direct decoded strings
    direct = [
        "matrixsumlist",
        "enter",
        "lastwordsbeforearchichoice",
        "thispassword",
        "matrixsumlistenter",
        "entermatrixsumlist",
        "matrixsumlistenterlastwordsbeforearchichoicethispassword",
        "shabefans too",
        "sha256fans too",
        "hashthetext",
        "HASHTHETEXT",
        "thematrixhasyou",
        "THEMATRIXHASYOU",
        "causality",
        "Safenet",
        "Luna",
        "HSM",
        "jacquefresco",
        "giveitjustonesecond",
        "heisenbergsuncertaintyprinciple",
        "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
        "our first hint is your last command",
        "ourfirsthintisyourlastcommand",
        "lastwords",
        "archichoice",
        "thispassword",
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
        "sixteenencryptions",
        "sevenintertwinedpasswords",
        "twentythreeciphers",
        "GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe",
        "GSMGIO5BTCPUZZLECHALLENGE",
        "gsmg.io/theseedisplanted",
        "theseedisplanted",
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecialdessertiwroteitmyself",
        "11110",
        "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1",
    ]
    
    for p in direct:
        candidates.add(p)
        candidates.add(sha256(p))
    
    # Matrix-derived passwords
    rows = row_sums()
    cols = col_sums()
    
    # Row sums as letters
    row_letters = ''.join(chr(64 + s) if 1 <= s <= 26 else str(s) for s in rows)
    candidates.add(row_letters)
    candidates.add(sha256(row_letters))
    
    # Column sums as letters
    col_letters = ''.join(chr(64 + s) if 1 <= s <= 26 else str(s) for s in cols)
    candidates.add(col_letters)
    candidates.add(sha256(col_letters))
    
    # Row sums as numbers
    row_nums = ''.join(str(s) for s in rows)
    candidates.add(row_nums)
    candidates.add(sha256(row_nums))
    
    # Column sums as numbers
    col_nums = ''.join(str(s) for s in cols)
    candidates.add(col_nums)
    candidates.add(sha256(col_nums))
    
    # Matrix as string
    flat = matrix_flat()
    candidates.add(flat)
    candidates.add(sha256(flat))
    
    # Matrix as ASCII (binary to bytes)
    try:
        matrix_bytes = bytes(int(flat[i:i+8], 2) for i in range(0, len(flat), 8))
        candidates.add(matrix_bytes.hex())
    except:
        pass
    
    # Known puzzle passwords
    known_passwords = [
        "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",
        "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",
        "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",
        "89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32",
    ]
    candidates.update(known_passwords)
    
    # Combined derived passwords
    candidates.add("matrixsumlist" + "enter")
    candidates.add(sha256("matrixsumlist" + "enter"))
    candidates.add("enter" + "matrixsumlist")
    candidates.add(sha256("enter" + "matrixsumlist"))
    candidates.add("lastwordsbeforearchichoice" + "thispassword")
    candidates.add(sha256("lastwordsbeforearchichoice" + "thispassword"))
    
    # All combos with SHA256 of combinations
    for combo in [
        "matrixsumlistenter",
        "matrixsumlistenterlastwordsbeforearchichoicethispassword",
        "lastwordsbeforearchichoicethispassword",
        "matrixsumlistenterthispassword",
    ]:
        candidates.add(combo)
        candidates.add(sha256(combo))
    
    # Remove empty strings and None
    candidates.discard('')
    candidates.discard(None)
    
    return list(candidates)

def try_decrypt(filepath, password, outpath):
    try:
        result = subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-d", "-a",
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
                    if printable / len(text) > 0.6:
                        return text
                except:
                    try:
                        text = data.decode('latin-1')
                        printable = sum(c.isprintable() or c in '\n\r\t' for c in text)
                        if printable / len(text) > 0.6:
                            return text
                    except:
                        pass
        if os.path.exists(outpath):
            os.remove(outpath)
    except Exception as e:
        pass
    return None

def main():
    filepath = "/root/puzzle-solve/data/salphaselon_encrypted.txt"
    outpath = "/tmp/salpha_test.dec"
    
    print("Generating password candidates...")
    candidates = generate_password_candidates()
    print(f"Generated {len(candidates)} candidates")
    
    found = []
    for i, pwd in enumerate(candidates):
        if i % 100 == 0:
            print(f"  Trying {i}/{len(candidates)}...")
        result = try_decrypt(filepath, pwd, outpath)
        if result:
            print(f"\n*** SUCCESS! ***")
            print(f"Password: {pwd}")
            print(f"Content preview: {result[:300]}")
            found.append((pwd, result))
            
            # Save to file
            with open(f"/root/puzzle-solve/results/salpha_decrypted_{len(found)}.txt", "w") as f:
                f.write(f"Password: {pwd}\n")
                f.write("=" * 60 + "\n")
                f.write(result)
    
    print(f"\nDone. Found {len(found)} successful decryption(s).")
    if found:
        print(f"Results saved to /root/puzzle-solve/results/")

if __name__ == "__main__":
    main()
