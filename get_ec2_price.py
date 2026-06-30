#!/usr/bin/env python3

import argparse
import requests
import sys

# Replace with the correct Vantage API endpoint
API_URL = "https://api.vantage.sh/v1/instances"


def fetch_instances(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    response = requests.get(API_URL, headers=headers, timeout=30)

    response.raise_for_status()

    return response.json()


def get_price(instance):
    """
    Update this if your API response differs.
    """
    try:
        return float(instance["pricing"]["linux"]["ondemand"])
    except Exception:
        return None


def find_cheapest(instances, family, min_vcpu, min_memory):

    matches = []

    for inst in instances:

        instance_type = inst.get("instance_type", "")

        if not instance_type.startswith(family):
            continue

        if inst.get("vcpus", 0) < min_vcpu:
            continue

        if inst.get("memory", 0) < min_memory:
            continue

        price = get_price(inst)

        if price is None:
            continue

        matches.append({
            "instance": instance_type,
            "vcpus": inst["vcpus"],
            "memory": inst["memory"],
            "price": price
        })

    if not matches:
        return None

    return min(matches, key=lambda x: x["price"])


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--family", required=True)
    parser.add_argument("--vcpu", required=True, type=int)
    parser.add_argument("--memory", required=True, type=float)
    parser.add_argument("--token", required=True)

    args = parser.parse_args()

    try:
        instances = fetch_instances(args.token)
    except Exception as e:
        print(f"Failed to fetch Vantage API: {e}")
        sys.exit(1)

    cheapest = find_cheapest(
        instances,
        args.family,
        args.vcpu,
        args.memory
    )

    if cheapest is None:
        print("No matching instance found.")
        sys.exit(1)

    print("\n========================================")
    print("Lowest-priced EC2 Instance")
    print("========================================")
    print(f"Instance : {cheapest['instance']}")
    print(f"vCPUs    : {cheapest['vcpus']}")
    print(f"Memory   : {cheapest['memory']} GiB")
    print(f"Price    : ${cheapest['price']}/hour")
    print("========================================")


if __name__ == "__main__":
    main()
