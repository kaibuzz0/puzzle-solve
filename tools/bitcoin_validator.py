#!/usr/bin/env python3
"""
Targeted brute-force with strict Bitcoin key validation
For GSMG.IO SalPhaseion and Cosmic Duality AES blobs
"""

import subprocess
import hashlib
import os
import sys
import struct

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
                return data
        if os.path.exists(outpath):
            os.remove(outpath)
    except Exception:
        pass
    return None

def is_valid_wif(key_bytes):
    """Check if bytes form a valid Bitcoin WIF key"""
    if len(key_bytes) == 32:
        # Raw private key - could be uncompressed WIF if prefixed with 0x80
        return False  # Need to check with prefix
    if len(key_bytes) == 33:
        # Possibly compressed WIF (32 bytes + 0x01 suffix)
        if key_bytes[-1] == 0x01:
            # This might be a compressed private key format
            return True
    if len(key_bytes) == 37:
        # Extended key format
        pass
    return False

def check_bitcoin_key(data):
    """Check if decrypted data contains a valid Bitcoin private key"""
    # Try extracting hex keys (64 chars)
    text = None
    try:
        text = data.decode('utf-8')
    except:
        try:
            text = data.decode('latin-1')
        except:
            pass
    
    if text:
        # Look for 64-char hex string
        import re
        hex_keys = re.findall(r'[0-9a-fA-F]{64}', text)
        for hk in hex_keys:
            # Check if it's a valid private key (between 1 and n-1)
            try:
                val = int(hk, 16)
                if 0 < val < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
                    return f"HEX_KEY:{hk}"
            except:
                pass
        
        # Look for WIF format (51 chars starting with 5, or 52 starting with K/L)
        wif51 = re.findall(r'5[1-9A-HJ-NP-Za-km-z]{50}', text)
        for w in wif51:
            return f"WIF51:{w}"
        wif52 = re.findall(r'[KL][1-9A-HJ-NP-Za-km-z]{51}', text)
        for w in wif52:
            return f"WIF52:{w}"
    
    # Check raw bytes for specific patterns
    if len(data) == 32:
        val = int.from_bytes(data, 'big')
        if 0 < val < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
            return f"RAW32BYTES:{data.hex()}"
    
    if len(data) == 33 and data[-1] == 0x01:
        val = int.from_bytes(data[:32], 'big')
        if 0 < val < 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141:
            return f"RAW_COMPRESSED:{data.hex()}"
    
    return None

def generate_candidates():
    candidates = []
    
    # All decoded strings with zeroing variations
    base = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]
    
    # Direct strings
    for s in base:
        candidates.append(s)
        candidates.append(sha256(s))
    
    # Concatenations
    candidates.append(''.join(base))
    candidates.append(sha256(''.join(base)))
    
    # With zeroed vowels
    for s in base:
        z = s.replace('a','0').replace('e','0').replace('i','0').replace('o','0').replace('u','0')
        candidates.append(z)
        candidates.append(sha256(z))
    
    # With 'o' zeroed (as in A1Z26 decode)
    for s in base:
        z = s.replace('o','0')
        candidates.append(z)
        candidates.append(sha256(z))
    
    # Chess + puzzle combos
    chess_terms = ["checkmate", "stalemate", "kingside", "queenside", "enpassant", "castling", "fubcd", "oraclequeen"]
    for c in chess_terms:
        candidates.append(c)
        candidates.append(sha256(c))
        for b in base:
            candidates.append(b + c)
            candidates.append(sha256(b + c))
            candidates.append(c + b)
            candidates.append(sha256(c + b))
    
    # Matrix + Alice combos
    refs = ["neo", "trinity", "morpheus", "architect", "oracle", "keymaker", "alice", "whiterabbit", "cheshire", "dormouse", "wonderland"]
    for r in refs:
        candidates.append(r)
        candidates.append(sha256(r))
        for b in base:
            candidates.append(b + r)
            candidates.append(sha256(b + r))
    
    # Prime-related
    prime_words = ["prime", "primes", "primebasic", "primebasics", "twentythree", "twentythree", "sixteen", "seven", "primenumbers", "reinsertingprimebasics"]
    for p in prime_words:
        candidates.append(p)
        candidates.append(sha256(p))
    
    # Duality / yin-yang
    duality = ["yingyang", "yinyang", "duality", "cosmicduality", "dualite", "halves", "betterhalf", "half", "twohalves"]
    for d in duality:
        candidates.append(d)
        candidates.append(sha256(d))
    
    # Tea party / dessert
    for tp in ["teaparty", "teapartywithalice", "dessert", "specialdessert", "aliceinthematrix"]:
        candidates.append(tp)
        candidates.append(sha256(tp))
    
    # Hush hush variants
    for h in ["hush", "hushhush", "hushhushhush", "shhhh", "quiet", "silence", "silent"]:
        candidates.append(h)
        candidates.append(sha256(h))
    
    # VIC result parts
    vic_parts = ["half", "betterhalf", "better", "privatekeys", "fundstolive", "crackthis", "manage"]
    for v in vic_parts:
        candidates.append(v)
        candidates.append(sha256(v))
    
    # Source code reference
    for sc in ["returntothesourcecodes", "sourcecodes", "source", "codes", "maincpp", "main", "cpp", "line1616"]:
        candidates.append(sc)
        candidates.append(sha256(sc))
    
    # OP_RETURN combined
    op_combined = "hereismysecrettheansweriswomenSOLUTIONisolveditwithanabacusiamtheonethereisnospoonfromneoredpillentertherabbitholeleavethematrixwhatisessentialisinvisibletotheeyecausalitytranscendedturingcompletehalvingALPHANOISESTHEMATRIXHASYOUfanstoo"
    candidates.append(op_combined)
    candidates.append(sha256(op_combined))
    
    # Remove duplicates
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
        "/root/puzzle-solve/data/cosmic_duality_encrypted.txt",
    ]
    
    ciphers = ["aes-256-cbc", "aes-256-ecb", "aes-128-cbc", "aes-128-ecb"]
    
    print("Generating candidates...")
    candidates = generate_candidates()
    print(f"Generated {len(candidates)} unique candidates")
    
    total = 0
    found = 0
    key_found = None
    
    for filepath in files:
        if not os.path.exists(filepath):
            continue
        print(f"\n--- {os.path.basename(filepath)} ---")
        for cipher in ciphers:
            for pwd in candidates:
                total += 1
                data = try_decrypt(filepath, pwd, cipher)
                if data:
                    key_check = check_bitcoin_key(data)
                    if key_check:
                        print(f"\n*** BITCOIN KEY FOUND! ***")
                        print(f"  File: {filepath}")
                        print(f"  Cipher: {cipher}")
                        print(f"  Password: {pwd}")
                        print(f"  Key: {key_check}")
                        key_found = {
                            'file': filepath,
                            'cipher': cipher,
                            'password': pwd,
                            'key': key_check,
                            'data': data
                        }
                        found += 1
                    elif len(data) > 10:
                        # Check if it's readable text
                        try:
                            text = data.decode('utf-8')
                            printable = sum(c.isprintable() or c in '\n\r\t' for c in text)
                            if len(text) > 0 and printable / len(text) > 0.8:
                                print(f"  Readable text: {text[:100]}")
                        except:
                            pass
    
    print(f"\n{'='*60}")
    print(f"Done. {found} Bitcoin key(s) found out of {total} attempts.")
    if key_found:
        print(f"\nKEY DETAILS:")
        for k, v in key_found.items():
            if k != 'data':
                print(f"  {k}: {v}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
