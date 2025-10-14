




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
    
    pyautogui.doubleClick(*POS_1)
    pyautogui.click(*TRASH_POS_1)
    pyautogui.doubleClick(*POS_2)
    pyautogui.click(*TRASH_POS_2)
    pyautogui.doubleClick(*POS_3)
    pyautogui.click(*TRASH_POS_3)
    pyautogui.press("Escape")
    
    
    
    
    execute("/shop")
    
    
    sleep(.2)
    pyautogui.click(*SHOP_DIVERS_POS)
    sleep(.2)
    
    
    for _ in range(4):
        pyautogui.click(*LAVA_ITEM_POS)
        sleep(.2)
        pyautogui.click(*BUY_MORE_POS)
        sleep(.2)
        pyautogui.click(*BUY_NINE_POS)
        sleep(.2)
    
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