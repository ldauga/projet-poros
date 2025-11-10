from time import sleep, time
from typing import List, Union

from pyautogui import click, keyDown, keyUp, moveTo, press

from Class import Home

from constant.inventory_coordinate import POS_BY_SLOTS_DOUBLE_CHEST
from system.lib.minescript import container_get_items, execute, player_look_at


class StorageLocation:
    def __init__(
        self,
        name: str,
        pos: Union[int, List[tuple]],
        patterns: Union[str, List[str]],
        tp_zone: Home,
        exclude_patterns: Union[str, List[str]] = None,
    ):
        self.name = name
        self.pos = [pos] if isinstance(pos, tuple) else pos
        self.patterns = [patterns] if isinstance(patterns, str) else patterns
        self.tp_zone = tp_zone
        self.exclude_patterns = [exclude_patterns] if isinstance(exclude_patterns, str) else exclude_patterns

    def matches(self, text: str) -> bool:
        if self.exclude_patterns:
            return all((pattern in text) for pattern in self.patterns) and not any((pattern in text) for pattern in self.exclude_patterns)
        return all((pattern in text) for pattern in self.patterns)

    def _open_chest(self, chest_pos, timeout=5.0):
        player_look_at(*chest_pos)
        sleep(.1)
        click(button="secondary")
        
        start = time()
        while True:
            inv = container_get_items()
            if inv:
                return [item for item in inv if item.slot <= 54]
            
            if time() - start > timeout:
                raise TimeoutError(f"Impossible d ouvrir le coffre apres {timeout} secondes.")
            
            sleep(0.3)


    def store(self, last_zone: Home, slot: int):
        if last_zone.name != self.tp_zone.name:
            self.tp_zone.tp()
            sleep(.2)
            
        
        
        for pos in self.pos:
            inv = self._open_chest(pos)
            
            if len(inv) < 54:
                
                moveTo(*POS_BY_SLOTS_DOUBLE_CHEST[slot])
                sleep(.3)
                keyDown('shift')
                click()
                keyUp('shift')
                sleep(.2)
                press("Escape")
                sleep(.3)
                
                
            
                break
            
            press("Escape")
            sleep(.1)
        
            

    def __repr__(self):
        return f"<TargetZone pos={self.pos}, patterns={self.patterns}, tp_zone='{self.tp_zone}'>"

