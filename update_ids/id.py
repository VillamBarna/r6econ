import pyautogui
import time
width , height = pyautogui.size()

def copy():
    pyautogui.click(478,64)
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.click(3000,80)
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.click(16,128)
    time.sleep(0.15)

pyautogui.click(1600, 1410) 

for z in range(13):
    for n in range(10):
        for i in range(4):
            pyautogui.click(width/2.3+100*i, height/6.85+130*n)
            time.sleep(0.2)
            copy()

    pyautogui.click(1800,480)
    pyautogui.scroll(-400)
    time.sleep(0.5)
    pyautogui.click(1440,1280)
    time.sleep(1)
