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
PRESTIGE_SOUND_STOPPER_KEY = 330


def prestige_teller(stop_event: threading.Event, prestige_to_pass, tell_prestige):
    while not stop_event.is_set():
        if prestige_to_pass[0] is None:
            sleep(0.1)
            continue
        if tell_prestige.get(prestige_to_pass[0], False):
            winsound.Beep(400, 500)
        sleep(1)


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

                elif f"{player_name.lower()} vient de passer prestige" in msg:
                    # Recompute after prestige to show correct next target
                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    prestige_level = get_prestige_level(tool) or (prestige_level + 1)
                    print(f"Prochain niveau requis pour prestige: {INITIAL_PRESTIGE + 10 * (prestige_level + 1)}.")
                    if prestige_to_pass[0] is not None:
                        tell_prestige[prestige_to_pass[0]] = True  # <-- fixed key
                    prestige_to_pass[0] = None


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


def input_process(stop_event: threading.Event, tell_prestige):
    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        while not stop_event.is_set():
            ev = event_queue.get()
            if ev and ev.type == EventType.KEY and ev.action == 1:  # key down
                if ev.key == PRESTIGE_SOUND_STOPPER_KEY:
                    tool = next((item for item in player_inventory() if item.item in POSSIBLE_TOOL), None)
                    if tool:
                        tell_prestige[tool.item] = False
                    print(ev.key)
                #     stop_event.set()
                #     break


if __name__ == "__main__":
    print("Balise running")
    stop_event = threading.Event()
    prestige_to_pass = [None]

    tell_prestige = {
        "minecraft:diamond_hoe": True,
        "minecraft:diamond_pickaxe": True,
    }

    t1 = threading.Thread(target=input_process, args=(stop_event, tell_prestige), daemon=True)
    t2 = threading.Thread(target=main, args=(stop_event,), daemon=True)  # <-- tuple!
    t3 = threading.Thread(target=prestige_checker, args=(stop_event, prestige_to_pass, tell_prestige), daemon=True)
    t4 = threading.Thread(target=prestige_teller, args=(stop_event, prestige_to_pass, tell_prestige), daemon=True)

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
