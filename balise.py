import re
import threading
import winsound
from time import sleep

from system.lib.minescript import EventQueue, EventType, echo, execute, player, player_inventory

STOP_KEY = 333

POSSIBLE_TOOL = [
    "minecraft:diamond_hoe",
    "minecraft:diamond_pickaxe",
]
INITIAL_PRESTIGE = 50



def prestige_teller(stop_event: threading.Event, prestige_to_pass):
    while not stop_event.is_set():
        if prestige_to_pass[0]:
            winsound.Beep(400, 500) 
        sleep(1)


def prestige_checker(stop_event: threading.Event, prestige_to_pass):
    def get_prestige_level(itemstack):
        if not itemstack or not getattr(itemstack, "nbt", None):
            return None
        m = re.search(r',"text":"(\d+)"}\],"text":"Prestige: "', itemstack.nbt)
        return int(m.group(1)) if m else None
    
    
    
    tool = next(
        (item for item in player_inventory() if item.item in POSSIBLE_TOOL),
        None,
    )
    prestige_level = get_prestige_level(tool) or 0
    
    required_level = INITIAL_PRESTIGE + 10 * (prestige_level)
    
    
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

                    tool = next(
                        (item for item in player_inventory() if item.item in POSSIBLE_TOOL),
                        None,
                    )
                    prestige_level = get_prestige_level(tool) or 0

                    required_level = INITIAL_PRESTIGE + 10 * prestige_level

                    if level >= required_level:
                        prestige_to_pass[0] = True
                elif f"{player_name.lower()} vient de passer prestige" in msg:
                    
                    print(f"Prochain niveau requis pour prestige: {INITIAL_PRESTIGE + 10 * (prestige_level + 1)}.")
                    
                    prestige_to_pass[0] = False



def main(stop_event: threading.Event):
    def near(value, target, tol=0.01):
        return abs(value - target) <= tol

    while not stop_event.is_set():
        x, y, z = player().position

        if near(y, 111.93750):
            execute("/farm")
            sleep(0.5)

        if -38 <= x <= -37 and 13 <= z <= 18 and -4 <= y <= -2:
            execute("/farm")
            sleep(0.5)

        if -316 <= x <= -314 and 92 <= y <= 94 and 22 <= z <= 23:
            execute("/mine")
            sleep(0.5)

        sleep(0.1)

    print("Balise Stopped")


if __name__ == "__main__":
    print("Balise running")
    stop_event = threading.Event()
    prestige_to_pass = [False]

    # t1 = threading.Thread(target=kill_process, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)
    t3 = threading.Thread(target=prestige_checker, args=(stop_event, prestige_to_pass), daemon=True)
    t4 = threading.Thread(target=prestige_teller, args=(stop_event, prestige_to_pass), daemon=True)

    # t1.start()
    t2.start()
    t3.start()
    t4.start()

    # t1.join()
    t2.join()
    t3.join()
    t4.join()
