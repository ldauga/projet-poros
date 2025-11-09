from time import sleep, time
from typing import List
from constant.StorageConfig import STORAGE_CONFIG
import constant.home as HOME_CONSTANT
from system.lib.minescript import ItemStack, echo, player_inventory
from itertools import groupby

def filter_inventory(inventory: List[ItemStack]):
    """
    exclude the off-hand item and the armor items
    """
    return [item for item in inventory if item.slot < 36]


def storage():
    inv = player_inventory()
    inv = filter_inventory(inv)

    storage_matches = []

    for item in inv:
        for config in STORAGE_CONFIG:
            if config.matches(item.nbt):
                storage_matches.append((config, item.slot))
                break

    if not storage_matches:
        echo("[STORAGE]: Rien à ranger.")
        return

    storage_matches.sort(key=lambda s: (tuple(s[0].pos), s[0].tp_zone))

    grouped = {
        pos: {
            zone: [(conf, slot) for conf, slot in group_zone]
            for zone, group_zone in groupby(group_pos, key=lambda s: s[0].tp_zone)
        }
        for pos, group_pos in groupby(storage_matches, key=lambda s: tuple(s[0].pos))
    }

    last_zone = HOME_CONSTANT.GOLDEN
    for pos, zones in grouped.items():
        for zone, pairs in zones.items():
            for config, slot in pairs:
                config.store(last_zone, slot)
                last_zone = zone
    
    
    echo("[Storage]: Finish.")