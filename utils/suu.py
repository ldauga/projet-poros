from time import sleep

from system.lib.minescript import container_get_items


sleep(1)


inv = container_get_items()

print([item.slot for item in inv])