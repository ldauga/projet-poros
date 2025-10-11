import json
import sys
import threading
import time
from system.lib.minescript import EventQueue, EventType, container_get_items, execute, player_inventory, player_inventory_slot_to_hotbar, player_look_at
import pyautogui




check = True
STOP_KEY = 333

POS_FACILE = (850, 411)
POS_MEDIUM = (905, 411)
POS_HARD = (1015, 411)
POS_VERY_HARD = (1070, 411)


CHEST_CULTURES = (-32 + .5, -57 + .5, -2 + .5)
CHEST_MINERAIS = (-32 + .5, -57 + .5, -4 + .5)
NONE_BLOCK = (-32 + .5, -57 + .5, -3 + .5)



SLOTS = {
    0: {"x": 750, "y": 800},
    1: {"x": 800, "y": 800},
    2: {"x": 850, "y": 800},
    3: {"x": 900, "y": 800},
    4: {"x": 950, "y": 800},
    5: {"x": 1000, "y": 800},
    6: {"x": 1050, "y": 800},
    7: {"x": 1100, "y": 800},
    8: {"x": 1150, "y": 800},
}

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            event = event_queue.get()
            if event.type == EventType.KEY and event.action == 1:  # key down
                if event.key == STOP_KEY:
                    stop_event.set()
                    break
                


        
def main(stop_event: threading.Event):
    
    
    if len(sys.argv) < 2:
        print("Usage: \\q <quest_type>")
        return
    else:
        
        
        input_arg = " ".join(sys.argv[1:])
        
        if input_arg not in ["easy", "medium", "hard", "very hard"]:
            print("Usage: \\q <quest_type>")
            return
        else:
            if input_arg == "easy":
                parchemin_pos = POS_FACILE
            if input_arg == "medium":
                parchemin_pos = POS_MEDIUM
            if input_arg == "hard":
                parchemin_pos = POS_HARD
            if input_arg == "very hard":
                parchemin_pos = POS_VERY_HARD
    
    parchemins = [1]
    
    try:
        while not stop_event.is_set() and len(parchemins):

            player_look_at(*NONE_BLOCK)

            execute("/c")

            time.sleep(0.3)
            
            if stop_event.is_set():
                return

            pyautogui.moveTo(*parchemin_pos)
            for _ in range(8):
                pyautogui.click()
                time.sleep(0.1)
                if stop_event.is_set():
                    return

            pyautogui.press("Escape")

            for i in range(1, 10):
                pyautogui.press(str(i))
                pyautogui.click(button="secondary", duration=0.1)

            inv = player_inventory()
            
            parchemins = [item for item in inv if ("Challenge" in json.dumps(item.__dict__))]
            
            player_look_at(*CHEST_MINERAIS)
            pyautogui.click(button="secondary")
            
            pyautogui.keyDown('shift')
            
            for item in parchemins:
                if "minerais" in json.dumps(item.__dict__):
                    pyautogui.moveTo(**SLOTS[item.slot], duration=0)
                    pyautogui.click(duration=0)
                    
                    if stop_event.is_set():
                        return

            
            pyautogui.keyUp('shift')
            pyautogui.press("Escape")
            
            player_look_at(*CHEST_CULTURES)

            pyautogui.click(button="secondary")
            
            pyautogui.keyDown('shift')
            
            for item in parchemins:
                if "cultures" in json.dumps(item.__dict__):
                    
                    pyautogui.moveTo(**SLOTS[item.slot], duration=0)
                    pyautogui.click(duration=0)
                    if stop_event.is_set():
                        return

            pyautogui.keyUp('shift')

            pyautogui.press("Escape")

            
            
            if len(parchemins) < 8:
                return
    finally:
        pyautogui.keyUp('shift')




if __name__ == "__main__":
    stop_event = threading.Event()

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)
    # t3 = threading.Thread(target=avast, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()
    # t3.start()

    # Optionally wait for threads to finish
    t1.join()
    t2.join()
    # t3.join()