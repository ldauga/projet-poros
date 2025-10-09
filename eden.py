from contextlib import redirect_stdout
import difflib
import math
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
        event_queue.register_key_listener()
        while not stop_event.is_set():
            event = event_queue.get()

            if event.type == EventType.KEY and event.action == 1:  # key down
                if event.key == STOP_KEY:
                    stop_event.set()
                    break


def look_at_subject(start_pos, end_pos, orientation, steps=10, curve_strength=0):
    """
    Smoothly rotate the camera from start_pos to end_pos to face the subject.
    
    start_pos: (x, y, z) tuple of player starting position
    end_pos:   (x, y, z) tuple of subject/target position
    steps:     number of interpolation steps
    curve_strength: strength of curve applied to movement
    """

    # Compute yaw and pitch required to face target
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    dz = end_pos[2] - start_pos[2]

    target_yaw = math.degrees(math.atan2(-dx, dz))
    dist_xz = math.sqrt(dx*dx + dz*dz)
    target_pitch = -math.degrees(math.atan2(dy, dist_xz))

    # Starting orientation (could be dynamic; here assume forward = yaw=0, pitch=0)
    yaw, pitch = orientation

    # Deltas
    delta_y = target_yaw - yaw
    delta_p = target_pitch - pitch

    # Perpendicular offsets for smooth curve
    perp_yaw = -delta_p * 0.1
    perp_pitch = delta_y * 0.1

    BASE_DELAY = 0.02  # base time between steps

    for i in range(1, steps + 1):
        frac = i / steps
        base_yaw = yaw + delta_y * frac
        base_pitch = pitch + delta_p * frac

        curve_factor = math.sin(math.pi * frac) * curve_strength
        curve_yaw = perp_yaw * curve_factor
        curve_pitch = perp_pitch * curve_factor

        jitter_yaw = random.uniform(-0.12, 0.12)
        jitter_pitch = random.uniform(-0.12, 0.12)

        next_y = base_yaw + curve_yaw + jitter_yaw
        next_p = base_pitch + curve_pitch + jitter_pitch

        player_set_orientation(next_y, next_p)
        time.sleep(BASE_DELAY)
    player_set_orientation(target_yaw, target_pitch)
    
def process_move(type: Union[Literal["right", "left"], None], pos):
    
    if type == None:
        player_press_right(False)
        player_press_left(False)
    elif type == "right":
        player_press_right(True)
        player_press_left(False)
    else:
        player_press_right(False)
        player_press_left(True)
        
    look_at_subject(player().position, pos, player_orientation())
    
    
    
    pass    
    


def main(stop_event: threading.Event):
    
    try:

        with open(sys.path[0] + "/eden.path", "r+") as f:
            
            # if 
            
            
            positions = []

            for line in f:
                line = line.strip()
                if line:  # skip empty lines
                    # remove parentheses and split by comma
                    x, y, z = map(float, line.strip("()").split(","))
                    positions.append((x, y, z))
            
        # while not stop_event.is_set():
            # block = player_get_targeted_block()
            # if block:
            #     pos = block.position
            #     f.write(f"({int(pos[0])}, {int(pos[1])}, {int(pos[2])})\n")
            #     time.sleep(.2)

        
        player_press_forward(True)
        
        
        # moves = [
        #     [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        #     # [None, (299, -3, 23)]
        # ]
        
        for move in positions:
            look_at_subject(player().position, move, player_orientation())
        #     process_move(*move)
        # # while True:
        
        # pass
    
    finally:
        player_press_right(False)
        player_press_forward(False)
        player_press_left(False)
    
    
    


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