

import math
import threading
from time import sleep
from typing import Tuple
import winsound

import pyautogui

from system.lib.minescript import EventQueue, EventType, player, player_orientation, player_position


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


def distance_between_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean distance between two 3D points.
    
    Args:
        p1 (tuple): First point as (x, y, z).
        p2 (tuple): Second point as (x, y, z).
        
    Returns:
        float: Distance between p1 and p2.
    """
    return abs(math.sqrt((p2[0] - p1[0])**2 +
                     (p2[1] - p1[1])**2 +
                     (p2[2] - p1[2])**2))


def main(stop_event: threading.Event):

    check = False 
    
    last_pos = player_position()
    last_yaw, last_pitch = player_orientation()
    
    
    while not stop_event.is_set():
        
        if check:
            winsound.Beep(800, 100)
            print("VERIF EN COURS")
        
        
        yaw, pitch = player_orientation()
        pos = player_position()
        
        if distance_between_points(last_pos, player_position()) > 2:
            check = True
            
            sleep(1)
            
            pyautogui.press("F7")
            
            
            
            
            winsound.Beep(800, 100)
            
        last_pos = player_position()
            
            
        sleep(.01)
        



if __name__ == "__main__":
    print("AVAST running")
    stop_event = threading.Event()
    prestige_to_pass = [False]

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()

    t1.join()
    t2.join()
