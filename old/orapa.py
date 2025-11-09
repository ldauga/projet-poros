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
# from minescript import ()
import sys
import json

from system.lib.minescript import player_press_backward, player_press_forward, player, EventQueue, EventType, player_look_at, player_orientation, player_get_targeted_block, player_press_attack, echo, flush, getblock, player_set_orientation, player_get_targeted_entity, player_press_sneak, player_press_left, player_press_right

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


def shortest_angle_delta(target: float, current: float) -> float:
    """Retourne la différence (target - current) dans l'intervalle [-180, 180)."""
    return ((target - current + 180.0) % 360.0) - 180.0


def block_center(pos: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """Centre visuel d’un bloc aux coords entières (ou déjà centré si coords décimales)."""
    x, y, z = pos
    return (round(x) + 0.5 if float(x).is_integer() else x,
            round(y) + 0.5 if float(y).is_integer() else y,
            round(z) + 0.5 if float(z).is_integer() else z)

def local_axes_from_yaw(yaw_deg: float) -> Tuple[Tuple[float,float,float], Tuple[float,float,float]]:
    """
    Renvoie (forward, right) dans le plan XZ à partir du yaw (en degrés).
    Convention cohérente avec ton look_at_subject:
      - yaw 0° = vers +Z
      - yaw augmente vers la droite
    """
    yaw = math.radians(yaw_deg)
    # Avant (XZ) : ( -sin(yaw), 0, cos(yaw) )
    fwd = (-math.sin(yaw), 0.0, math.cos(yaw))
    # Droite (XZ) = croix(Up, Forward) ou simplement (fwd.z, 0, -fwd.x)
    right = (fwd[2], 0.0, -fwd[0])
    return fwd, right

def normalize2(vx: float, vz: float) -> Tuple[float,float]:
    n = math.hypot(vx, vz)
    if n == 0.0: return (0.0, 0.0)
    return (vx/n, vz/n)

class StrafeController:
    """
    Contrôleur très simple (P + hystérésis) pour décider gauche/droite (+ avant/arrière si dispo).
    - deadzone évite l’oscillation près du centre.
    - on applique un délai mini entre inversions.
    """
    def __init__(self,
                 deadzone=0.08,
                 release_zone=0.05,
                 min_switch_interval=0.35):
        self.dead = deadzone
        self.rel = release_zone
        self.min_switch = min_switch_interval
        self.last_dir_lr = 0  # -1 gauche, 0 neutre, +1 droite
        self.last_dir_fb = 0  # -1 back,   0 neutre, +1 forward
        self.last_switch_t_lr = 0.0
        self.last_switch_t_fb = 0.0

    def _decide_axis(self, s: float, last_dir: int, last_switch_t: float) -> Tuple[int, float]:
        now = time.time()
        # Hystérésis : on sort de la zone morte avec deadzone, on relâche à release_zone
        if abs(s) <= self.rel:
            desire = 0
        elif abs(s) <= self.dead:
            # Dans la bande d’hystérésis : garder la décision
            desire = last_dir
        else:
            desire = 1 if s > 0 else -1

        if desire != last_dir and (now - last_switch_t) < self.min_switch:
            # Trop tôt pour inverser : rester comme avant
            desire = last_dir
        if desire != last_dir:
            last_switch_t = now
        return desire, last_switch_t

    def step(self, s_right: float, s_forward: float):
        # Décision gauche/droite
        dir_lr, self.last_switch_t_lr = self._decide_axis(s_right, self.last_dir_lr, self.last_switch_t_lr)
        self.last_dir_lr = dir_lr

        # Décision avant/arrière (si bindings présents)
        dir_fb, self.last_switch_t_fb = self._decide_axis(s_forward, self.last_dir_fb, self.last_switch_t_fb)
        self.last_dir_fb = dir_fb

        return dir_lr, dir_fb

# Instancier un contrôleur global (hors main())
STRAFE = StrafeController(deadzone=0.10, release_zone=0.05, min_switch_interval=0.40)

def human_like_recenter(step_target: Tuple[float,float,float], stop_event: threading.Event, hold_time=0.12):
    """
    Décide d’un micro-déplacement latéral (et avant/arrière si dispo) pour se recentrer vers le bloc cible,
    en fonction de la position/orientation actuelles du joueur.
    - hold_time: durée d’appui pour un “tap” (évite le maintien trop long).
    """
    if stop_event.is_set(): 
        return

    pos = player().position
    pos_eye = (pos[0], pos[1] + 1.5, pos[2])

    yaw, pitch = player_orientation()
    fwd, right = local_axes_from_yaw(yaw)

    # Direction vers la cible (plutôt centre du bloc)
    tx, ty, tz = block_center(step_target)
    dx, dy, dz = (tx - pos_eye[0], ty - pos_eye[1], tz - pos_eye[2])

    # On ne décide que dans le plan XZ pour le déplacement
    dir_xz = normalize2(dx, dz)
    # Projections scalaires (cosinus direct) sur les axes locaux
    s_forward = dir_xz[0]*fwd[0] + dir_xz[1]*fwd[2]
    s_right   = dir_xz[0]*right[0] + dir_xz[1]*right[2]

    dir_lr, dir_fb = STRAFE.step(s_right, s_forward)

    # Appliquer un tap court plutôt que maintien pour limiter “bot-like”
    # Gauche/Droite :
    if dir_lr < 0:
        player_press_right(False)
        player_press_left(True)
        time.sleep(hold_time)
        player_press_left(False)
    elif dir_lr > 0:
        player_press_left(False)
        player_press_right(True)
        time.sleep(hold_time)
        player_press_right(False)
    else:
        player_press_left(False)
        player_press_right(False)
        
    if dir_fb > 0:
        player_press_backward(False)
        player_press_forward(True)
        time.sleep(hold_time * 0.9)
        player_press_forward(False)
    elif dir_fb < 0:
        player_press_forward(False)
        player_press_backward(True)
        time.sleep(hold_time * 0.9)
        player_press_backward(False)
    else:
        player_press_forward(False)
        player_press_backward(False)


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
    delta_y = shortest_angle_delta(target_yaw, yaw)
    delta_p = shortest_angle_delta(target_pitch, pitch)
    
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
    with open(sys.path[0] + '/assets/blocklist.json') as f:
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
                    
                    entity_check = 0
                    
                    last_move = time.time()
                    next_move = random.uniform(1.0, 2.0)
                    
                    initial_player_pos = player().position

                    while True:
                        # time.sleep(0.8)
                    # main(match)
                    
                        TIME_BREAKING_LIMIT = .3
            
                        block_list = [
                            
                            (-183 + .6, 125 + .3, -26 + .9),
                            (-182 + .6, 125 + .3, -26 + .9),
                            (-181 + .6, 125 + .3, -26 + .9),
                            (-180 + .6, 125 + .3, -26 + .9),
                            (-180 + .6, 124 + .3, -26 + .9),
                            (-181 + .6, 124 + .3, -26 + .9),
                            (-181 + .6, 123 + .3, -26 + .9),
                            (-180 + .6, 123 + .3, -26 + .9),
                            (-180 + .6, 122 + .3, -26 + .9),
                            
                            
                            (-178, 125 + .3, -24 + .5),
                            (-178, 124 + .3, -24 + .5),
                            (-178, 124 + .3, -25 + .5),
                            (-178, 123 + .3, -24 + .5),
                            (-178, 123 + .3, -25 + .5),
                            (-178, 122 + .3, -24 + .5),
                            (-178, 122 + .3, -25 + .5),
                            (-178, 121 + .3, -24 + .5),
                            (-179, 121 + .3, -25 + .5),
                            
                            
                            (-179 +.5, 120 + .9, -24 + .5),
                            (-179 +.5, 120 + .9, -23 + .5),
                            (-178 +.5, 120 + .9, -23 + .5),
                            (-178 +.5, 120 + .9, -22 + .5),
                            
                            
                            (-180 + .5, 120 + .9, -22 + .5),
                            (-181 + .5, 120 + .9, -20 + .5),
                            
                            
                            (-183 + .5, 119 + .9, -21 + .5),
                            (-184 + .5, 119 + .9, -21 + .5),
                            (-183 + .5, 119 + .9, -22 + .5),
                            (-182 + .5, 119 + .9, -23 + .5),
                            (-183 + .5, 119 + .9, -23 + .5),
                            (-184 + .5, 119 + .9, -23 + .5),
                            (-182 + .5, 119 + .9, -24 + .5),
                            (-183 + .5, 119 + .9, -24 + .5),
                        
                            
                            
                            (-184 + .6, 120 + .3, -26 + .9),
                            (-183 + .6, 120 + .3, -26 + .9),
                            (-183 + .6, 121 + .3, -26 + .9),
                            (-183 + .6, 122 + .3, -26 + .9),
                            
                            
                            
                         # ORAPA V1
                            
                            # (162, 37, 135),
                            # (-182 + .5, 121.5, -12),
                            # (-183 + .5, 121.5, -12),
                            # (-184 + .5, 121.5, -12),

                            # (-184 + .5, 122.5, -12),
                            # (-185 + .5, 122.5, -12),

                            # (-185 + .5, 121.5, -13),
                            # (-186 + .5, 121.5, -13),
                            # (-186 + .5, 122.5, -13),
                            # (-187 + .5, 122.5, -13),
                            # (-187 + .5, 121.5, -13),
                            # (-188 + .5, 121.5, -13),
                            # (-189 + .5, 121.5, -13),
                            # (-189 + .5, 120.5, -13),
                            # (-188 + .5, 120.5, -13),
                            # (-187 + .5, 120.5, -13),
                            # (-186 + .5, 120.5, -13),
                            # (-185 + .5, 120.5, -13),
                            # (-184 + .5, 120.5, -13),
                            # (-185 + .5, 119.5, -14 + .5),
                            # (-187 + .5, 119.5, -13),
                            # (-188 + .5, 119.5, -13),
                        ]
                        
                        # player_press_sneak(True)
                        

                        # human_like_recenter(initial_player_pos, stop_event, hold_time=0.10)
                        
                        


                        for block in block_list:
                            pos = player().position
                            pos[1] += 1.5
                            if stop_event.is_set():
                                    return
                            orientation = player_orientation()
                            look_at_subject(pos, block, orientation, steps=10, curve_strength=1)
                            orientation = player_orientation()
                            
                            t0 = time.time()
                            while (targeted_block := player_get_targeted_block()) is not None and targeted_block.type == match:
                                player_press_left(False)
                                player_press_right(False)
                                if stop_event.is_set():
                                    return
                                if time.time() - t0 >= TIME_BREAKING_LIMIT:
                                    break
                                if player_get_targeted_entity(4):
                                    print("entity check")
                                    entity_check += 1
                                    if entity_check >= 5:
                                        stop_event.set()
                                        return
                                    player_press_attack(False)
                                    time.sleep(10)
                                    player_press_attack(True)
                                # if time.time() - last_move >= next_move:
                                    
                                    
                                #     movements[relative_direction(pos, orientation[0], initial_player_pos)](True)
                                    
                                #     # random.choice((player_press_left, player_press_right))(True)
                                #     last_move = time.time()
                                time.sleep(0.01)
                            # player_press_left(False)
                            # player_press_right(False)
                            # player_press_forward(False)
                            # player_press_backward(False)
                            time.sleep(0.1)
                            
                        
                        
                        orientation = player_orientation()
                        
                        # look_at_subject(pos, (-187 + .5, 121.5, -13), orientation, steps=10, curve_strength=1)
                        
                        # time.sleep(0.2)
                        
                        # orientation = player_orientation()
                        
                        
                        
                        # look_at_subject(pos, (-185 + .5, 121.5, -13), orientation, steps=10, curve_strength=1)
                        # time.sleep(0.2)
                finally:
                    player_press_attack(False)
                    player_press_left(False)
                    player_press_right(False)
                    player_press_forward(False)
                    player_press_backward(False)
                    player_press_sneak(False)

                    
                    

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