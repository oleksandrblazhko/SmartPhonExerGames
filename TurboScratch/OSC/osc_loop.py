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
        time.sleep(1)
        client.send_message("/input/MoveForward", False)
        print("Sent: /input/MoveForward False")
        client.send_message("/input/MoveBackward", True)
        print("Sent: /input/MoveBackward True")
        time.sleep(1)
        client.send_message("/input/MoveBackward", False)
        print("Sent: /input/MoveBackward False")


except KeyboardInterrupt:
    print("\nStopped.")
    