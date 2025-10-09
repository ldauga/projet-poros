
import threading
from time import sleep

from system.lib.minescript import EventQueue, EventType, execute, player, world_info

STOP_KEY = 333

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
    
    while not stop_event.is_set():
        x, y, z = player().position
        
        
        if y == 111.93750:
            execute("/farm")
            sleep(.5)
                
        if -38 <= x <= -37 and 13 <= z <= 18 and -4 <= y <= -2:  # PORTAIL 
            execute("/farm")
            sleep(.5)
        if -316 <= x <= -314 and 92 <= y <= 94 and 22 <= z <= 23:  # PORTAIL 
            execute("/mine")
            sleep(.5)
        
        
        sleep(0.1)
        
        # (232, 111, 83) 
        # (232, 111, 84) 
        # (233, 111, 84) 
        # (233, 111, 83)
    print("Balise Stopped")
    
        
        
        
        


 


if __name__ == "__main__":
    print("Balise running")
    stop_event = threading.Event()
    

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)
    # t3 = threading.Thread(target=avast, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()
    # # t3.start()

    # # Optionally wait for threads to finish
    t1.join()
    t2.join()
    # # t3.join()