import json
import time

import requests
from pythonoscquery.osc_query_browser import OSCQueryBrowser


def print_input_nodes(node):
    """
    Рекурсивно друкує всю інформацію про вузли /input/*
    """

    path = node.get("FULL_PATH", "")

    if path.startswith("/input"):

        print("=" * 80)
        print(path)

        # показати ВСІ поля, які повернув сервер
        for key, value in node.items():

            if key == "CONTENTS":
                continue

            print(f"{key:15}: {value}")

        print()

    contents = node.get("CONTENTS", {})

    for child in contents.values():
        print_input_nodes(child)


# --------------------------------------------------

print("Searching OSCQuery server...")

browser = OSCQueryBrowser()

time.sleep(3)

services = browser.get_discovered_oscquery()

if not services:
    print("OSCQuery server not found.")
    quit()

service = services[0]

ip = service.parsed_addresses()[0]
port = service.port

print(f"Server : {service.name}")
print(f"Address: {ip}:{port}")

url = f"http://{ip}:{port}/"

print(f"Connecting to {url}")

response = requests.get(url)

tree = json.loads(
    response.content.decode("utf-8-sig")
)

print()
print("INPUT COMMANDS")
print()

print_input_nodes(tree)
