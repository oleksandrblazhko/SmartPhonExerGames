import json
import time

import requests
from pythonoscquery.osc_query_browser import OSCQueryBrowser


def find_input_nodes(node):
    """
    Рекурсивний пошук усіх вузлів /input/*
    """
    full_path = node.get("FULL_PATH", "")

    if full_path.startswith("/input"):
        print(full_path)

    contents = node.get("CONTENTS", {})

    for child in contents.values():
        find_input_nodes(child)


print("Searching OSCQuery server...")

browser = OSCQueryBrowser()

time.sleep(3)

services = browser.get_discovered_oscquery()

if not services:
    print("OSCQuery server not found.")
    exit()

service = services[0]

ip = service.parsed_addresses()[0]
port = service.port

print(f"Server : {service.name}")
print(f"Address: {ip}:{port}")

url = f"http://{ip}:{port}/"

print("Downloading OSC tree...")

response = requests.get(url)

if response.status_code != 200:
    print("HTTP Error:", response.status_code)
    exit()

# ChilloutVR повертає JSON з UTF-8 BOM
tree = json.loads(response.content.decode("utf-8-sig"))

print()
print("========== INPUT COMMANDS ==========")

find_input_nodes(tree)
