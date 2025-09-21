from minescript import (player_inventory, EventQueue, EventType, execute, flush)
import time

STOP_KEY = 259 # BACKSPACE

def main():


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
                
                if len([item for item in inv if item.item == "minecraft:wheat"]) >= 20:
                    execute("/sell all")
                    time.sleep(0.3)
                    # flush()


print('Seller running')
main()    

print('Finished')




