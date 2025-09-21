r"""Orapa v0.2 — distributed via Leoir

Usage:
    \orapa BLOCK_TYPE

Mimics human-like mining behavior to break the specified block,
helping bypass basic anti-cheat detection.

Created by Leoir.
All rights reserved. Unauthorized distribution, modification, or commercial use is prohibited.
"""

from contextlib import redirect_stdout
from typing import Tuple
from minescript import (player, EventQueue, EventType, player_look_at, player_orientation, player_get_targeted_block, player_press_attack, echo, flush, getblock)
import sys
import json

STOP_KEY = 259 # BACKSPACE

def diff_between_points(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """
    Return the difference (dx, dy, dz) between two 3D points.
    
    Args:
        p1 (tuple): First point as (x, y, z).
        p2 (tuple): Second point as (x, y, z).
        
    Returns:
        tuple: (dx, dy, dz) where each is p2 - p1.
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]
    return dx, dy, dz

def is_in_box(pos: Tuple[float, float, float],
              min_pos: Tuple[float, float, float],
              max_pos: Tuple[float, float, float]) -> bool:
    """
    Check if a 3D point is inside (or on the edge of) a box defined by min and max coordinates.

    Args:
        pos (Tuple[float, float, float]): position of the point to check.
        min_pos (Tuple[float, float, float]): position of the minimum corner of the box.
        max_pos (Tuple[float, float, float]): position of the maximum corner of the box.
    Returns:
        True if the point is inside or on the box edges, False otherwise.
    """
    return (
        min_pos[0] <= pos[0] <= max_pos[0] and
        min_pos[1] <= pos[1] <= max_pos[1] and
        min_pos[2] <= pos[2] <= max_pos[2]
    )


def block_bounds_from_center(center: Tuple[float, float, float], size: Tuple[int, int, int]):
    """
    Return the bounding corner of a rectangle of <size> centered in <center>

    Args:
        center (Tuple[float, float, float]): center of the square
        size (Tuple[int, int, int]): size of the final square

    Returns:
        Tuple[Tuple[int, int, int], Tuple[int, int, int]]: bounding corner position
    """
    x, y, z = center
    sx, sy, sz = size
    min_pos = (int(x - (sx - 1) / 2), int(y - (sy - 1) / 2), int(z - (sz - 1) / 2))
    max_pos = (int(x + (sx - 1) / 2), int(y + (sy - 1) / 2), int(z + (sz - 1) / 2))
    return min_pos, max_pos

import math
import random
import time
from typing import Tuple

# If you already define BASE_DELAY elsewhere, remove this line.
BASE_DELAY = 0.015  # seconds between micro-steps


import difflib
import math

import math
from typing import Tuple, Optional

def point_in_fov(
    start: Tuple[float, float, float],
    orientation: Tuple[float, float],
    point: Tuple[float, float, float],
    fov_deg: float,
    max_distance: Optional[float] = None,
    yaw_offset: float = 90.0,
    pitch_offset: float = -10.0,
) -> bool:
    """
    Check if `point` lies inside the player's field of view (3D cone).

    Parameters
    ----------
    start : (x, y, z)
        Player position.
    orientation : (yaw, pitch)
        Same conventions as your ray:
        - yaw around Z (horizontal), in degrees.
        - pitch around Y (vertical), in degrees.
        Offsets (yaw_offset=+90, pitch_offset=-10) mirror your ray computation.
    point : (x, y, z)
        Target point to test.
    fov_deg : float
        Full cone angle in degrees (e.g., 90 => half-angle is 45).
    max_distance : float | None
        If provided, the point must also be within this distance.
    yaw_offset, pitch_offset : float
        Offsets to keep behavior consistent with your ray_end_position.

    Returns
    -------
    bool
        True if the point is inside the FOV cone (and distance, if given).
    """
    px, py, pz = start
    tx, ty, tz = point

    # Forward (unit) vector from orientation, matching your ray math
    yaw_rad = math.radians(orientation[0] + yaw_offset)
    pitch_rad = math.radians(orientation[1] + pitch_offset)

    fx = math.cos(pitch_rad) * math.cos(yaw_rad)
    fy = -math.sin(pitch_rad)
    fz = math.cos(pitch_rad) * math.sin(yaw_rad)

    # Vector from player to target
    vx = tx - px
    vy = ty - py
    vz = tz - pz

    # Distance & normalization
    dist = math.sqrt(vx*vx + vy*vy + vz*vz)
    if dist == 0.0:
        return True  # same position -> trivially "in FOV"
    if max_distance is not None and dist > max_distance:
        return False

    inv_dist = 1.0 / dist
    ux, uy, uz = vx * inv_dist, vy * inv_dist, vz * inv_dist

    # Angle between forward and target
    dot = fx*ux + fy*uy + fz*uz
    # Clamp for numerical stability
    dot = max(-1.0, min(1.0, dot))

    half_fov_rad = math.radians(fov_deg * 0.5)
    # Equivalent check without acos (faster): dot >= cos(half_fov)
    return dot >= math.cos(half_fov_rad)


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

# # Example usage:
# p1 = (1, 2, 3)
# p2 = (4, 6, 8)


def break_utils(targeted_block: str):
    
    def a():
    
        
        player_press_attack(True)
        player_press_attack(False)
        flush()
        return 0
    
    return a

def hold_attack_until_broken(
    target_block_type: str,
    target_pos_center: tuple[float, float, float],
    max_hold_s: float = 8.0,
    poll_every: float = 0.05,
) -> bool:
    
    break_value = False
    
    while True:
        tb = player_get_targeted_block(5.0)
        
        
        if not tb or tb.type != target_block_type:
            break
        
        player_press_attack(True)
        time.sleep(0.1)
        
    player_press_attack(False)
    flush()
    
    # tb = player_get_targeted_block(5.0)
    # if not tb or (tb.position[0]+0.5, tb.position[1]+0.5, tb.position[2]+0.5) != tuple(target_pos_center):
    #     player_look_at(*target_pos_center)
    #     flush()
    #     time.sleep(0.02)
    #     tb = player_get_targeted_block(5.0)

    # start = time.time()
    # pressed = False
    # try:
    #     while True:
    #         if time.time() - start > max_hold_s:
    #             return False  # timeout

    #         block = player_get_targeted_block(5.0)
    #         if not block or block.type != target_block_type:
    #             return True  # block changed/broken

    #         if not pressed:
    #             # Make absolutely sure no stdout leaks during this call:
    #             with redirect_stdout(sys.stderr):  # or redirect to _sink
    #                 player_press_attack(True)
    #             flush()
    #             pressed = True

    #         time.sleep(poll_every)
    # finally:
    #     if pressed:
    #         with redirect_stdout(sys.stderr):
    #             player_press_attack(False)
    #         # flush()  # optional

    

def smooth_look_at(pos_to_look_at: Tuple[int, int, int]):
    
    
    
    
    
    
    
    camera_pos = player().position
    camera_pos[1] += 1
    distance_with_player = distance_between_points(camera_pos, pos_to_look_at)
    actual_looking_pos = ray_end_position(camera_pos, player_orientation(), distance_with_player)
    distance_between_looking_point = distance_between_points(actual_looking_pos, pos_to_look_at)
    MAX_STEP = max((int(distance_between_looking_point)) ** 3, 10)
    difference = diff_between_points(actual_looking_pos, pos_to_look_at)
    
    
    # initial
    
    
    last_looking_pos = actual_looking_pos
    
    for i in range(MAX_STEP):
        frac = (i + 1) / MAX_STEP  # plus simple
        actual_looking_pos = ray_end_position(camera_pos, player_orientation(), distance_with_player)
        difference = diff_between_points(actual_looking_pos, pos_to_look_at)

        # Pas théorique pour arriver exactement à la cible
        step = [d / (MAX_STEP - i) for d in difference]

        # Ajout de random qui se réduit en fin de parcours
        noise_strength = (1 - frac) ** 2
        step_with_noise = [
            step[0] + (random.uniform(-0.05, 0.05) * noise_strength),
            step[1] + (random.uniform(-0.05, 0.05) * noise_strength),
            step[2] + (random.uniform(-0.05, 0.05) * noise_strength),
        ]

        last_looking_pos = [
            last_looking_pos[0] + step_with_noise[0],
            last_looking_pos[1] + step_with_noise[1],
            last_looking_pos[2] + step_with_noise[2],
        ]

        player_look_at(*last_looking_pos)
        time.sleep(0.01 + random.uniform(0, 0.01))
    
    
    
    # player_look_at



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

def main(tracked_block: str):

    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        event_queue.register_block_update_listener()
        while True:
            event = event_queue.get()
            if event.type == EventType.KEY:
                if event.action == 0: # up
                    pass
                elif event.action == 1: # down
                    if event.key == STOP_KEY:
                        return
                    # if event.key == 265:
                    #     smooth_look_at((6.5, -58.5, 6.5))
                else: # repeat
                    pass
            
            if event.type == EventType.BLOCK_UPDATE:
            
                if event.new_state == tracked_block and getblock(*event.position) == tracked_block:
                    
                    player_position = player().position
                    player_position[1] += 1
                    
                    target = event.position
                    target[0] += .5
                    target[1] += .5
                    target[2] += .5
                    if point_in_fov(player_position, player_orientation(), target, 135, 4.5):
                    
                    # min_pos, max_pos = block_bounds_from_center(player_position, (10, 5, 10))
                    
                    
                    # if is_in_box(event.position, min_pos, max_pos):
                        
                        print(f"new block spawned in the radius : {event.new_state}")
                        smooth_look_at(target)
                        
                        ok = hold_attack_until_broken(tracked_block, target)

                
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
            main(match)