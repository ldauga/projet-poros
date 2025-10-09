

import threading

from auto import STOP_KEY
from system.lib.minescript import EventQueue, EventType



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


if __name__ == "__main__":
    print("Balise running")
    stop_event = threading.Event()
    prestige_to_pass = [False]

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
