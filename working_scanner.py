#!/usr/bin/env python3
import subprocess
import time

# KNOWN WORKING TARGETS FOR TESTING
TARGETS = [
    "0x940181a94A35A4569E4529A3CDfB74e38FD98631",  # Aerodrome Base
    "0x794a61358D6845594F94dc1DB02A252b5b4814aD",  # AAVE V3 Base
    "0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1",  # Uniswap V3 Base
    "0x1F98431c8aD98523631AE4a59f267346ea31F984",  # Uniswap V3 Ethereum
    "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F"   # Synthetix Ethereum
]

def scan_target(address):
    print(f"🔍 Scanning {address}...")
    try:
        # Fast scan for critical vulnerabilities only
        result = subprocess.run(["slither", address, "--detect", "reentrancy-eth,suicidal,controlled-delegatecall"], capture_output=True, text=True, timeout=60)
        if "INFO:Detectors:" in result.stdout:
            print(f"🚨 VULNERABILITY FOUND: {address}")
            lines = result.stdout.split('\n')
            for line in lines:
                if "INFO:Detectors:" in line or "Reference:" in line:
                    print(f"   {line}")
            return True
        else:
            print(f"✅ {address} - No critical issues")
            return False
    except Exception as e:
        print(f"⚠️ {address} - Scan failed or timed out")
        return False

print("🤖 WORKING SCANNER ACTIVATED")
print(f"🎯 Monitoring {len(TARGETS)} known contracts")
cycle = 0

while True:
    cycle += 1
    print(f"\n🔄 CYCLE {cycle} - {time.ctime()}")
    
    vulnerabilities_found = 0
    for target in TARGETS:
        if scan_target(target):
            vulnerabilities_found += 1
    
    print(f"📊 Cycle complete: {vulnerabilities_found} vulnerabilities found")
    print("💤 Waiting 10 minutes for next scan...")
    time.sleep(600)
