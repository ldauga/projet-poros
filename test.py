import threading
import time
from system.lib.minescript import EventQueue, EventType, execute, player




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
                

def chat_command_process(stop_event):
    
    last_command_time = None
    last_sender = None
    
    try:
        
        with EventQueue() as events:
            events.register_chat_listener()
            while not stop_event.is_set():
                ev = events.get()
                if not ev:
                    continue
                
                if ev.type == EventType.CHAT:
                    msg = (ev.message or "")
                    
                    
                    if "(Message " in msg:
                        
                        if "LeLeoOriginel" in msg or "gardounai" in msg:
                            
                            pseudo = "gardounai"
                            if "LeLeoOriginel" in msg:
                                pseudo = "LeLeoOriginel"
                            
                            msg = msg.split(f"{pseudo})")[-1].strip()
                            
                            if "cmd" in msg:
                                
                                command = msg.split()
                                last_command_time = time.time()
                                last_sender = pseudo
                                
                                
                                
                                print("parse command")
    finally:
        
        
        if last_command_time is not None and time.time() - last_command_time < 60:
            if last_sender in ["LeLeoOriginel", "gardounai"]:
                execute(f"/msg {last_sender} unexpectedly {player().name}'s POROS broke :'(")
                                




if __name__ == "__main__":
    print('test')
    stop_event = threading.Event()

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=chat_command_process, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()