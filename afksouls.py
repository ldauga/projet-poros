import threading
from time import sleep
from pyautogui import click, moveTo

from avast import SOUND_RESETER_KEY
from system.lib.minescript import EventQueue, EventType, execute

STOP_KEY = 333

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:  # key down
                if ev.key == STOP_KEY:
                    print("Stopping")
                    stop_event.set()
                    break
                
                    


for _ in range(20):
    execute("afk")
    sleep(0.2)
    moveTo(1129, 380)
    sleep(0.2)
    click()
    moveTo(851, 379)
    sleep(0.2)
    click()
