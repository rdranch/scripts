from configparser import ConfigParser
from ctypes import windll
from win32api import GetAsyncKeyState, mouse_event
from keyboard import is_pressed, wait
from time import sleep
from os import path, getcwd
from multiprocessing import freeze_support, Process

def configManager(name):
    config = ConfigParser()

    if not path.exists(name):
        config['CONTROLLER'] = {'Vertical':'3', 'Horizontal':'0', 'Rate': '0.005', 'Toggle':'F2'}

        with open("macro.ini", "w") as configfile:
            config.write(configfile)
        print("[*] Config file created in " + getcwd() + ".")
    else:
        config.read("macro.ini")
    
    return config

def printFormat():
    print("[!] Config file incorrectly formatted.")
    print("Format:\n[NAME]\nHorizontal = (some number)\nVertical = (some number)\nRate = (a float/double)\nToggle = (Keyboard button)")
    exit(0)

def recoil(shiftX, shiftY, rate):
    while True:
        if GetAsyncKeyState(1) < 0 and GetAsyncKeyState(2) < 0:
            mouse_event(0x0001, int(shiftX), int(shiftY), 0, 0)
            sleep(float(rate))

if __name__ == "__main__":
    windll.kernel32.SetConsoleTitleW("Global recoil macro coded by Darkon (Darkinator#3932) AKA The.Don_ (v.1.1)")
    freeze_support()
    print("[*] To activate/deactivate, hit toggle key in config file. Rate is how often to pull down. CTRL + C to quit. Changes to config require a restart.")

    name = "macro.ini"

    try:
        config = configManager(name)
        header = config.sections()[0]
        shiftX = config[header]['Horizontal']
        shiftY = config[header]['Vertical']
        rate = config[header]['Rate']
        toggle = config[header]['Toggle']
    except:
        printFormat()

    try:
        while True:
            if is_pressed(toggle):
                print("[*] ACTIVATED") 
                proc = Process(target=recoil, args=(shiftX, shiftY, rate))
                proc.start()
                wait(toggle)
                print("[*] DEACTIVATED") 
                proc.terminate()
                sleep(0.4)

    except KeyboardInterrupt:
        print("[!] Quitting.")
        exit(0)
    except Exception as e:
        print(e)