import win32api, keyboard, multiprocessing, ctypes
from json import dumps, loads
from time import sleep
from os import path, getcwd, startfile
from random import randint, uniform, shuffle
from win32gui import GetWindowText, GetForegroundWindow
from psutil import process_iter

# TODO add randomization to looking around

# Knifing is not dealt with
default_config = {
    "toggle":"f2",
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

def macro(config, path):
    '''Main macro script which will run a series of actions found in the config file to automatically move.
    Will infinitely run until forced shut or process is terminated.

    Arguments
    ---------
    Config : Dictionary
        Key/action mapping
    Path : string
        The path of R6 executable
    '''
    
    # Checks if Rainbow Six is open, will restart it if not.
    while True:
        while "RainbowSix.exe" not in [p.name() for p in process_iter()]:
            print("[!] Siege crashed or closed. Stopping bot while it restarts.")
            startfile(path)
            sleep(120)
            print("[*] Continuing...")
            keyboard.press('enter')
            sleep(0.03)
            keyboard.release('enter')

        # Shuffles order in which actions are done
        random_list = ["reload", "up", "left", "down", "right", "crouch"]
        shuffle(random_list)

        # Main activity section
        keyboard.press(config[random_list[0]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[0]])
        sleep(uniform(0.3, 1))
        keyboard.press(config[random_list[1]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[1]])
        sleep(uniform(0.3, 1))
        keyboard.press(config[random_list[2]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[2]])
        sleep(uniform(0.3, 1))
        keyboard.press(config[random_list[3]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[3]])
        sleep(uniform(0.3, 1))
        keyboard.press(config[random_list[4]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[4]])
        sleep(uniform(0.3, 1))
        keyboard.press(config[random_list[5]])
        sleep(uniform(0.3, 1))
        keyboard.release(config[random_list[5]])
        sleep(uniform(0.3, 1))
        keyboard.press(config["lean_left"])
        sleep(uniform(0.3, 1))
        keyboard.release(config["lean_left"])
        sleep(uniform(0.3, 1))
        keyboard.press(config["lean_right"])
        sleep(uniform(0.3, 1))
        keyboard.release(config["lean_right"])
        sleep(uniform(0.3, 1))
        keyboard.press(config["lean_right"])
        sleep(uniform(0.3, 1))
        keyboard.release(config["lean_right"])
        sleep(uniform(0.3, 1))

        # ADS/UNAds
        for _ in range(2):
            win32api.mouse_event(0x0008, 0, 0, 0, 0) # Right click press
            sleep(uniform(0.3, 1))
            win32api.mouse_event(0x0010, 0, 0, 0, 0) # Right click release
            sleep(uniform(0.3, 1))

        # Sit down / stand up
        for _ in range(2):
            keyboard.press(config["prone"])
            sleep(uniform(0.3, 1))
            keyboard.release(config["prone"])
            sleep(uniform(0.5, 1))
        
        # Drop/pickup bomb, ping
        keyboard.press(config["interact"])
        sleep(uniform(0.3, 1))
        keyboard.release(config["interact"])
        sleep(uniform(0.3, 1))
        keyboard.press(config["ping"])
        sleep(uniform(0.3, 1))
        keyboard.release(config["ping"])
        sleep(uniform(0.3, 1))
        
        # Pull/put out gadget
        keyboard.press(config["gadget"])
        sleep(uniform(0.6, 1))
        win32api.mouse_event(0x0800, 0, 0, 120, 0) # SCROLL UP - ONE WHEEL CLICK IS 120
        keyboard.release(config["gadget"])
        sleep(1.5)

        win32api.mouse_event(0x0001, 0, -1000, 0, 0) # Moves cursor to top of screen
        sleep(0.5)

        win32api.mouse_event(0x0002, 0, 0, 0, 0) # Left click press
        sleep(uniform(0.3, 1))
        win32api.mouse_event(0x0004, 0, 0, 0, 0) # Left click release
        sleep(uniform(0.3, 1))

        win32api.mouse_event(0x0020, 0, 0, 0, 0) # Middle click press
        sleep(uniform(0.3, 1))
        win32api.mouse_event(0x0040, 0, 0, 0, 0) # Middle click release
        sleep(uniform(0.3, 1))

        win32api.mouse_event(0x0001, 0, cy, 0 ,0) # Centers crosshair
        keyboard.press('enter')
        sleep(uniform(0.3, 1))
        keyboard.press('enter')
        sleep(0.03)
        keyboard.release('enter')
        sleep(uniform(0.3, 1))
        keyboard.release('enter')
        sleep(0.03)

        # Spin 4x to the right
        for _ in range(4):
            win32api.mouse_event(0x0001, cx//4, 0, 0, 0)
            sleep(uniform(0.3, 1))

        keyboard.press('esc')
        sleep(uniform(0.3, 1))
        keyboard.release('esc')
        sleep(0.03)
        keyboard.press('esc')
        sleep(0.03)
        keyboard.release('esc')
        sleep(uniform(0.3, 1))

    
def check_open():
    '''Checks all process names to see if RainbowSix is open
    If R6 is found, it will return the path.

    Returns
    -------
    String : executable path
    '''
    print("[*] Waiting for Rainbow Six to be opened.")
    while "RainbowSix.exe" not in [p.name() for p in process_iter()]:
        sleep(2)
    
    for proc in process_iter():
        if proc.name() == "RainbowSix.exe":
            return proc.exe()


if __name__ == "__main__":
    # Create title for exe
    ctypes.windll.kernel32.SetConsoleTitleW("Bot coded by Darkon (Darkinator#3932) AKA The.Don_ (v.1.0)")
    multiprocessing.freeze_support()

    # Check if config file is created
    if not path.exists("botSettings.ini"):   
        with open("botSettings.ini", "w") as f:
            f.write(dumps(default_config, indent=4))
            print(f"[*] botSettings.ini created in {getcwd()}")
            config = default_config
    else:
        with open("botSettings.ini", "r") as f:
            config = loads(f.read())
    toggle = config['toggle']

    # Run bot
    try:
        path = check_open()
        print(f"[*] Press {toggle} to activate/deactive bot. CTRL+C to EXIT.") 
        while True:
            if keyboard.is_pressed(toggle):
                print("[*] BOT ACTIVATED") 
                proc = multiprocessing.Process(target=macro, args=(config, path))
                proc.start()
                keyboard.wait(toggle)
                print("[*] BOT DEACTIVATED") 
                proc.terminate()
                sleep(0.5)
    except KeyboardInterrupt:
        print("[*] EXITING")
        exit(0)
