import requests

url = "http://127.0.0.1:63213/"

r = requests.get(url)

print("Status:", r.status_code)
print("Headers:", r.headers)
print("First 20 bytes:", r.content[:20])
print()
print(r.text[:500])
