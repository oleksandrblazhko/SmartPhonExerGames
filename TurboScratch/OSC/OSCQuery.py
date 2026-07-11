"""
OSCQuery Browser for ChilloutVR

Install:

pip install python-oscquery zeroconf

"""

import time

from pythonoscquery.osc_query_browser import OSCQueryBrowser
from pythonoscquery.osc_query_client import OSCQueryClient


# ---------------------------------------------------------
# Pretty print one node
# ---------------------------------------------------------

def print_node(node, file=None):

    print("-" * 70, file=file)

    print(f"Path        : {node.full_path}", file=file)

    try:
        print(f"Description : {node.description}", file=file)
    except Exception:
        pass

    try:
        print(f"Access      : {node.access}", file=file)
    except Exception:
        pass

    try:
        print(f"Type        : {node.type}", file=file)
    except Exception:
        pass

    try:
        print(f"Value       : {node.value}", file=file)
    except Exception:
        pass

    try:
        print(f"Container   : {node.is_container}", file=file)
    except Exception:
        pass


# ---------------------------------------------------------
# Recursive tree walk
# ---------------------------------------------------------

def walk(node, file=None):

    print_node(node, file)

    if hasattr(node, "children"):

        for child in node.children.values():

            walk(child, file)


# ---------------------------------------------------------
# Find all /input/*
# ---------------------------------------------------------

def collect_inputs(node, result):

    if node.full_path.startswith("/input"):

        result.append(node)

    if hasattr(node, "children"):

        for child in node.children.values():

            collect_inputs(child, result)


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

print()

print("Searching OSCQuery services...")

browser = OSCQueryBrowser()

time.sleep(3)

services = browser.get_discovered_oscquery()

if len(services) == 0:

    print("No OSCQuery services found.")

    exit()

print()

print("Found services:")

for i, service in enumerate(services):

    print(f"[{i}] {service.name}")

print()

index = int(input("Select service number: "))

service = services[index]

client = OSCQueryClient(service)

print()

print("Connecting...")

# root = client.query_node("/")

import requests

url = f"http://{service.ip}:{service.port}/"

r = requests.get(url)

print(r.status_code)

print(r.content[:100])

print(r.text[:300])


print("Connected!")

print()

# ---------------------------------------------------------
# Save entire tree
# ---------------------------------------------------------

with open("osc_tree.txt", "w", encoding="utf8") as f:

    walk(root, f)

print("Tree saved to osc_tree.txt")

# ---------------------------------------------------------
# Show INPUT commands
# ---------------------------------------------------------

inputs = []

collect_inputs(root, inputs)

print()

print("=" * 70)

print("INPUT COMMANDS")

print("=" * 70)

for node in inputs:

    print(node.full_path)

print()

print(f"Found {len(inputs)} input commands.")
