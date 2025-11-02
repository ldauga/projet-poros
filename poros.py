import math
import os
import random
import re
import sys
import threading
import winsound
from time import sleep

from avast import distance_between_points
from pygame_loader import play_mp3
from system.lib.minescript import EventQueue, EventType, chat, echo, execute, flush, player, player_inventory, player_position
from collections import deque

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



def horizontal_distance(p1, p2):
    """
    Compute the horizontal distance between two 3D points on the XZ plane.

    Parameters:
        p1, p2: tuples or lists of length 3 (x, y, z)

    Returns:
        float: horizontal distance between the two points
    """
    x1, _, z1 = p1
    x2, _, z2 = p2
    return math.sqrt((x2 - x1)**2 + (z2 - z1)**2)

def random_line_from_file(path: str) -> str:
    """Return a random line from a text file."""
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
        # plus = random_line_from_file(os.path.join(sys.path[0], "msg.txt"))
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
            play_mp3(os.path.join(sys.path[0], "bing.mp3"))

        sleep(10)


def prestige_checker(stop_event: threading.Event, prestige_to_pass, tell_prestige):
    def get_prestige_level(itemstack):
        if not itemstack or not getattr(itemstack, "nbt", None):
            return None
        m = re.search(r',"text":"(\d+)"}\],"text":"Prestige: "', itemstack.nbt)
        return int(m.group(1)) if m else None

    # initial state
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
                        play_mp3(os.path.join(sys.path[0], "bing.mp3"))

                        

                elif f"{player_name.lower()} vient de passer prestige" in msg:
                    # Recompute after prestige to show correct next target
                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    prestige_level = get_prestige_level(tool) or (prestige_level + 1)
                    print(f"Prochain niveau requis pour prestige: {INITIAL_PRESTIGE + 10 * (prestige_level + 1)}.")
                    if prestige_to_pass[0] is not None:
                        tell_prestige[prestige_to_pass[0]] = True  # <-- fixed key
                    prestige_to_pass[0] = None


def balise(stop_event: threading.Event):
    def near(value, target, tol=0.01):
        return abs(value - target) <= tol

    while not stop_event.is_set():
        x, y, z = player().position
        
        print(x, y, z)
        
        
        if (x, y, z) == (1522.5, 106.5, 303.5):
            chat(".killAura.disable();")

        # if near(y, 111.93750):
        #     execute("/farm")
        #     sleep(0.5)

        # if -38 <= x <= -37 and 13 <= z <= 18 and -4 <= y <= -2:
        #     execute("/farm")
        #     sleep(0.5)

        # if -316 <= x <= -314 and 92 <= y <= 94 and 22 <= z <= 23:
        #     execute("/mine")
        #     sleep(0.5)

        sleep(0.1)

    print("Balise Stopped")


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
                        print(f"You disabled the prestige for the {tool.item}")

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
                    play_mp3(os.path.join(sys.path[0], "chat.mp3"))
                if any(peusdo in msg.lower() and "[Ile]" not in msg for peusdo in PSEUDO_LIST[player_name]):
                    play_mp3(os.path.join(sys.path[0], "chat.mp3"))




def chat_watcher(stop_event: threading.Event):
    """Continuously store the 10 latest chat messages."""
    with EventQueue() as event_queue:
        event_queue.register_chat_listener()
        while not stop_event.is_set():
            try:
                ev = event_queue.get(timeout=0.5)
                if ev and ev.type == EventType.CHAT:
                    msg = ev.message or ""
                    LAST_CHAT_MESSAGES.append(msg)
            except Exception:
                pass

def tp_checker(stop_event: threading.Event):
    last_pos = player_position()
    
    while not stop_event.is_set():
        pos = player_position()
        if horizontal_distance(last_pos, pos) > 10:
            execute("/fly")
            sleep(.3)
            
        #     for m in reversed(LAST_CHAT_MESSAGES):
        #         if FLY_ACTIVATE_MSG in m:
        #             print("A L IS")
        #             break
        #         elif FLY_DESACTIVATE_MSG in m:
        #             print("A L IS")
        #             execute("/fly")
        #             break
        #         elif FLY_NOT_ALLOWED_MSG in m:
        #             print("AU SPAWN")
        #             break
        #         else:
        #             print("nothing")
        
        last_pos = pos
        sleep(0.2)


if __name__ == "__main__":
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
