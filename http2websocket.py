import asyncio
import json
import math
import websockets
import aiohttp
import threading
import time
import keyboard
import numpy as np
import os
import signal
import winsound

# --- Глобальні змінні та налаштування ---

# Змінні для калібрування
delta_accX = 0.0
delta_accY = 0.0

# Стан калібрування
class CalibrationState:
    IDLE = 0
    CALIBRATING = 1
    DONE = 2

calibration_state = CalibrationState.IDLE
calibration_data = []

# Множина для зберігання всіх підключених клієнтів WebSocket
CONNECTED_CLIENTS = set()

# Словник для зберігання останніх даних з сенсорів, включаючи розраховані кути
SENSOR_DATA = {
    "accX": 0,
    "accY": 0,
    "angle_x": 0,
    "angle_y": 0
}

# Базова частина IP-адреси
BASE_IP = "192.168.0."
DEFAULT_PORT = 8080

# URL-адреса HTTP-сервера, звідки беруться дані (буде встановлена після пошуку)
HTTP_SERVER_URL = None

# Коефіцієнт масштабування для перетворення значень акселерометра в кути
SCALING_FACTOR = 7.1

# Коефіцієнт згладжування для фільтра (EMA)
# 0.2 = сильне згладжування, 0.8 = слабке згладжування
ALPHA = 0.3

# Фільтровані значення
filtered_accX = 0.0
filtered_accY = 0.0

# Файл конфігурації
CONFIG_FILE = "config.json"

def clamp(value, min_val, max_val):
    """Допоміжна функція, що обмежує значення в заданому діапазоні [min_val, max_val]."""
    return max(min_val, min(value, max_val))

def load_config():
    """
    Завантажує конфігурацію з файлу.
    Повертає збережену IP-адресу або None.
    """
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                saved_ip = config.get("server_ip")
                if saved_ip:
                    print(f"Завантажено збережену адресу: {saved_ip}")
                    return saved_ip
        except (json.JSONDecodeError, IOError) as e:
            print(f"Помилка читання конфігурації: {e}")
    return None

def save_config(ip_address):
    """
    Зберігає IP-адресу сервера у файл конфігурації.
    """
    try:
        config = {"server_ip": ip_address}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Адресу збережено: {ip_address}")
    except IOError as e:
        print(f"Помилка запису конфігурації: {e}")

async def check_server_available(session, ip_address):
    """
    Перевіряє доступність HTTP-сервера за вказаною IP-адресою.
    Повертає True, якщо сервер доступний і повертає коректні дані.
    """
    url = f"http://{ip_address}:{DEFAULT_PORT}/get?accX&accY"
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=2)) as response:
            if response.status == 200:
                data = await response.json()
                # Перевіряємо, чи є дані в буфері (не null)
                accX = data.get("buffer", {}).get("accX", {}).get("buffer", [None])[0]
                accY = data.get("buffer", {}).get("accY", {}).get("buffer", [None])[0]
                if accX is not None and accY is not None:
                    return True, url
    except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError, KeyError):
        pass
    return False, None

async def find_server():
    """
    Шукає доступний HTTP-сервер, перевіряючи діапазони адрес 100-103 та 160-163.
    Повертає URL знайденого сервера або None, якщо сервер не знайдено.
    """
    async with aiohttp.ClientSession() as session:
        # Перший діапазон: 100-110
        print("Пошук сервера в діапазоні 192.168.0.100-103...")
        for i in range(100, 103):
            ip = f"{BASE_IP}{i}"
            available, url = await check_server_available(session, ip)
            if available:
                print(f"Знайдено сервер: {url}")
                return url
        
        # Другий діапазон: 161-170
        print("Пошук сервера в діапазоні 192.168.0.160-163...")
        for i in range(160, 163):
            ip = f"{BASE_IP}{i}"
            available, url = await check_server_available(session, ip)
            if available:
                print(f"Знайдено сервер: {url}")
                return url
    
    return None

def get_user_ip():
    """
    Запитує у користувача власне значення IP-адреси.
    """
    while True:
        try:
            user_input = input("Введіть останнє число IP-адреси (наприклад, 111 або 165): ")
            last_octet = int(user_input)
            if 1 <= last_octet <= 254:
                url = f"http://{BASE_IP}{last_octet}:{DEFAULT_PORT}/get?accX&accY"
                print(f"Використовується адреса: {url}")
                return url
            else:
                print("Число має бути в діапазоні від 1 до 254.")
        except ValueError:
            print("Будь ласка, введіть коректне число.")

async def register_client(websocket):
    """
    Реєструє нового клієнта, що підключився, 
    і утримує з'єднання відкритим до його закриття.
    """
    CONNECTED_CLIENTS.add(websocket)
    print(f"Новий клієнт підключився. Всього клієнтів: {len(CONNECTED_CLIENTS)}")
    try:
        # Очікуємо, поки клієнт не від'єднається
        await websocket.wait_closed()
    finally:
        # Видаляємо клієнта з множини після від'єднання
        CONNECTED_CLIENTS.remove(websocket)
        print(f"Клієнт від'єднався. Всього клієнтів: {len(CONNECTED_CLIENTS)}")

async def data_loop():
    """
    Головний цикл програми: періодично запитує дані з HTTP-сервера,
    обчислює кути нахилу та транслює їх усім підключеним клієнтам.
    """
    global calibration_state, delta_accX, delta_accY, calibration_data, filtered_accX, filtered_accY

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(HTTP_SERVER_URL) as response:
                    if response.status == 200:
                        data = await response.json()
                        accX = data.get("buffer", {}).get("accX", {}).get("buffer", [0])[0]
                        accY = data.get("buffer", {}).get("accY", {}).get("buffer", [0])[0]

                        if calibration_state == CalibrationState.CALIBRATING:
                            calibration_data.append((accX, accY))
                            continue

                        if calibration_state == CalibrationState.DONE:
                            accX -= delta_accX
                            accY -= delta_accY

                        # Застосовуємо фільтр низьких частот (EMA)
                        filtered_accX = ALPHA * accX + (1 - ALPHA) * filtered_accX
                        filtered_accY = ALPHA * accY + (1 - ALPHA) * filtered_accY

                        ratio_x = clamp(filtered_accX / SCALING_FACTOR, -1.0, 1.0)
                        ratio_y = clamp(filtered_accY / SCALING_FACTOR, -1.0, 1.0)

                        angle_x = math.degrees(math.asin(ratio_x))
                        angle_y = math.degrees(math.asin(ratio_y))

                        SENSOR_DATA.update({
                            "accX": filtered_accX, "accY": filtered_accY,
                            "angle_x": angle_x, "angle_y": angle_y
                        })
                    else:
                        print(f"Помилка отримання даних: HTTP {response.status}")
            except aiohttp.ClientError as e:
                print(f"Помилка підключення до HTTP-сервера: {e}")
            except json.JSONDecodeError:
                print("Помилка: не вдалося розкодувати JSON.")

            if CONNECTED_CLIENTS:
                message = json.dumps({
                    "accX": SENSOR_DATA["accX"],
                    "accY": SENSOR_DATA["accY"]
                })
                # Використовуємо gather з return_exceptions=True, щоб уникнути падіння циклу,
                # якщо один з клієнтів від'єднався.
                await asyncio.gather(*[client.send(message) for client in CONNECTED_CLIENTS], return_exceptions=True)

            await asyncio.sleep(0.05)  # 20 Гц

def calibration_thread():
    """
    Потік для виконання калібрування.
    """
    global calibration_state, delta_accX, delta_accY, calibration_data
    
    print("Режим калібрування. Тримайте смартфон у стані спокою впродовж 5 секунд")
    calibration_data = []
    calibration_state = CalibrationState.CALIBRATING
    
    for i in range(3, -1, -1):
        if i == 0:
            print(f"{i} .......")
            winsound.Beep(1000, 700)
        else:
            print(f"{i} ...")
            winsound.Beep(1000, 200)
        time.sleep(1)
        
    if calibration_data:
        accX_data, accY_data = zip(*calibration_data)
        delta_accX = np.mean(accX_data)
        delta_accY = np.mean(accY_data)
        print(f"Калібрування завершено: delta_accX={delta_accX:.2f}, delta_accY={delta_accY:.2f}")
    else:
        print("Не вдалося отримати дані для калібрування.")

    calibration_state = CalibrationState.DONE

import os
import signal

def input_handler():
    """
    Обробник введення з клавіатури для керування програмою.
    """
    global calibration_state
    
    while True:
        key = keyboard.read_key()
        if key == 'c' or key == 'C':
            if calibration_state != CalibrationState.CALIBRATING:
                cal_thread = threading.Thread(target=calibration_thread)
                cal_thread.start()
        elif key == 'q' or key == 'Q':
            print("Завершення роботи...")
            os.kill(os.getpid(), signal.SIGINT)
            break
        time.sleep(0.1)


async def main_async():
    """Основна функція, яка запускає WebSocket-сервер та цикл обробки даних."""
    global HTTP_SERVER_URL
    
    # Спроба завантажити збережену адресу з конфігурації
    print("Перевірка доступності HTTP-сервера...")
    saved_ip = load_config()
    
    server_url = None
    
    # Спершу перевіряємо збережену адресу
    if saved_ip:
        print(f"Перевірка збереженої адреси: {saved_ip}...")
        async with aiohttp.ClientSession() as session:
            available, url = await check_server_available(session, saved_ip)
            if available:
                print(f"Знайдено сервер за збереженою адресою: {url}")
                server_url = url
            else:
                print("Збережена адреса недоступна. Пошук нового сервера...")
    
    # Якщо збережена адреса не працює, шукаємо сервер
    if server_url is None:
        server_url = await find_server()
    
    # Якщо сервер не знайдено, запитуємо адресу у користувача
    if server_url is None:
        print("\nНе вдалося знайти сервер у діапазонах 192.168.0.100-110 та 192.168.0.161-170.")
        print("Будь ласка, введіть адресу сервера вручну.")
        server_url = get_user_ip()
    
    # Зберігаємо робочу адресу в конфігурацію
    # Витягуємо IP з URL для збереження
    ip_to_save = server_url.split("//")[1].split(":")[0]
    save_config(ip_to_save)
    
    HTTP_SERVER_URL = server_url
    print(f"Підключення до сервера: {HTTP_SERVER_URL}")
    
    server = await websockets.serve(register_client, "localhost", 8767)
    data_task = asyncio.create_task(data_loop())

    print("WebSocket-сервер запущено на ws://localhost:8767")
    print("Клавіші керування: C - калібрування стану спокою, Q - завершення роботи")
    
    try:
        await data_task
    except asyncio.CancelledError:
        pass
    finally:
        server.close()
        await server.wait_closed()

def main():
    global HTTP_SERVER_URL
    
    input_thread = threading.Thread(target=input_handler)
    input_thread.daemon = True
    input_thread.start()
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_async())
    except KeyboardInterrupt:
        print("\nПрограму зупинено.")
    finally:
        tasks = asyncio.all_tasks(loop=loop)
        for task in tasks:
            task.cancel()
        
        # Збираємо всі задачі, щоб вони завершилися з CancelledError
        group = asyncio.gather(*tasks, return_exceptions=True)
        loop.run_until_complete(group)
        loop.close()


# Точка входу в програму
if __name__ == "__main__":
    main()
