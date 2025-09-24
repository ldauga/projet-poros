r"""Orapa v1.0 — distributed via Leoir

Usage:
    \orapa BLOCK_TYPE

Mimics human-like mining behavior to break the specified block,
helping bypass basic anti-cheat detection.

Created by Leoir.
All rights reserved. Unauthorized distribution, modification, or commercial use is prohibited. For educational purpose only.
"""




from contextlib import redirect_stdout
import difflib
import math
import random
import threading
import time
from typing import Tuple
from minescript import (player, EventQueue, EventType, player_look_at, player_orientation, player_get_targeted_block, player_press_attack, echo, flush, getblock, player_set_orientation)
import sys
import json



def ray_end_position(
    start: Tuple[float, float, float],
    orientation: Tuple[float, float, float],
    length: float,
) -> Tuple[float, float, float]:
    """
    Compute the end position of a ray in 3D space.

    Parameters
    ----------
    start : (x, y, z)
        The starting position of the ray.
    orientation : (yaw, pitch, roll)
        Orientation of the ray. Roll is ignored for direction (used for full 3D rotations).
        - yaw: rotation around Z axis (horizontal angle)
        - pitch: rotation around Y axis (vertical angle)
    length : float
        Length of the ray.

    Returns
    -------
    (x_end, y_end, z_end)
        The end position of the ray.
    """
    x, y, z = start
    yaw, pitch = orientation

    yaw_rad = math.radians(yaw + 90)
    pitch_rad = math.radians(pitch - 10)
    
    dx = length * math.cos(pitch_rad) * math.cos(yaw_rad)
    dz = length * math.cos(pitch_rad) * math.sin(yaw_rad)
    dy = length * -math.sin(pitch_rad)

    return (
        x + dx,
        y + dy,
        z + dz
    )
    
def distance_between_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """
    Calculate the Euclidean distance between two 3D points.
    
    Args:
        p1 (tuple): First point as (x, y, z).
        p2 (tuple): Second point as (x, y, z).
        
    Returns:
        float: Distance between p1 and p2.
    """
    return round(math.sqrt((p2[0] - p1[0])**2 +
                     (p2[1] - p1[1])**2 +
                     (p2[2] - p1[2])**2))



def look_at_subject(start_pos, end_pos, orientation, steps=30, curve_strength=0.2):
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
        time.sleep(BASE_DELAY + random.uniform(-0.001, 0.001))
    player_set_orientation(target_yaw, target_pitch)
    

def normalize_input(name: str) -> str:
    """Normalize Minecraft-style names into a consistent, comparable format."""
    if name.startswith("minecraft:"):
        name = name.split("minecraft:", 1)[1]
    name = name.replace("_", " ")
    return name.title()

def find_closest_variant(query: str, blocks: list, cutoff: float = 0.6) -> str | None:
    query_norm = normalize_input(query)

    all_variants = [variant for block in blocks for variant in block["variants"]]

    for v in all_variants:
        if v.lower() == query_norm.lower():
            return True, v

    matches = difflib.get_close_matches(query_norm.lower(), [v.lower() for v in all_variants], n=1, cutoff=cutoff)
    if matches:
        for v in all_variants:
            if v.lower() == matches[0]:
                return False, v

    return False, None
    
def main(stop_event):
    with open(sys.path[0] + '/blocklist.json') as f:
        data = json.load(f)
        if len(sys.argv) < 2:
            echo("Usage: \\orapa <block_type>")
        else:
            input_arg = " ".join(sys.argv[1:])
            direct_match, match = find_closest_variant(normalize_input(input_arg), data)

            if not direct_match:
                echo(f"{sys.argv[1]} is not a valid block{' closest match is ' + match if match else ''}")
            else:
                match = "minecraft:" + "_".join((word.lower() for word in match.split()))
                echo(f"Orapa is stating wating for {match}")
                
                try:
                    player_press_attack(True)
                
                    while True:
                        # time.sleep(0.8)
                    # main(match)
            
                        block_list = [
                            (-182 + .5, 121.5, -12),
                            (-183 + .5, 121.5, -12),
                            (-184 + .5, 121.5, -12),

                            (-184 + .5, 122.5, -12),
                            (-185 + .5, 122.5, -12),

                            (-185 + .5, 121.5, -13),
                            (-186 + .5, 121.5, -13),
                            (-186 + .5, 122.5, -13),
                            (-187 + .5, 122.5, -13),
                            (-187 + .5, 121.5, -13),
                            (-188 + .5, 121.5, -13),
                            (-189 + .5, 121.5, -13),
                            (-189 + .5, 120.5, -13),
                            (-188 + .5, 120.5, -13),
                            (-187 + .5, 120.5, -13),
                            (-186 + .5, 120.5, -13),
                            (-185 + .5, 120.5, -13),
                            (-184 + .5, 120.5, -13),
                            (-185 + .5, 119.5, -14 + .5),
                            (-187 + .5, 119.5, -13),
                            (-188 + .5, 119.5, -13),
                        ]

                        pos = player().position
                        pos[1] += 1.5

                        for block in block_list:
                            orientation = player_orientation()
                            look_at_subject(pos, block, orientation, steps=10, curve_strength=1)
                            
                            while player_get_targeted_block().type == match:
                                if stop_event.is_set():
                                    return
                                time.sleep(0.01)
                            time.sleep(0.1)
                        
                        
                        orientation = player_orientation()
                        
                        look_at_subject(pos, (-187 + .5, 121.5, -13), orientation, steps=10, curve_strength=1)
                        
                        time.sleep(0.2)
                        
                        orientation = player_orientation()
                        
                        
                        
                        look_at_subject(pos, (-185 + .5, 121.5, -13), orientation, steps=10, curve_strength=1)
                        time.sleep(0.2)
                finally:
                    player_press_attack(False)
                    
                    

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
                
# def avast(stop_event: threading.Event):
    
    
#     last_pos = player().position
#     while True:
#         pos = player().position
        
        
#         if distance_between_points(pos, last_pos) > 5:
        
        
        
    
                            


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