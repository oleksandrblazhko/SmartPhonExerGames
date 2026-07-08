import pydirectinput

def press_keys(accX, accY, offset_accX, offset_accY, threshold=0.5):
    """
    Натискає клавіші в залежності від значень accX, accY та їх відхилень.
    Використовує поріг для уникнення хибних спрацьовувань.
    """
    # X-axis control
    if accX > offset_accX + threshold:
        pydirectinput.keyDown('a')
        pydirectinput.keyUp('d')
    elif accX < offset_accX - threshold:
        pydirectinput.keyDown('d')
        pydirectinput.keyUp('a')
    else:
        pydirectinput.keyUp('a')
        pydirectinput.keyUp('d')

    # Y-axis control
    if accY > offset_accY + threshold:
        pydirectinput.keyDown('s')
        pydirectinput.keyUp('w')
    elif accY < offset_accY - threshold:
        pydirectinput.keyDown('w')
        pydirectinput.keyUp('s')
    else:
        pydirectinput.keyUp('s')
        pydirectinput.keyUp('w')

