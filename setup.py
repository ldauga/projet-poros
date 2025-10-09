from system.lib.minescript import EventQueue, EventType
import pyautogui


check = True
STOP_KEY = 333

with EventQueue() as event_queue:
    event_queue.register_key_listener()
    print("oui")
    while check:
        event = event_queue.get()

        if event.type == EventType.KEY and event.action == 1:
            if event.key == STOP_KEY:
                check = False
                break
        
        x, y = pyautogui.position()
        print(f"Position de la souris : ({x}, {y})")