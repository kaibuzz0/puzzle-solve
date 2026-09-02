#!/usr/bin/env python3
"""
GSMG.IO 5 BTC Puzzle Solver - Main Entry Point

This script verifies all known solved stages and attempts to decrypt
remaining unsolved AES blobs.
"""

import sys
sys.path.insert(0, '/root/puzzle-solve/tools')

from aes_decrypt import build_password_list, try_decrypt
from beaufort import beaufort_decrypt
from vic import decode_vic

def main():
    print("=" * 60)
    print("GSMG.IO 5 BTC PUZZLE SOLVER")
    print("=" * 60)
    
    # 1. Verify VIC cipher (Phase 3.2.2)
    print("\n[1] Verifying VIC cipher (Phase 3.2.2)...")
    CIPHERTEXT = "15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112"
    result = decode_vic(CIPHERTEXT, "FUBCDORALTHINGKYMVPSJQZXW", 1, 4)
    expected = "IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE"
    if result == expected:
        print(f"    [PASS] VIC cipher verified!")
    else:
        print(f"    [WARN] Got: {result}")
        print(f"    Expected: {expected}")
    
    # 2. Try SalPhaseion AES blob
    print("\n[2] Attempting SalPhaseion AES blob decryption...")
    print("    File: data/salphaselon_encrypted.txt")
    passwords = build_password_list()
    results = try_decrypt("/root/puzzle-solve/data/salphaselon_encrypted.txt", passwords)
    if results:
        print(f"    FOUND {len(results)} decryption(s)!")
        for r in results:
            print(f"\n--- Decrypted Text (password: {r['password'][:40]}...) ---")
            print(r['text'][:500])
    else:
        print("    No successful decryption found with current password list.")
        print("    The SalPhaseion AES blob remains unsolved - community help needed!")
    
    # 3. Active clues summary
    print("\n[3] Active unsolved clues:")
    print("    - SalPhaseion AES blob needs correct password")
    print("    - 'matrixsumlist' + 'enter' + 'lastwordsbeforearchichoice' + 'thispassword'")
    print("    - 'HASHTHETEXT' from Decentraland audio hint")
    print("    - 'HALF AND BETTER HALF' - suggests 2 keys or split private key")
    print("    - Chess references may still have hidden meaning")
    
    print("\n" + "=" * 60)
    print("Solver complete. See known_solutions.md and remaining_puzzles.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
