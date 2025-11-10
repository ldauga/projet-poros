import random
from minescript import (player, player_orientation, player_set_orientation)
import time

pos = player().position
pos[1] += 1.25

orientation = player_orientation()

target_pos = (333.5, -3, -115.5)


import math

def look_at_subject(start_pos, end_pos, orientation, steps=30, curve_strength=0.2):
    """
    Smoothly rotate the camera from start_pos to end_pos to face the subject.
    
    start_pos: (x, y, z) tuple of player starting position
    end_pos:   (x, y, z) tuple of subject/target position
    steps:     number of interpolation steps
    curve_strength: strength of curve applied to movement
    """

    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    dz = end_pos[2] - start_pos[2]

    target_yaw = math.degrees(math.atan2(-dx, dz))
    dist_xz = math.sqrt(dx*dx + dz*dz)
    target_pitch = -math.degrees(math.atan2(dy, dist_xz))

    yaw, pitch = orientation

    delta_y = target_yaw - yaw
    delta_p = target_pitch - pitch

    perp_yaw = -delta_p * 0.1
    perp_pitch = delta_y * 0.1

    BASE_DELAY = 0.02

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



look_at_subject(pos, target_pos, orientation)


