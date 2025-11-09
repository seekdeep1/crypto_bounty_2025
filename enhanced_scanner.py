#!/usr/bin/env python3
import requests
import time
import re
import subprocess

def scan_with_slither(contract_address):
    try:
        # validate ethereum address (0x + 40 hex chars)
        if not re.fullmatch(r"0x[a-fA-F0-9]{40}", str(contract_address)):
            print(f"⚠️ Skipping invalid address: {contract_address}")
            return False
        print(f"🔍 Scanning {contract_address} with Slither...")
        result = subprocess.run(["slither", contract_address, "--detect", "reentrancy-eth"], capture_output=True, text=True, timeout=60)
        if "INFO:Detectors:" in result.stdout:
            print(f"🚨 VULNERABILITY FOUND in {contract_address}!")
            print(result.stdout)
            return True
    except subprocess.TimeoutExpired:
        print(f"⚠️ Slither timed out for {contract_address}")
    except Exception as e:
        print(f"⚠️ Scan failed: {e}")
    return False


def get_new_protocols():
    try:
        response = requests.get("https://api.llama.fi/protocols", timeout=10)
        protocols = response.json()
        # keep only entries with a valid Ethereum address (0x + 40 hex chars)
        new_protocols = [p for p in protocols if p.get("address") and re.fullmatch(r"0x[a-fA-F0-9]{40}", str(p["address"]))]
        # optional: prefer entries with an addedToDefillama timestamp if present
        new_protocols.sort(key=lambda x: x.get("addedToDefillama") or 0, reverse=True)
        return new_protocols[:3]
    except Exception as e:
        print(f"API Error: {e}")
        return []

print("🤖 ENHANCED AUTOMATED HUNTER ACTIVATED")
while True:
    print(f"🕐 Scan cycle: {time.ctime()}")
    targets = get_new_protocols()
    
    if targets:
        print(f"🎯 Found {len(targets)} new protocols")
        for target in targets:
            print(f"🔍 Target: {target.get('name', 'Unknown')}")
            if target.get('address'):
                scan_with_slither(target['address'])
    else:
        print("⏳ No new protocols found...")
    
    time.sleep(600)
