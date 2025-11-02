import string
import sys
import threading
from time import sleep

import pyautogui
from system.lib.minescript import EventQueue, EventType, chat, entities, execute, player, player_get_targeted_block, player_get_targeted_entity, player_press_use, player_set_orientation

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
        "boss_kill": "",
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
        "tp_type": "minecraft:carved_pumpkin",
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



all_relics = [False]

def has_unprintable_char(s: str) -> bool:
    """Return True if the string contains at least one unprintable character."""
    printable = set(string.printable)
    return any(ch not in printable for ch in s)


def main(stop_event, all_relics):
    if len(sys.argv) < 2:
        print("Enter dungeon type: " + " | ".join(DATA.keys()))
        return
    else:
        try:
            execute("donjon")
            sleep(1)
            dungeon = sys.argv[1]
            
            chat('#goto ' + DATA[dungeon]["start"])
            
            while not stop_event.is_set():
                if (entity := player_get_targeted_entity(3)) and has_unprintable_char(entity.name):
                    player_press_use(True)
                    player_press_use(False)
                    
                    if dungeon == "event":
                        sleep(.3)
                        click_on_event_tp()
                    break
                sleep(0.1)
            chat("#stop")
            sleep(1.5)

            if dungeon != "event":
                farm_zone = DATA[dungeon]["farm"]
                tp_zone = DATA[dungeon]["boss_tp"]
            else:
                pos = player().position
                farm_zone = [-385, 52, pos[2]]
                farm_zone[2] += 22
                print(farm_zone)
                
                tp_zone = [farm_zone[0], farm_zone[1], farm_zone[2]]
                tp_zone[2] += 22
                farm_zone = " ".join([str(int(i)) for i in farm_zone])
                tp_zone = " ".join([str(int(i)) for i in tp_zone])
                
                
            chat("#goto " + farm_zone)
            
            chat(".killAura.enable();")
            while not stop_event.is_set() and not all_relics[0]:
                sleep(3)
                chat("#goto " + farm_zone)
                
            # chat(".killAura.disable();")
            all_relics[0] = False
            chat("#goto " + tp_zone)
            while not stop_event.is_set():
                if (block := player_get_targeted_block()) and block.type == DATA[dungeon]["tp_type"]:
                    player_press_use(True)
                    player_press_use(False)
                    break
                sleep(0.1)
            
            
            if dungeon != "event":
                while not stop_event.is_set():
                    current_entities = entities()
                    
                    print(current_entities)
                    
                    sleep(0.1)
                    
                
            
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