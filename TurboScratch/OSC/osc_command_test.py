import json
import time

import requests
from pythonosc import udp_client
from pythonoscquery.osc_query_browser import OSCQueryBrowser


def collect_inputs(node, commands):
    """Збирає всі команди /input/*"""

    path = node.get("FULL_PATH", "")

    if path.startswith("/input/") and path != "/input":
        commands.append({
            "path": path,
            "type": node.get("TYPE", "")
        })

    for child in node.get("CONTENTS", {}).values():
        collect_inputs(child, commands)


print("Searching OSCQuery server...")

browser = OSCQueryBrowser()

time.sleep(2)

services = browser.get_discovered_oscquery()

if not services:
    print("OSCQuery server not found.")
    exit()

service = services[0]

ip = "127.0.0.1"

osc_port = 63213

client = udp_client.SimpleUDPClient(ip, osc_port)

url = f"http://{ip}:{service.port}"

response = requests.get(url)

tree = json.loads(response.content.decode("utf-8-sig"))

commands = []

collect_inputs(tree, commands)

print("\n========== INPUT COMMANDS ==========\n")

for i, cmd in enumerate(commands, 1):
    print(f"{i:2d}. {cmd['path']}    ({cmd['type']})")

print()

while True:

    s = input("\nSelect command (q=quit): ")

    if s.lower() == "q":
        break

    try:
        index = int(s) - 1
        cmd = commands[index]
    except:
        print("Wrong number.")
        continue

    path = cmd["path"]
    typ = cmd["type"]

    print("\nSelected:", path)
    print("Type:", typ)

    try:

        if typ == "T":
            value = input("Text: ")

        elif typ == "i":
            value = int(input("Integer: "))

        elif typ == "f":
            value = float(input("Float: "))

        elif typ == "b":
            value = bool(int(input("Bool (0/1): ")))

        else:
            value = float(input("Value: "))

        client.send_message(path, value)

        print("Message sent:")
        print(path, value)

    except Exception as e:
        print(e)
