










import threading
from time import sleep

from pyautogui import click, moveTo

from constant.command import PETS
from constant.pets import POS_BY_SLOTS_MY_PETS, POS_BY_SLOTS_STORED_PETS
from system.lib.minescript import EventQueue, EventType, execute


STOP_KEY = 333

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:
                if ev.key == STOP_KEY:
                    print("Stopping")
                    stop_event.set()
                    break


def main(stop_event):
    while not stop_event.is_set():
        click(button="secondary")
        sleep(.2)
        moveTo(483, 505)
        # moveTo(1066, 435) #jeton
        click()

        
        


        
 
if __name__ == "__main__":
    print("HEALTH running")
    all_relics = [False]
    
    stop_event = threading.Event()

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()






