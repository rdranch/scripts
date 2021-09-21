import win32api, keyboard, multiprocessing, ctypes
from json import dumps, loads
from time import sleep
from os import path

# Knifing is not dealt with
default_config = {
    "reload":"r",
    "up":"w",
    "lean_left":"q",
    "lean_right":"e",
    "left":"a",
    "down":"s",
    "right":"d",
    "crouch":"z",
    "prone":"left ctrl",
    "interact":"f",
    "ping":"v",
    "gadget":"`",
}

cx = win32api.GetSystemMetrics(0) # Get screen width
cy = win32api.GetSystemMetrics(1) // 2 # Get screen height

def macro(): 
    if not path.exists("botSettings.ini"):   
        with open("botSettings.ini", "w") as f:
            f.write(dumps(default_config, indent=4))
            config = default_config
    else:
        with open("botSettings.ini", "r") as f:
            config = loads(f.read())

    while True:
        # Reload --> Up --> Lean left --> Lean Right --> Straighten out --> Left --> Down --> Right --> Crouch 
        keyboard.press(config["reload"])
        sleep(0.3)
        keyboard.release(config["reload"])
        sleep(0.3)
        keyboard.press(config["up"])
        sleep(0.3)
        keyboard.release(config["up"])
        sleep(0.3)
        keyboard.press(config["lean_left"])
        sleep(0.3)
        keyboard.release(config["lean_left"])
        sleep(0.3)
        keyboard.press(config["lean_right"])
        sleep(0.3)
        keyboard.release(config["lean_right"])
        sleep(0.3)
        keyboard.press(config["lean_right"])
        sleep(0.3)
        keyboard.release(config["lean_right"])
        sleep(0.3)
        keyboard.press(config["left"])
        sleep(0.3)
        keyboard.release(config["left"])
        sleep(0.3)
        keyboard.press(config["down"])
        sleep(0.3)
        keyboard.release(config["down"])
        sleep(0.3)
        keyboard.press(config["right"])
        sleep(0.3)
        keyboard.release(config["right"])
        sleep(0.3)
        keyboard.press(config["crouch"])
        sleep(0.3)
        keyboard.release(config["crouch"])
        sleep(0.3)

        # ADS/UNAds
        for _ in range(2):
            win32api.mouse_event(0x0008, 0, 0, 0, 0) # Right click press
            sleep(0.3)
            win32api.mouse_event(0x0010, 0, 0, 0, 0) # Right click release
            sleep(0.3)

        # Sit down / stand up
        for _ in range(2):
            keyboard.press(config["prone"])
            sleep(0.3)
            keyboard.release(config["prone"])
            sleep(0.5)
        
        # Drop/pickup bomb, ping
        keyboard.press(config["interact"])
        sleep(0.3)
        keyboard.release(config["interact"])
        sleep(0.3)
        keyboard.press(config["ping"])
        sleep(0.3)
        keyboard.release(config["ping"])
        sleep(0.3)
        
        # Pull/put out gadget
        keyboard.press(config["gadget"])
        sleep(0.3)
        win32api.mouse_event(0x0800, 0, 0, 120, 0) # SCROLL UP - ONE WHEEL CLICK IS 120
        keyboard.release(config["gadget"])
        sleep(1.0)

        win32api.mouse_event(0x0001, 0, -1000, 0, 0) # Moves cursor to top of screen
        sleep(0.5)

        win32api.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
        sleep(0.3)
        win32api.mouse_event(0x0004, 0, 0, 0, 0) # Left click release
        sleep(0.3)

        win32api.mouse_event(0x0020, 0, 0, 0, 0) # Middle click press
        sleep(0.3)
        win32api.mouse_event(0x0040, 0, 0, 0, 0) # Middle click release
        sleep(0.3)

        win32api.mouse_event(0x0001, 0, cy, 0 ,0) # Centers crosshair
        keyboard.press('enter')
        sleep(0.3)
        keyboard.press('enter')
        sleep(0.03)
        keyboard.release('enter')
        sleep(0.3)
        keyboard.release('enter')
        sleep(0.03)

        # Spin 4x to the right
        for _ in range(4):
            x, y = win32api.GetCursorPos()
            win32api.mouse_event(0x0001, cx//4, 0, 0, 0)
            sleep(0.3)

        keyboard.press('esc')
        sleep(0.3)
        keyboard.release('esc')
        sleep(0.03)
        keyboard.press('esc')
        sleep(0.03)
        keyboard.release('esc')
        sleep(0.3)
    

if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("Bot coded by Darkon (Darkinator#3932) AKA The.Don_ (v.0.1)")
    multiprocessing.freeze_support()
    try:
        while True:
            # Start macro bot
            print("[*] Press F2 to activate/deactive bot. CTRL+C to EXIT.") 
            keyboard.wait('f2')
            print("[*] BOT ACTIVATED") 
            proc = multiprocessing.Process(target=macro, args=())
            proc.start()

            # End macro bot
            keyboard.wait('f2')
            proc.terminate()
            print("[*] BOT DEACTIVATED") 
    except KeyboardInterrupt:
        print("[*] EXITING")
        exit(0)