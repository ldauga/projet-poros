from contextlib import redirect_stdout
import difflib
import math
import os
import random
import threading
import time
from typing import Literal, Tuple, Union
from minescript import (player, EventQueue, EventType, player_look_at, player_orientation, player_get_targeted_block, player_press_attack, echo, flush, getblock, player_set_orientation, player_press_forward, player_press_right, player_press_left)
import sys
import json




STOP_KEY = 333

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        # event_queue.register_key_listener()
        event_queue.register_mouse_listener()
        while not stop_event.is_set():
            event = event_queue.get()
            if event.type == EventType.MOUSE and event.action and not event.button :
                stop_event.set()
                break
            # if event.type == EventType.KEY and event.action == 1:  # key down
            #     if event.key == STOP_KEY:


def point_in_direction(start_pos, orientation, length):
    """
    Compute the 3D position of a point given a starting position, an orientation, and a distance.
    
    start_pos:   (x, y, z) tuple of starting position
    orientation: (yaw, pitch) in degrees
    length:      distance from starting point
    """
    x, y, z = start_pos
    yaw, pitch = orientation

    # Convert to radians
    yaw_rad = math.radians(yaw)
    pitch_rad = math.radians(pitch)

    # Compute directional vector
    dx = -math.sin(yaw_rad) * math.cos(pitch_rad)
    dy = -math.sin(pitch_rad)
    dz =  math.cos(yaw_rad) * math.cos(pitch_rad)

    # Scale by length and add to start position
    return (
        x + dx * length,
        y + dy * length,
        z + dz * length
    )

def main(stop_event):
    positions = []
    
    try:
        player_press_forward(True)
        while not stop_event.is_set():
            pos = player().position
            pos[1]+=1.5
            orientation = player_orientation()
            ray_end_pos = point_in_direction(pos, orientation, 3)
            positions.append(ray_end_pos)
            # f.write(f"({ray_end_pos[0]}, {ray_end_pos[1]}, {ray_end_pos[2]})\n")
            time.sleep(.2)
    finally:
        player_press_forward(False)
    path = os.path.join(sys.path[0], "eden.path")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join("({:.6f}, {:.6f}, {:.6f})".format(*pos) for pos in positions) + "\n")        
        
            
        
        
        



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