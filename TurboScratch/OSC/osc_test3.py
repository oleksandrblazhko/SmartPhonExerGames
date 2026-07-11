from pythonosc import udp_client
import time

# OSC settings (default ChilloutVR)
OSC_IP = "127.0.0.1"
OSC_PORT = 9000

client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

print(f"Sending /input/MoveForward -> True to {OSC_IP}:{OSC_PORT}")
print("Press Ctrl+C to stop.\n")

try:
    while True:
        client.send_message("/input/MoveForward", True)
        print("Sent: /input/MoveForward True")
        time.sleep(0.1)   # 10 messages per second

except KeyboardInterrupt:
    print("\nStopped.")
    