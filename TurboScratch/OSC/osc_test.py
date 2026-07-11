from pythonoscquery.osc_query_browser import OSCQueryBrowser
import time

browser = OSCQueryBrowser()

print("Searching...")
time.sleep(3)

services = browser.get_discovered_oscquery()

service = services[0]

print(type(service))
print()

print(dir(service))
print()

print(service)
