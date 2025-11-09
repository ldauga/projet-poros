




from time import sleep
import pyautogui
from system.lib.minescript import execute

POS_1 = (744, 636)
POS_2 = (743, 742)
POS_3 = (1017, 811)

TRASH_POS_1 = (745, 274)
TRASH_POS_2 = (797, 274)
TRASH_POS_3 = (853, 275)

SHOP_DIVERS_POS = (1067, 380)

LAVA_ITEM_POS = (854, 279)

BUY_MORE_POS = (954, 538)

BUY_NINE_POS = (1179, 270)

def trash_inv():
    # try:
    execute("/trash")
    sleep(.1)
    
    pyautogui.moveTo(*POS_1)
    pyautogui.doubleClick()
    sleep(.1)
    pyautogui.moveTo(*TRASH_POS_1)
    sleep(.1)
    pyautogui.click()
    sleep(.1)
    pyautogui.moveTo(*POS_2)
    pyautogui.doubleClick()
    sleep(.1)
    pyautogui.moveTo(*TRASH_POS_2)
    sleep(.1)
    pyautogui.click()
    sleep(.1)
    pyautogui.moveTo(*POS_3)
    pyautogui.doubleClick()
    sleep(.1)
    pyautogui.moveTo(*TRASH_POS_3)
    sleep(.1)
    pyautogui.click()
    pyautogui.press("Escape")
    
    
    
    
    execute("/shop")
    
    
    sleep(.1)
    pyautogui.moveTo(*SHOP_DIVERS_POS)
    sleep(.1)
    pyautogui.click()
    
    
    for _ in range(4):
        sleep(.1)
        pyautogui.moveTo(*LAVA_ITEM_POS)
        sleep(.1)
        pyautogui.click()
        sleep(.1)
        pyautogui.moveTo(*BUY_MORE_POS)
        sleep(.1)
        pyautogui.click()
        sleep(.1)
        pyautogui.moveTo(*BUY_NINE_POS)
        sleep(.1)
        pyautogui.click()
    
    pyautogui.press("Escape")
    
    
    
    
    
    
    
    #     pyautogui.keyDown("shift")
    #     pyautogui.mouseDown()
    #     sleep(.1)
        
        
    #     for row_index in range(1, 5):
    #         pyautogui.moveTo(*ROWS_POS[row_index]["start"], duration=.1)
    #         pyautogui.moveTo(*ROWS_POS[row_index]["end"], duration=.4)
            
        
    # finally:
    #     pyautogui.keyUp("shift")
    #     pyautogui.mouseUp()


trash_inv()