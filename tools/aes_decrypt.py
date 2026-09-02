# AES Decryption Helper
# For the GSMG.IO puzzle, all encrypted blobs use openssl AES-256-CBC with base64 encoding
# The password is always a SHA256 hash string (64 hex chars)

import subprocess
import hashlib
import os

# Known SHA256 passwords that have successfully decrypted phases
KNOWN_PASSWORDS = [
    "eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf",  # Phase 2: causality
    "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5",  # Phase 3
    "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c",  # Phase 3.2
]

# Derived passwords to try on SalPhaseion blob
DERIVED_PASSWORDS = [
    "matrixsumlist",
    "enter", 
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlistenter",
    "enterthispassword",
    "lastwordsbeforearchichoicethispassword",
    "matrixsumlistenterlastwordsbeforearchichoicethispassword",
    "shabefans too",
    "sha256fans too",
    "hashthetext",
    "THEMATRIXHASYOU",
    "thematrixhasyou",
]

# Passwords derived from the Architect's text clues
ARCHITECT_CLUES = [
    "return to the source codes",
    "return to the source",
    "source codes",
    "reinserting the prime basics",
    "prime basics",
    "overtwentythreeciphers",
    "sixteenencryptions",
    "sevenintertwinedpasswords",
    "ciao bella o",
    "ciaobellao",
    "ciao bella",
    "half and better half",
    "halfandbetterhalf",
    "better half",
    "betterhalf",
]

def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def build_password_list():
    """Build full list of passwords to try (raw + SHA256 of each)"""
    passwords = []
    
    # Direct known passwords
    passwords.extend(KNOWN_PASSWORDS)
    
    # Derived strings and their SHA256
    for p in DERIVED_PASSWORDS:
        passwords.append(p)
        passwords.append(sha256(p))
    
    # Architect clues and their SHA256
    for p in ARCHITECT_CLUES:
        passwords.append(p)
        passwords.append(sha256(p))
    
    # Combine some derived passwords
    passwords.append(sha256("matrixsumlist"))
    passwords.append(sha256("enter"))
    passwords.append(sha256("lastwordsbeforearchichoice"))
    passwords.append(sha256("thispassword"))
    passwords.append(sha256("matrixsumlist" + "enter"))
    passwords.append(sha256("matrixsumlist" + "enter" + "lastwordsbeforearchichoice"))
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for p in passwords:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result

def decrypt_aes_file(filepath, password, outpath=None):
    """Try to decrypt an AES-256-CBC base64 file with openssl"""
    if outpath is None:
        outpath = filepath + ".dec"
    
    try:
        result = subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-d", "-a", 
             "-in", filepath, "-out", outpath,
             "-pass", "pass:" + password],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            # Check if output is valid (not empty, contains readable text)
            if os.path.exists(outpath) and os.path.getsize(outpath) > 0:
                with open(outpath, 'rb') as f:
                    data = f.read()
                # Quick check for non-gibberish (mostly printable or valid UTF-8)
                try:
                    text = data.decode('utf-8')
                    printable_ratio = sum(c.isprintable() or c in '\n\r\t' for c in text) / len(text)
                    if printable_ratio > 0.7:
                        return {"success": True, "text": text, "password": password}
                except UnicodeDecodeError:
                    # Try latin-1 as fallback
                    text = data.decode('latin-1')
                    printable_ratio = sum(c.isprintable() or c in '\n\r\t' for c in text) / len(text)
                    if printable_ratio > 0.7:
                        return {"success": True, "text": text, "password": password}
            # Clean up failed attempt
            if os.path.exists(outpath):
                os.remove(outpath)
        return {"success": False, "error": result.stderr}
    except Exception as e:
        return {"success": False, "error": str(e)}

def try_decrypt(filepath, passwords):
    """Try multiple passwords on a file and return results"""
    results = []
    for pwd in passwords:
        result = decrypt_aes_file(filepath, pwd)
        if result["success"]:
            results.append(result)
            print(f"  SUCCESS with: {pwd[:30]}...")
            print(f"  Output preview: {result['text'][:200]}...")
    return results
