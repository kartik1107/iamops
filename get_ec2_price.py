#!/usr/bin/env python3

import os
import sys
import requests


# Jenkins parameter:
# INSTANCE_FAMILY=m7
INSTANCE_FAMILY = os.getenv("INSTANCE_FAMILY")

if len(sys.argv) > 1:
    INSTANCE_FAMILY = sys.argv[1]

if not INSTANCE_FAMILY:
    print("ERROR: Please provide an instance family.")
    print("Usage: python find_cheapest_instance.py m7")
    sys.exit(1)

# Public pricing dataset maintained by Vantage
URL = "https://instances.vantage.sh/instances.json"

try:
    response = requests.get(URL, timeout=30)
    response.raise_for_status()
    instances = response.json()
except Exception as e:
    print(f"Failed to retrieve pricing data: {e}")
    sys.exit(1)

matches = []

for instance in instances:
    instance_type = instance.get("instance_type", "")

    # Match family
    if not instance_type.startswith(INSTANCE_FAMILY):
        continue

    pricing = instance.get("pricing", {})
    us_east_1 = pricing.get("us-east-1", {})

    linux_price = us_east_1.get("linux", {}).get("ondemand")

    if linux_price is None:
        continue

    matches.append({
        "instance_type": instance_type,
        "price": float(linux_price),
        "vcpu": instance.get("vCPU"),
        "memory": instance.get("memory"),
    })

if not matches:
    print(f"No instances found for family '{INSTANCE_FAMILY}'")
    sys.exit(1)

cheapest = min(matches, key=lambda x: x["price"])

print("\n=== Cheapest Instance ===")
print(f"Family        : {INSTANCE_FAMILY}")
print(f"Instance Type : {cheapest['instance_type']}")
print(f"vCPU          : {cheapest['vcpu']}")
print(f"Memory        : {cheapest['memory']}")
print(f"Price/hour    : ${cheapest['price']:.6f}")
