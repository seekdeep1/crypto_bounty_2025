#!/usr/bin/env python3
import requests
import json
import time

def get_new_protocols():
    try:
        response = requests.get("https://api.llama.fi/protocols")
        protocols = response.json()
        # Filter new protocols (last 7 days)
        new_protocols = [p for p in protocols if p['addedToDefillama'] > (time.time() - 604800)]
        return new_protocols[:5]  # Return top 5 newest
    except:
        return []

print("🕵️ Live Scanner Activated")
while True:
    targets = get_new_protocols()
    if targets:
        print(f"🎯 Found {len(targets)} new protocols")
        for target in targets:
            print(f"🔍 Analyzing: {target['name']} - {target['address']}")
    time.sleep(300)  # Check every 5 minutes
