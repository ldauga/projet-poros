import random
from minescript import (player_inventory, EventQueue, EventType, execute, flush)
import time

STOP_KEY = 259 # BACKSPACE

def main():
    
    next_goal = 4


    with EventQueue() as event_queue:
        event_queue.register_key_listener()
        event_queue.register_block_update_listener()
        while True:
            event = event_queue.get()
            if event.type == EventType.KEY:
                if event.key != STOP_KEY:
                    continue
                return

            if event.type == EventType.BLOCK_UPDATE:
                inv = player_inventory()
                
                
                if sum([item.count for item in inv if item.item == "minecraft:wheat"]) >= next_goal:
                    next_goal = random.randint(128, 384)
                    execute("/condense")
                    time.sleep(0.3)
                    # flush()
                elif sum([item.count for item in inv if item.item == "minecraft:paper"]) >= 1280:
                    execute("/sellall")
                    time.sleep(0.3)


print('Seller running')
main()    

print('Finished')




