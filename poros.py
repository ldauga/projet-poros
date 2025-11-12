from datetime import datetime
import math
import os
import random
import re
import sys
import threading
from typing import Literal
import winsound
from time import sleep

from avast import distance_between_points
from utils.pygame_loader import play_mp3
from system.lib.minescript import EventQueue, EventType, chat, echo, execute, flush, player, player_inventory, player_position
from collections import deque

from utils.storage import storage

STOP_KEY = 333

POSSIBLE_TOOL = [
    "minecraft:diamond_hoe",
    "minecraft:diamond_pickaxe",
]
INITIAL_PRESTIGE = 50
PRESTIGE_SOUND_STOPPER_KEY = 330
LAST_CHAT_MESSAGES = deque(maxlen=10)
FLY_ACTIVATE_MSG = "[Fly] Tu as ac"
FLY_DESACTIVATE_MSG = "[Fly] Tu as d"
FLY_NOT_ALLOWED_MSG = "[Fly] Vous ne pouvez pas activer le fly ici"

actual_dimension: Literal["spawn", "is"] = "spawn"


BALISE_ENTER_SETH_1 = (27, 179, 19)
BALISE_ENTER_SETH_2 = (26, 184, 26)

BALISE_EXIT_SETH_1 = (46, 108, 59)
BALISE_EXIT_SETH_2 = (42, 112, 58)


BALISE_STORAGE = (44, 108, -22)






def is_in_block(pos, target):
    """
    Check if the target position is within the same block as the given position.
    Each block is a 1x1x1 cube aligned to integer coordinates.

    Parameters:
        pos (tuple): Block position (x, y, z)
        target (tuple): Target position (xt, yt, zt)

    Returns:
        bool: True if target is inside the same block, False otherwise.
    """
    x, y, z = map(math.floor, pos)
    xt, yt, zt = map(math.floor, target)

    return (x, y, z) == (xt, yt, zt)


def passed_through_thick_pane(pos1, pos2, prev_pos, curr_pos):
    """
    Check if the player crosses a 3D pane (thin box) between two positions.

    The pane is defined by two opposite corners (pos1, pos2),
    and it can have thickness along one axis.

    Parameters:
        pos1 (tuple): First corner of the pane (x1, y1, z1)
        pos2 (tuple): Opposite corner of the pane (x2, y2, z2)
        prev_pos (tuple): Player's previous position (xp1, yp1, zp1)
        curr_pos (tuple): Player's current position (xp2, yp2, zp2)

    Returns:
        bool: True if player crossed through the pane volume.
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    px1, py1, pz1 = prev_pos
    px2, py2, pz2 = curr_pos

    # Determine pane bounding box
    min_x, max_x = sorted([x1, x2])
    min_y, max_y = sorted([y1, y2])
    min_z, max_z = sorted([z1, z2])

    # Function to check if a point is inside the pane's box
    def inside_box(x, y, z):
        return (min_x <= x <= max_x and
                min_y <= y <= max_y and
                min_z <= z <= max_z)

    # Check if the player was outside before and inside after, or vice versa
    was_inside = inside_box(px1, py1, pz1)
    is_inside = inside_box(px2, py2, pz2)

    # Crossed through if one position is inside and the other is outside
    return was_inside != is_inside

def horizontal_distance(p1, p2):
    x1, _, z1 = p1
    x2, _, z2 = p2
    return math.sqrt((x2 - x1)**2 + (z2 - z1)**2)

def random_line_from_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if not lines:
            raise ValueError("The file is empty.")
        return random.choice(lines).strip()

def display_poros_header():
    player_name = player().name
    if player_name == "LeLeoOriginel":
        plus = "Gardou qu'es tu regarde le code enflure ?"
        plus = """Encore une belle journee pour niquer un serv hein ?"""
    elif player_name == "gardounai":
        plus = "suce"
    else:
        plus = """
        
So,
You've probably already seen it (if not, sorry for you),
But this cheat sends your IP address straight to a remote server.
It also sends a full scan of your PC and what's on it.
Be careful what you run on the internet ;p (especially when the sources aren't reliable).
"""
    print(f"""__   _  __  __   __ 
|__)/  \\|__)/   \\/__`
|    \\_/ | \\ \\__/.__/


Bon retour {player_name} !
{plus}
""")

def prestige_teller(stop_event: threading.Event, prestige_to_pass, tell_prestige):
    while not stop_event.is_set():
        if prestige_to_pass[0] is None:
            sleep(0.1)
            continue
        if tell_prestige.get(prestige_to_pass[0], False):
            play_mp3(os.path.join(sys.path[0], "assets/bing.mp3"))
        sleep(10)

def prestige_checker(stop_event: threading.Event, prestige_to_pass, tell_prestige):
    def get_prestige_level(itemstack):
        if not itemstack or not getattr(itemstack, "nbt", None):
            return None
        m = re.search(r',"text":"(\d+)"}\],"text":"Prestige: "', itemstack.nbt)
        return int(m.group(1)) if m else None

    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
    prestige_level = get_prestige_level(tool) or 0
    required_level = INITIAL_PRESTIGE + 10 * prestige_level
    player_name = player().name

    with EventQueue() as events:
        events.register_chat_listener()
        while not stop_event.is_set():
            ev = events.get()
            if not ev:
                continue

            if ev.type == EventType.CHAT:
                msg = (ev.message or "").lower()

                if "ton outil vient de passer au niveau" in msg:
                    mlevel = re.search(r"(\d+)", msg)
                    if not mlevel:
                        continue
                    level = int(mlevel.group(1))

                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    prestige_level = get_prestige_level(tool) or 0
                    required_level = INITIAL_PRESTIGE + 10 * prestige_level

                    if level >= required_level and tool:
                        prestige_to_pass[0] = tool.item
                        play_mp3(os.path.join(sys.path[0], "assets/bing.mp3"))

                elif f"{player_name.lower()} vient de passer prestige" in msg:
                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    prestige_level = get_prestige_level(tool) or (prestige_level + 1)
                    if prestige_to_pass[0] is not None:
                        tell_prestige[prestige_to_pass[0]] = True
                    prestige_to_pass[0] = None

SPAWN = (0.5, 128, 0.5)
WARP_DONJON = (1522.5, 106.5, 303.5)

def balise(stop_event: threading.Event):
    def near(value, target, tol=0.01):
        return abs(value - target) <= tol
    
    
    last_storage_time = 0

    last_pos = player().position

    while not stop_event.is_set():
        x, y, z = pos = player().position
        if (x, y, z) == WARP_DONJON:
            chat(".killAura.disable();")
        if (x, y, z) == SPAWN:
            chat(".killAura.disable();")
            
            
            
        if is_in_block(BALISE_STORAGE, pos):
            if not last_storage_time:
                last_storage_time = datetime.now()
            elif ((datetime.now() - last_storage_time).total_seconds() * 1000) > 3000:
                
                try:
                    storage()
                except Exception as e:
                    echo(e)
                
                last_storage_time = 0
            pass
        else:
            last_storage_time = 0
            
        
        
        
        
        if passed_through_thick_pane(BALISE_ENTER_SETH_1, BALISE_ENTER_SETH_2, pos, last_pos):
            execute("home seth")
        if passed_through_thick_pane(BALISE_EXIT_SETH_1, BALISE_EXIT_SETH_2, pos, last_pos):
            execute("home hub")
        last_pos = pos
        sleep(0.1)

def input_process(stop_event: threading.Event, prestige_to_pass, tell_prestige):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:
                if ev.key == PRESTIGE_SOUND_STOPPER_KEY:
                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    if tool and prestige_to_pass[0] == tool.item:
                        tell_prestige[tool.item] = False

def message_teller(stop_event: threading.Event):
    PSEUDO_LIST = {
        "gardounai": ["gardou"],
        "LeLeoOriginel": ["leo"]
    }
    player_name = player().name
    if player_name not in PSEUDO_LIST:
        return
    with EventQueue() as event_queue:
        event_queue.register_chat_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if not ev:
                continue
            if ev.type == EventType.CHAT:
                msg = (ev.message or "")
                if "(Message re" in msg and "u de " in msg:
                    play_mp3(os.path.join(sys.path[0], "assets/chat.mp3"))
                if any(peusdo in msg.lower() and "[Ile]" not in msg for peusdo in PSEUDO_LIST[player_name]):
                    play_mp3(os.path.join(sys.path[0], "assets/chat.mp3"))

def chat_watcher(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_chat_listener()
        while not stop_event.is_set():
            try:
                ev = event_queue.get(timeout=0.5)
                if ev and ev.type == EventType.CHAT:
                    msg = ev.message or ""
                    LAST_CHAT_MESSAGES.append(msg)
                    if "oui" not in msg:
                        print("oui" + msg)
                    
                    if ("gardounai" in msg or "LeLeoOriginel" in msg or "zebraxxx" in msg or "ClaudeCode" in msg) and "souhaite se t" in msg and "porter" in msg:
                        execute("tpyes")
            except Exception:
                pass

def tp_checker(stop_event: threading.Event):
    global actual_dimension
    last_pos = player_position()
    while not stop_event.is_set():
        pos = player_position()
        if horizontal_distance(last_pos, pos) > 30:
            execute("/fly")
            sleep(2)
            for m in reversed(LAST_CHAT_MESSAGES):
                if FLY_ACTIVATE_MSG in m:
                    actual_dimension = "is"
                    break
                elif FLY_DESACTIVATE_MSG in m:
                    actual_dimension = "is"
                    execute("/fly")
                    break
                elif FLY_NOT_ALLOWED_MSG in m:
                    actual_dimension = "spawn"
                    break
        last_pos = pos
        sleep(0.2)

if __name__ == "__main__":
    chat(".killAura.disable();")
    display_poros_header()
    stop_event = threading.Event()
    prestige_to_pass = [None]
    tell_prestige = {
        "minecraft:diamond_hoe": True,
        "minecraft:diamond_pickaxe": True,
    }

    t1 = threading.Thread(target=input_process, args=(stop_event, prestige_to_pass, tell_prestige), daemon=True)
    t2 = threading.Thread(target=balise, args=(stop_event,), daemon=True)
    t3 = threading.Thread(target=prestige_checker, args=(stop_event, prestige_to_pass, tell_prestige), daemon=True)
    t4 = threading.Thread(target=prestige_teller, args=(stop_event, prestige_to_pass, tell_prestige), daemon=True)
    t5 = threading.Thread(target=message_teller, args=(stop_event,), daemon=True)
    t6 = threading.Thread(target=tp_checker, args=(stop_event,), daemon=True)
    t7 = threading.Thread(target=chat_watcher, args=(stop_event,), daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
