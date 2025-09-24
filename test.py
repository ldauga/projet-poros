
from contextlib import redirect_stdout
import random
import time
from typing import Tuple
from minescript import (player, EventQueue, EventType, player_look_at, player_orientation, player_set_orientation, execute, player_press_forward, player_press_right, player_press_left, player_press_attack, getblock)
import sys
import math
import threading


def precise_sleep(duration: float, stop_event: threading.Event):
    """
    Sleep for 'duration' seconds with reduced jitter.
    Uses perf_counter, compensates drift, and spin-waits in the last ~1ms.
    """
    if stop_event.is_set():
        return
    start = time.time()
    end = start + duration
    while not stop_event.is_set():
        now = time.time()
        remaining = end - now
        if remaining <= 0:
            break
        if remaining > 0.002:
            time.sleep(remaining - 0.001)
        else:
            # Final tight spin wait for sub-millisecond precision.
            while not stop_event.is_set() and time.time() < end:
                pass
            break


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


STOP_KEY = 259




stop = False

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            event = event_queue.get()
            if event.type == EventType.KEY and event.action == 1:  # key down
                if event.key == STOP_KEY:
                    stop_event.set()
                    break
        


def better_turn(orientation_wanted: Tuple[float, float],
                seconds: float,
                stop_event: threading.Event):
    if stop_event.is_set():
        return

    start_yaw, start_pitch = player_orientation()
    target_yaw, target_pitch = float(orientation_wanted[0]), float(orientation_wanted[1])

    # Normalize shortest-path yaw movement if needed (optional):
    def shortest_delta(a, b):
        d = (b - a + 180.0) % 360.0 - 180.0
        return d

    dyaw   = shortest_delta(start_yaw,   target_yaw)
    dpitch = (target_pitch - start_pitch)

    t0 = time.perf_counter()
    t_end = t0 + max(0.0, seconds)

    # Update at a nominal rate, but compute from exact time
    nominal_dt = 0.03  # 100 Hz target updates
    next_tick = t0

    while not stop_event.is_set():
        now = time.perf_counter()
        if now >= t_end:
            break

        # progress in [0,1]
        p = (now - t0) / seconds if seconds > 0 else 1.0
        # Optionally ease (e.g., smoothstep) to reduce jerk; linear is fine too.
        # p_eased = p*p*(3 - 2*p)
        p_eased = p

        yaw   = start_yaw   + dyaw   * p_eased
        pitch = start_pitch + dpitch * p_eased
        player_set_orientation(yaw, pitch)

        # schedule next tick precisely
        next_tick += nominal_dt
        delay = next_tick - time.perf_counter()
        if delay > 0:
            precise_sleep(delay, stop_event)

    # Final snap to desired orientation (exact)
    if not stop_event.is_set():
        player_set_orientation(target_yaw, target_pitch)

    
    

def player_turn(direction: str | None, orientation: list, delta_angle: float, duration: float, stop_event: threading.Event):
    """Apply left/right press changes (if any), then turn by delta_angle for duration."""
    if direction == "right":
        player_press_right(True)
        player_press_left(False)
    elif direction == "left":
        player_press_left(True)
        player_press_right(False)
    elif direction == "release":
        player_press_left(False)
        player_press_right(False)
    # direction == None => keep current press state

    orientation[0] += delta_angle
    better_turn(orientation, duration, stop_event)


def main(stop_event: threading.Event):
    try:
        while not stop_event.is_set():
        # orientation = player_orientation()
            orientation = [45, 20]

            # execute("/tp 307.70 -2 13.30")
            player_set_orientation(*orientation)
            player_press_forward(True)

            precise_sleep(3.2, stop_event)
            player_press_attack(True)

            # (direction, delta_angle, duration)
            # direction: "right" | "left" | "release" | None (no change)
            turn_sequence = [
                ("right", +25, 1.0),

                (None,  -20, 0.7),
                (None,  -10, 0.1),
                (None,  -20, 0.6),

                (None,  +45, 0.5),
                (None,  -43, 0.7),
                (None,  +45, 0.5),
                (None,  -60, 0.4),

                (None,   +5, 0.05),
                (None,  -25, 0.2),
                (None,  -35, 0.2),
                (None,  -58, 0.4),

                (None,  +48, 0.5),
                (None,  -10, 0.1),
                (None,  +42, 0.5),
                (None,  +55, 0.4),

                ("left", -64, 0.6),
                (None,  -42, 0.4),

                ("right", +82, 0.7),
                (None,   +49, 0.4),

                ("left", -79, 0.4),
                (None,  -46, 0.4),
                (None,  -25, 0.4),

                ("right", +65, 0.5),
                (None,   +46, 0.4),
                (None,   +52, 0.3),

                ("left", -46, 0.4),
                (None, -57, 0.4),
                (None, -70, 0.3),
                
                ("right", +46, 0.4),
                (None, +56, 0.3),
                
                ("left", -51, 0.4),
                (None, -49, 0.4),
                (None, -48, 0.3),
                
                ("right", +51, 0.3),
                (None, +57, 0.4),
                
                ("left", -49, 0.4),
                (None, -51, 0.4),
                (None, -49, 0.3),
                
                ("right", +52, 0.3),
                (None, +56, 0.4),
                
                ("left", -38, 0.4),
                (None, -51, 0.4),
                (None, -49, 0.3),
                
                ("right", +54, 0.3),
                (None, +39, 0.4),
                (None, +51, 0.4),
                (None, +56, 0.4),
                
                ("left", -38, 0.4),
                (None, -51, 0.4),
                
                ("right", +46, 0.4),
                (None, +56, 0.3),
                
                
                ("left", -64, 0.4),
                (None, -52, 0.3),
                
                ("right", +65, 0.5),
                (None,   +46, 0.4),
                (None,   +52, 0.3),
                
                ("left", -46, 0.4),
                (None, -57, 0.4),
                (None, -70, 0.3),
                
                ("right", +51, 0.3),
                (None, +57, 0.4),
                (None, +56, 0.4),
                
                ("left", -79, 0.4),
                (None,  -46, 0.4),
                (None,  -25, 0.4),
                (None, -51, 0.4),
                
                ("right", +54, 0.3),
                (None, +39, 0.4),
                (None, +51, 0.4),
                
                ("left", -46, 0.4),
                (None, -57, 0.4),
            ]

            for direction, delta, duration in turn_sequence:
                player_turn(direction, orientation, delta, duration, stop_event)
                
            player_press_right(False)
            player_press_left(False)
            orientation[0] -= 42
            better_turn(orientation, .2, stop_event)
            
            precise_sleep(1.5, stop_event)
            
            orientation[0] -= 107
            better_turn(orientation, 8.5, stop_event)
            
            player_press_attack(False)
            player_press_right(False)
            orientation[0] += 176
            better_turn(orientation, .5, stop_event)
            
            player_look_at(307, -2, 13)
            
            player_press_forward(False)
            precise_sleep(20, stop_event)
            
            player_press_forward(True)
            precise_sleep(3, stop_event)
            player_press_forward(False)
            
            precise_sleep(5, stop_event)
            
            
        
        
        

        # return

    finally:
        player_press_forward(False)
        player_press_attack(False)
        player_press_right(False)
        player_press_left(False)




if __name__ == "__main__":
    stop_event = threading.Event()

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()

    # Optionally wait for threads to finish
    t1.join()
    t2.join()