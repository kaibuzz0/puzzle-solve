#!/usr/bin/env python3
"""
Fresh brute-force attempt for GSMG.IO remaining AES blobs
Tests new password ideas not in existing attack logs
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

def generate_fresh_candidates():
    candidates = []
    
    # === POEM ===
    poem = "Roses are White but often Red. Yellow has a number and so does Blue. Go back to the first puzzle piece without further ado. It might have shown you only one door, beware that the rabbits nest may contain a whole lot more. Hush hush."
    candidates.append(poem)
    candidates.append(sha256(poem))
    candidates.append(poem.lower().replace(" ", ""))
    candidates.append(sha256(poem.lower().replace(" ", "")))
    candidates.append(poem.lower().replace(" ", "").replace(".", ""))
    candidates.append(sha256(poem.lower().replace(" ", "").replace(".", "")))
    
    # === HUSH HUSH ===
    for h in ["hushhush", "HUSHHUSH", "HushHush", "hush hush", "HUSH HUSH"]:
        candidates.append(h)
        candidates.append(sha256(h))
    
    # === FIRST PUZZLE PIECE ===
    for fpp in ["theseedisplanted", "firstpuzzlepiece", "thefirstpuzzlepiece", "gobacktothefirstpuzzlepiece"]:
        candidates.append(fpp)
        candidates.append(sha256(fpp))
    
    # === RABBIT ===
    for r in ["rabbitsnest", "whiterabbit", "followthewhiterabbit", "entertherabbithole", "rabbithole", "rabbitnest"]:
        candidates.append(r)
        candidates.append(sha256(r))
    
    # === YIN YANG / DUALITY ===
    for yy in ["yinyang", "yingyang", "duality", "cosmicduality", "halfandbetterhalf", "halfbetterhalf", "betterhalf", "halfhalf"]:
        candidates.append(yy)
        candidates.append(sha256(yy))
    
    # === PRIME BASICS ===
    for pb in ["primebasics", "primebasic", "primenumber", "primes", "twentythree", "seven", "sixteen", "reinsertingtheprimebasics"]:
        candidates.append(pb)
        candidates.append(sha256(pb))
    
    # === OUR FIRST HINT IS YOUR LAST COMMAND ===
    for hint in ["ourfirsthintisyourlastcommand", "firsthint", "lastcommand", "yourlastcommand", "ourfirsthint"]:
        candidates.append(hint)
        candidates.append(sha256(hint))
    
    # === MATRIX COMBOS ===
    for mc in ["thematrixhasyou", "thematrix", "matrixhasyou", "hastheanswer", "wakeupneo", "knockknockneo", "followthewhiterabbit", "thereisnospoon", "redpill", "bluepill", "purplepill"]:
        candidates.append(mc)
        candidates.append(sha256(mc))
    
    # === ALICE ===
    for a in ["alice", "wonderland", "cheshirecat", "dormouse", "threesisters", "elsie", "lacie", "tillie", "whiterabbit", "teaparty", "madhatter"]:
        candidates.append(a)
        candidates.append(sha256(a))
    
    # === LITTLE PRINCE ===
    for lp in ["thelittleprince", "lepetitprince", "whatisessentialisinvisibletotheeye", "itisonlywiththeheartthatoneseesrightly", "baobab", "rose"]:
        candidates.append(lp)
        candidates.append(sha256(lp))
    
    # === ANSWER IS WOMEN ===
    for w in ["women", "thewomen", "theansweriswomen", "answeriswomen", "threegirls", "threesisters", "elsielacietillie"]:
        candidates.append(w)
        candidates.append(sha256(w))
    
    # === CREATOR ===
    for cr in ["jrkbgrt", "jrk", "bgrt", "gsmg", "gsmgio", "globallysupportingmygeneration"]:
        candidates.append(cr)
        candidates.append(sha256(cr))
    
    # === SOURCE CODE ===
    for sc in ["returntothesourcecodes", "sourcecodes", "maincpp", "bitcoinsource", "satoshi", "genesisblock"]:
        candidates.append(sc)
        candidates.append(sha256(sc))
    
    # === COMBINE DECODED STRINGS WITH SEPARATORS ===
    parts = ["matrixsumlist", "enter", "lastwordsbeforearchichoice", "thispassword"]
    for sep in ["", " ", "_", "-", ".", ",", "0", "1", "2"]:
        candidates.append(sep.join(parts))
        candidates.append(sha256(sep.join(parts)))
    
    # === ZEROED OUT VARIATIONS ===
    # Replace o with 0 in each part
    zeroed_parts = [p.replace('o', '0') for p in parts]
    candidates.append(''.join(zeroed_parts))
    candidates.append(sha256(''.join(zeroed_parts)))
    
    # Replace vowels with 0
    vowel_zeroed = [p.replace('a','0').replace('e','0').replace('i','0').replace('o','0').replace('u','0') for p in parts]
    candidates.append(''.join(vowel_zeroed))
    candidates.append(sha256(''.join(vowel_zeroed)))
    
    # === PRIME POSITION LETTERS ===
    # Keep only letters at prime positions (2,3,5,7,11,13,...)
    def prime_only(s):
        primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
        return ''.join(s[i-1] for i in primes if i <= len(s))
    
    prime_parts = [prime_only(p) for p in parts]
    candidates.append(''.join(prime_parts))
    candidates.append(sha256(''.join(prime_parts)))
    
    # === NON-PRIME POSITION LETTERS (zero out primes) ===
    def non_prime_only(s):
        non_primes = [1,4,6,8,9,10,12,14,15,16,18,20,21,22,24,25,26,27,28]
        return ''.join(s[i-1] for i in non_primes if i <= len(s))
    
    non_prime_parts = [non_prime_only(p) for p in parts]
    candidates.append(''.join(non_prime_parts))
    candidates.append(sha256(''.join(non_prime_parts)))
    
    # === COMBINE WITH VIC RESULT ===
    vic = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
    vic_nospace = vic.replace(" ", "")
    for part in parts:
        candidates.append(part + vic_nospace)
        candidates.append(sha256(part + vic_nospace))
        candidates.append(vic_nospace + part)
        candidates.append(sha256(vic_nospace + part))
    
    # === VIC RESULT MODIFIED ===
    candidates.append(vic_nospace)
    candidates.append(sha256(vic_nospace))
    candidates.append(vic_nospace.lower())
    candidates.append(sha256(vic_nospace.lower()))
    candidates.append(vic_nospace.upper())
    candidates.append(sha256(vic_nospace.upper()))
    
    # === SHA256 OF ALL PHASE PASSWORDS ===
    phase_passwords = [
        "theseedisplanted",
        "theflowerblossomsthroughwhatseemstobeaconcretesurface",
        "causality",
        "jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple",
        "THEMATRIXHASYOU",
        vic_nospace,
    ]
    all_phases = ''.join(phase_passwords)
    candidates.append(sha256(all_phases))
    candidates.append(all_phases)
    
    # === ADDRESS ===
    addr = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
    candidates.append(addr)
    candidates.append(sha256(addr))
    candidates.append(addr.lower())
    candidates.append(sha256(addr.lower()))
    
    # === BECH32 ===
    bech32 = "bc1qks8zrshwmu3m8vgqdzwl2u8jjfgnvgjlezwqcd"
    candidates.append(bech32)
    candidates.append(sha256(bech32))
    
    # === OP_RETURN MESSAGES ===
    op_msgs = [
        "hereismysecret",
        "theansweriswomen",
        "SOLUTION",
        "isolveditwithanabacus",
        "iamtheone",
        "thereisnospoon",
        "fromneo",
        "redpill",
        "entertherabbithole",
        "leavethematrix",
        "happyxmasEverythingThatHasABeginningHasAnEnd",
        "causalitytranscended",
        "turingcomplete",
        "halving",
        "ALPHANOISES",
        "THEMATRIXHASYOU",
        "fanstoo",
        "whatisessentialisinvisibletotheeye",
    ]
    for msg in op_msgs:
        candidates.append(msg)
        candidates.append(sha256(msg))
        candidates.append(msg.lower())
        candidates.append(sha256(msg.lower()))
    
    # === OP_RETURN ALL ===
    all_op = ''.join(op_msgs)
    candidates.append(sha256(all_op))
    candidates.append(all_op)
    
    # === CHESS POSITION ===
    chess = "B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2"
    candidates.append(chess)
    candidates.append(sha256(chess))
    candidates.append(chess.replace("/", ""))
    candidates.append(sha256(chess.replace("/", "")))
    
    # === PUZZLE URL ===
    url = "gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32"
    candidates.append(url)
    candidates.append(sha256(url))
    candidates.append(url.replace("/", ""))
    candidates.append(sha256(url.replace("/", "")))
    
    # === DATE HINTS ===
    for d in ["20190420", "20200101", "20200706", "20250903"]:
        candidates.append(d)
        candidates.append(sha256(d))
    
    # === BLOCK HEIGHT ===
    for bh in ["964501", "949653", "209999", "1357"]:
        candidates.append(bh)
        candidates.append(sha256(bh))
    
    # === SQUARE AND RABBIT ===
    for sr in ["sqauresandarabbit", "sqaureandarabbit", "squareandarabbit", "rabbitandsquare"]:
        candidates.append(sr)
        candidates.append(sha256(sr))
    
    # === PURPLE PILL ===
    for pp in ["purplepill", "purple", "pill", "candyflipping"]:
        candidates.append(pp)
        candidates.append(sha256(pp))
    
    # === 42 ===
    for a in ["42", "fortytwo", "theanswer", "answer", "answertoeverything"]:
        candidates.append(a)
        candidates.append(sha256(a))
    
    # === CREATOR CHAT MESSAGES ===
    creator_msgs = [
        "thepuzzletalksforme",
        "youhavealltheinfo",
        "thehardestpartisdone",
        "onceyouhitayinyang",
        "globallysupportingmygeneration",
        "thepreviousthereisanotherdoorhintisstillathing",
        "primeandzero",
        "primeandzeroout",
    ]
    for msg in creator_msgs:
        candidates.append(msg)
        candidates.append(sha256(msg))
    
    # Remove duplicates and empty
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
    
    print("Generating fresh password candidates...")
    candidates = generate_fresh_candidates()
    print(f"Generated {len(candidates)} unique candidates")
    print(f"Testing {len(files)} files x {len(ciphers)} ciphers = up to {len(candidates) * len(files) * len(ciphers)} attempts")
    print("=" * 60)
    
    found = 0
    total = 0
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"\nSKIP: {filepath} not found")
            continue
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
                    print(f"  Password: {pwd[:80]}{'...' if len(pwd)>80 else ''}")
                    print(f"  Content ({len(result)} chars):")
                    print(f"  {'='*50}")
                    print(result[:500])
                    print(f"  {'='*50}")
                    found += 1
                    
                    out_file = f"/root/puzzle-solve/results/decrypt_found_{found}.txt"
                    with open(out_file, "w") as f:
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
