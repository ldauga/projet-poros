import math
import string
import sys
import threading
from time import sleep

import pyautogui
from system.lib.minescript import EventQueue, EventType, chat, entities, execute, player, player_get_targeted_block, player_get_targeted_entity, player_position, player_press_use, player_set_orientation

DATA = {
    # "tuto": {
    #     "start": {"position": "1498 103 339", "orientation": (0, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    "mirage": {
        "start": "1489 104 338",
        "farm": "86 27 -692",
        "boss_tp": "84 28 -605",
        "tp_type": "minecraft:sea_lantern",
        "boss_kill": "",
    },
    
    "maya": {
        "start": "1484 104 329",
        "farm": "1354 16 1758",
        "boss_tp": " 1400 -13 1814",
        "tp_type": "minecraft:sea_lantern",
        "boss_kill": "772 59 -106",
    },


    # },
    # "forteresse": {
    #     "start": {"position": "1485 103 320", "orientation": (90, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    # "manoir": {
    #     "start": {"position": "1485 103 311", "orientation": (90, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    # "crypte": {
    #     "start": {"position": "1485 103 295", "orientation": (90, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
    
    "bunker": {
        "start": "1482 104 286",
        "farm": "517 81 647",
        "boss_tp": "1400 -13 1814",
        "tp_type": "minecraft:sea_lantern",
        "boss_kill": "-353 58 -111",
    },
        

    # },
    # "bunker": {
    #     "start": {"position": "1485 103 286", "orientation": (90, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    # "forge": {
    #     "start": {"position": "1487 103 277", "orientation": (90, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    # "abysse": {
    #     "start": {"position": "1489 103 271", "orientation": (180, -30)},
    #     "farm":,
    #     "boss_tp": {
    #         "position":,
    #         "orientation":,
    #     },
    #     "boss_kill":,
        

    # },
    "event": {
        "start": "1498 104 264",
        "farm": "-385 53 4396",
        "boss_tp": "-385 54 4420",
        "tp_type": "minecraft:red_sandstone_wall",
        # "boss_tp": {
        #     "position":,
        #     "orientation":,
        # },
        # "boss_kill":,
        

    },
}


def click_on_event_tp():

    def colors_are_close(rgb1, rgb2, tolerance=15):
        return all([  (abs(rgb1[index] - rgb2[index]) <= tolerance)   for index in range(3)])

    pyautogui.click(button="secondary")


    target_color = (58, 97, 55)
    region = (710, 240, 490, 340)

    screenshot = pyautogui.screenshot(region=region)

    width, height = screenshot.size
    found = None

    for x in range(width):
        for y in range(height):
            pixel = screenshot.getpixel((x, y))
            if colors_are_close(pixel, target_color):
                found = (region[0] + x, region[1] + y)
                
                pyautogui.moveTo(*found)
                pyautogui.click()
                print(f"Found approximate color at {found} (pixel={pixel})")
                break
        if found:
            break


def check_pos(pos, target):
    return all([target[index] <= pos[index <= target[index]] + 1 for index in range(3)])

def has_unprintable_char(s: str) -> bool:
    """Return True if the string contains at least one unprintable character."""
    printable = set(string.printable)
    return any(ch not in printable for ch in s)


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

def main(stop_event, all_relics):
    if len(sys.argv) < 2:
        print("Enter dungeon type: " + " | ".join(DATA.keys()))
        return
    elif sys.argv[1] not in DATA.keys():
        print("Enter dungeon type: " + " | ".join(DATA.keys()))
        return
    else:
        try:
            dungeon = sys.argv[1]
            execute("warp donjon_" + dungeon.capitalize())
            sleep(2)
            while not stop_event.is_set():
                
                # if not stop_event.is_set():
                #     chat('#goto ' + DATA[dungeon]["start"])
                
                # while not stop_event.is_set():
                #     if (entity := player_get_targeted_entity(3)) and has_unprintable_char(entity.name):
                #         player_press_use(True)
                #         player_press_use(False)
                        
                #         if dungeon == "event":
                #             sleep(1)
                #             click_on_event_tp()
                #         break
                #     sleep(0.1)
                # chat("#stop")
                # sleep(1.5)

                if dungeon != "event":
                    farm_zone = DATA[dungeon]["farm"]
                    tp_zone = DATA[dungeon]["boss_tp"]
                    boss_kill = DATA[dungeon]["boss_kill"]
                else:
                    pos = player().position
                    farm_zone = [-385, 52, pos[2]]
                    farm_zone[2] += 22
                    
                    tp_zone = [farm_zone[0], farm_zone[1], farm_zone[2]]
                    tp_zone[2] += 22
                    farm_zone = " ".join([str(int(i)) for i in farm_zone])
                    tp_zone = " ".join([str(int(i)) for i in tp_zone])
                    
                    
                if not stop_event.is_set():
                    chat("#goto " + farm_zone)
                if not stop_event.is_set():
                    chat(".killAura.enable();")
                
                while not stop_event.is_set() and not all_relics[0]:
                    sleep(3)
                    chat("#goto " + farm_zone)
                chat("#stop")
                chat(".killAura.disable();")
                all_relics[0] = False
                    
                last_pos = player_position()
                while not stop_event.is_set():
                    
                    pos = player().position
                    
                    
                    chat("#set allowBreakAnyway " + DATA[dungeon]["tp_type"])
                    chat("#mine " + DATA[dungeon]["tp_type"])
                    
                    if horizontal_distance(last_pos, pos) > 30:
                        print("TP")
                        break
                    
                    if (block := player_get_targeted_block()) and block.type == DATA[dungeon]["tp_type"]:
                        chat("#stop")
                        player_press_use(True)
                        player_press_use(False)
                        # break
                    sleep(0.1)
                    last_pos = pos
                sleep(2)
                
                kill_aura_enable = False
                last_pos = player_position()
                if not stop_event.is_set():
                    chat(".killAura.enable();")
                
                if dungeon != "event":
                    while not stop_event.is_set():
                        pos = player_position()
                        # if not kill_aura_enable:
                        #     if check_pos(pos, [int(a) for a in boss_kill.split()]):
                        #         kill_aura_enable = True
                        #     # current_entities = entities()
                        
                        if horizontal_distance(last_pos, pos) > 30:
                            print("TP")
                            break
                        if not stop_event.is_set():
                            chat("#goto " + boss_kill)
                        last_pos = pos
                        
                        sleep(1)
                        
                sleep(2)
            
        finally:
            stop_event.set()    
            chat("#stop")
            chat(".killAura.disable();")
    
STOP_KEY = 333

def kill_process(stop_event: threading.Event):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:
                if ev.key == STOP_KEY:
                    print("Stopping")
                    stop_event.set()
                    break



  
def relique_checker(stop_event, all_relics):
    with EventQueue() as event_queue:
        event_queue.register_chat_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if not ev:
                    continue
                
            if ev.type == EventType.CHAT:
                msg = (ev.message or "")
                if "32/32" in msg or "64/64" in msg:
                    all_relics[0] = True
        
if __name__ == "__main__":
    print("DUNGEON running")
    all_relics = [False]
    
    stop_event = threading.Event()

    t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event, all_relics), daemon=True)
    t3 = threading.Thread(target=relique_checker, args=(stop_event, all_relics), daemon=True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

# tp pos /setblock -385 52 5033 minecraft:beacon
# tp pos /setblock -385 52 5252 minecraft:beacon