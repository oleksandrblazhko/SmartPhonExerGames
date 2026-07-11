
# Persona
Раніше ти створив програму - TurboScratch\http2websocket.py
Програма має параметр командного рядку --keys, який дозволяє генерувати натискання клавіш w,s,a,d
Тепер треба адаптувати роботу програми для керування зовнішньою програмою через OSC-команди.

# Tasks
1) додати до програми http2websocket.py параметр командного рядку --osc
2) за параметром реалізувати алгоритм передачі OSC-команд за прикладом передачі сигналів роботи з клавіатурою, який представлено у TurboScratch\key_presser.py
3) алгоритм реалізувати в окремоюу модулі osc_commands.py

# Context
1) OSC-протокол використовує функцію керування командами з однією булєвою змінною:
- вмикання команди - send_message("/input/command", True)
- вимикання команди - send_message("/input/command", False)

2) Приклад програмного коду:

from pythonosc import udp_client
import time

OSC_IP = "127.0.0.1"
OSC_PORT = 9000

client = udp_client.SimpleUDPClient(OSC_IP, OSC_PORT)

## команда руху вперед (клавіша w)
client.send_message("/input/MoveForward", True)
## команда руху назад (клавіша s)
client.send_message("/input/MoveBackward", True)
## команда руху наліво (клавіша a)
client.send_message("/input/MoveLeft", True)
## команда руху направо (клавіша d)
client.send_message("/input/MoveRight", True)


