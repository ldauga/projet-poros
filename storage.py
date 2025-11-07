from time import sleep, time
from typing import List, Union
import unicodedata

from pyautogui import click, keyDown, keyUp, moveTo, press

import constant.home as HOME_CONSTANT
from constant.inventory_coordinate import POS_BY_SLOTS
import constant.storage as STORAGE_CONSTANT
import constant.colors as COLORS_CONSTANT
from system.lib.minescript import ItemStack, container_get_items, execute, player_inventory, player_look_at


class TargetZone:
    def __init__(
        self,
        name: str,
        pos: Union[int, List[tuple]],
        patterns: Union[str, List[str]],
        tp_zone: str,
        exclude_patterns: Union[str, List[str]] = None,
    ):
        # Normalize to lists for consistent handling
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
                return [item for item in inv if item.slot != 81]
            
            if time() - start > timeout:
                raise TimeoutError(f"Impossible d'ouvrir le coffre après {timeout} secondes.")
            
            sleep(0.1)

        
        


    def store(self, last_zone, slot):
        if last_zone != self.tp_zone:
            execute(self.tp_zone)
            sleep(.3)
        
        
        for pos in self.pos:
            inv = self._open_chest(pos)
            print(len(inv))
            
                            
                
            
            # for item in inv:
            #     print(item.slot)
            
            if len(inv) < 54:
                
                
                moveTo(*POS_BY_SLOTS[slot])
                sleep(.3)
                keyDown('shift')
                click()
                keyUp('shift')
                sleep(.3)
                press("Escape")
                sleep(.3)
                
                
            
                break
            
            press("Escape")
            sleep(.1)
        
            

    def __repr__(self):
        return f"<TargetZone pos={self.pos}, patterns={self.patterns}, tp_zone='{self.tp_zone}'>"



STORAGE_CONFIG = [
    # GOLDEN
    
    # LIGNE 1
    TargetZone("SAC_POINT_FARM", STORAGE_CONSTANT.CHEST_SAC_POINT_FARM, "Sac de points farm", HOME_CONSTANT.GOLDEN),
    
    TargetZone("BOITE_BOOST", STORAGE_CONSTANT.CHEST_BOITE_BOOST, ["Boite", "boosts"], HOME_CONSTANT.GOLDEN),
    
    TargetZone("BOITES_PETS", STORAGE_CONSTANT.CHEST_BOITES_PETS, ["Boite", "familiers"], HOME_CONSTANT.GOLDEN, exclude_patterns="bonbons"),
    
    TargetZone("RUNES_OUTILS", STORAGE_CONSTANT.CHEST_RUNES_OUTILS, "farmdariaomnitool:rune_id", HOME_CONSTANT.GOLDEN),
    TargetZone("SAC_RUNES_OUTILS", STORAGE_CONSTANT.CHEST_RUNES_OUTILS, "Sac de Runes", HOME_CONSTANT.GOLDEN),
    
    
    # LIGNE 2
    TargetZone("SAC_AMES", STORAGE_CONSTANT.CHEST_SAC_AMES, ["Sac d", "mes"], HOME_CONSTANT.GOLDEN),
    
    TargetZone("ARMES", STORAGE_CONSTANT.CHEST_ARMES, ["minecraft:", "sword"], HOME_CONSTANT.GOLDEN),
    TargetZone("ARMES", STORAGE_CONSTANT.CHEST_ARMES, "minecraft:bow", HOME_CONSTANT.GOLDEN),
    
    TargetZone("PETS_LEGENDAIRE", STORAGE_CONSTANT.CHEST_PETS, ["companions:pet-id", COLORS_CONSTANT.LEGENDARY], HOME_CONSTANT.GOLDEN),
    TargetZone("PETS_MYTHIQUE", STORAGE_CONSTANT.CHEST_PETS, ["companions:pet-id", COLORS_CONSTANT.MYTHIQUE], HOME_CONSTANT.GOLDEN),
    
    TargetZone("RUNE_COMBAT", STORAGE_CONSTANT.CHEST_RUNES_COMBATS, "Glisse sur un objet pour appliquer", HOME_CONSTANT.GOLDEN),
    
    # LIGNE 3
    TargetZone("ARMURES_BOOTS", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:diamond_boots", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_LEGGINGS", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:diamond_leggings", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_CHESTPLATE", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:diamond_chestplate", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_HELMET", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:diamond_helmet", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_NETHERITE_BOOTS", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:netherite_boots", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_NETHERITE_LEGGINGS", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:netherite_leggings", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_NETHERITE_CHESTPLATE", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:netherite_chestplate", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_NETHERITE_HELMET", STORAGE_CONSTANT.CHEST_ARMURES_DONJON, "minecraft:netherite_helmet", HOME_CONSTANT.GOLDEN),
        
    TargetZone("ARMURES_FARM_BOOTS", STORAGE_CONSTANT.CHEST_ARMURES_FARM, "minecraft:leather_boots", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_FARM_LEGGINGS", STORAGE_CONSTANT.CHEST_ARMURES_FARM, "minecraft:leather_leggings", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_FARM_CHESTPLATE", STORAGE_CONSTANT.CHEST_ARMURES_FARM, "minecraft:leather_chestplate", HOME_CONSTANT.GOLDEN),
    TargetZone("ARMURES_FARM_MASQUE", STORAGE_CONSTANT.CHEST_ARMURES_FARM, "Masque de ", HOME_CONSTANT.GOLDEN),
    
    
    # LIGNE 4
    TargetZone("CLEF_FRAGMENTEE_LEGENDAIRE", STORAGE_CONSTANT.CHEST_CLEF_LEG_COSMETIQUE, ["gendaire", "Assemble six fragments pour"], HOME_CONSTANT.GOLDEN),
    TargetZone("CLEF_FRAGMENTEE_COSMETIQUE", STORAGE_CONSTANT.CHEST_CLEF_LEG_COSMETIQUE, ["Cosm", "tiques", "Assemble six fragments pour"], HOME_CONSTANT.GOLDEN),
    
    TargetZone("CLEF_DONJON", STORAGE_CONSTANT.CHEST_CLEF_DONJON, ["Assemble six fragments pour", "de donjon"], HOME_CONSTANT.GOLDEN),
    TargetZone("CLEF_HALLOWEEN", STORAGE_CONSTANT.CHEST_CLEF_DONJON, ["Assemble fix fragments pour", "halloween"], HOME_CONSTANT.GOLDEN),
    
    # LIGNE 5
    TargetZone("CLEF_FRAGMENTEE_EPIQUE", STORAGE_CONSTANT.CHEST_CLEF_EPIC, ["Epique", "Assemble six fragments pour"], HOME_CONSTANT.GOLDEN),
    
    TargetZone("SLOT_GENERATEUR", STORAGE_CONSTANT.CHEST_SLOT_GENS, ["Slot de g", "rateur"], HOME_CONSTANT.GOLDEN),
    
    # LIGNE 6
    TargetZone("CLEF_FRAGMENTEE_RARE", STORAGE_CONSTANT.CHEST_CLEF_RARE, ["Rare", "Assemble six fragments pour"], HOME_CONSTANT.GOLDEN),
    
    TargetZone("POTION_DONJON", STORAGE_CONSTANT.CHEST_POTION_DONJON, ["Consomme cette potion", "afin de r"], HOME_CONSTANT.GOLDEN),
    
     
    
    # JETONS
    
    TargetZone("SAC_JETON_COMMUN", [STORAGE_CONSTANT.CHEST_JETON_T1_1, STORAGE_CONSTANT.CHEST_JETON_T1_2, STORAGE_CONSTANT.CHEST_JETON_T1_3], ["Sac de jetons", COLORS_CONSTANT.COMMUN], HOME_CONSTANT.JETON),
    TargetZone("SAC_JETON_PEU_COMMUN", [STORAGE_CONSTANT.CHEST_JETON_T2_1, STORAGE_CONSTANT.CHEST_JETON_T2_2, STORAGE_CONSTANT.CHEST_JETON_T2_3], ["Sac de jetons", COLORS_CONSTANT.PEU_COMMUN], HOME_CONSTANT.JETON),
    TargetZone("SAC_JETON_RARE", [STORAGE_CONSTANT.CHEST_JETON_T3_1, STORAGE_CONSTANT.CHEST_JETON_T3_2, STORAGE_CONSTANT.CHEST_JETON_T3_3], ["Sac de jetons", COLORS_CONSTANT.RARE], HOME_CONSTANT.JETON),
    TargetZone("SAC_JETON_EPIC", [STORAGE_CONSTANT.CHEST_JETON_T4_1, STORAGE_CONSTANT.CHEST_JETON_T4_2, STORAGE_CONSTANT.CHEST_JETON_T4_3], ["Sac de jetons", COLORS_CONSTANT.EPIC], HOME_CONSTANT.JETON),
    TargetZone("SAC_JETON_MYTHIQUE", [STORAGE_CONSTANT.CHEST_JETON_T4_1, STORAGE_CONSTANT.CHEST_JETON_T4_2, STORAGE_CONSTANT.CHEST_JETON_T4_3], ["Sac de jetons", COLORS_CONSTANT.MYTHIQUE], HOME_CONSTANT.JETON),
    
    
    
    # XP
    
    TargetZone("SAC_XP_COMMUN", [STORAGE_CONSTANT.CHEST_XP_T1_1, STORAGE_CONSTANT.CHEST_XP_T1_2, STORAGE_CONSTANT.CHEST_XP_T1_3], ["EXP Outil", COLORS_CONSTANT.COMMUN], HOME_CONSTANT.XP),
    TargetZone("SAC_XP_PEU_COMMUN", [STORAGE_CONSTANT.CHEST_XP_T2_1, STORAGE_CONSTANT.CHEST_XP_T2_2, STORAGE_CONSTANT.CHEST_XP_T2_3], ["EXP Outil", COLORS_CONSTANT.PEU_COMMUN], HOME_CONSTANT.XP),
    TargetZone("SAC_XP_RARE", [STORAGE_CONSTANT.CHEST_XP_T3_1, STORAGE_CONSTANT.CHEST_XP_T3_2, STORAGE_CONSTANT.CHEST_XP_T3_3], ["EXP Outil", COLORS_CONSTANT.RARE], HOME_CONSTANT.XP),
    TargetZone("SAC_XP_EPIC", [STORAGE_CONSTANT.CHEST_XP_T4_1, STORAGE_CONSTANT.CHEST_XP_T4_2, STORAGE_CONSTANT.CHEST_XP_T4_3], ["EXP Outil", COLORS_CONSTANT.EPIC], HOME_CONSTANT.XP),
    TargetZone("SAC_XP_MYTHIQUE", [STORAGE_CONSTANT.CHEST_XP_T4_1, STORAGE_CONSTANT.CHEST_XP_T4_2, STORAGE_CONSTANT.CHEST_XP_T4_3], ["EXP Outil", COLORS_CONSTANT.MYTHIQUE], HOME_CONSTANT.XP),
    
    
    # COGS
    
    TargetZone("COGS_COMMUN", [STORAGE_CONSTANT.CHEST_COGS_T1_1, STORAGE_CONSTANT.CHEST_COGS_T1_2, STORAGE_CONSTANT.CHEST_COGS_T1_3], ["Clique droit sur ton g", COLORS_CONSTANT.COMMUN], HOME_CONSTANT.COGS),
    TargetZone("COGS_PEU_COMMUN", [STORAGE_CONSTANT.CHEST_COGS_T2_1, STORAGE_CONSTANT.CHEST_COGS_T2_2, STORAGE_CONSTANT.CHEST_COGS_T2_3], ["Clique droit sur ton g", COLORS_CONSTANT.PEU_COMMUN], HOME_CONSTANT.COGS),
    TargetZone("COGS_RARE", [STORAGE_CONSTANT.CHEST_COGS_T3_1, STORAGE_CONSTANT.CHEST_COGS_T3_2, STORAGE_CONSTANT.CHEST_COGS_T3_3], ["Clique droit sur ton g", COLORS_CONSTANT.RARE], HOME_CONSTANT.COGS),
    TargetZone("COGS_EPIC", [STORAGE_CONSTANT.CHEST_COGS_T4_1, STORAGE_CONSTANT.CHEST_COGS_T4_2, STORAGE_CONSTANT.CHEST_COGS_T4_3], ["Clique droit sur ton g", COLORS_CONSTANT.EPIC], HOME_CONSTANT.COGS),
    
    
    
    
    
    # PETS
    
    TargetZone("PETS_COMMUN", [STORAGE_CONSTANT.CHEST_PET_T1_1, STORAGE_CONSTANT.CHEST_PET_T1_2, STORAGE_CONSTANT.CHEST_PET_T1_3], ["companions:pet-id", COLORS_CONSTANT.COMMUN], HOME_CONSTANT.PETS),
    TargetZone("PETS_PEU_COMMUN", [STORAGE_CONSTANT.CHEST_PET_T2_1, STORAGE_CONSTANT.CHEST_PET_T2_2, STORAGE_CONSTANT.CHEST_PET_T2_3], ["companions:pet-id", COLORS_CONSTANT.PEU_COMMUN], HOME_CONSTANT.PETS),
    TargetZone("PETS_RARE", [STORAGE_CONSTANT.CHEST_PET_T3_1, STORAGE_CONSTANT.CHEST_PET_T3_2, STORAGE_CONSTANT.CHEST_PET_T3_3], ["companions:pet-id", COLORS_CONSTANT.RARE], HOME_CONSTANT.PETS),
    TargetZone("PETS_EPIC", [STORAGE_CONSTANT.CHEST_PET_T4_1, STORAGE_CONSTANT.CHEST_PET_T4_2, STORAGE_CONSTANT.CHEST_PET_T4_3], ["companions:pet-id", COLORS_CONSTANT.EPIC], HOME_CONSTANT.PETS),
    
    
    
    
    TargetZone("PETS_MYTHIQUE", STORAGE_CONSTANT.CHEST_PETS, ["companions:pet-id", COLORS_CONSTANT.MYTHIQUE], HOME_CONSTANT.GOLDEN),
    
        
        
    
    # BONBON
    
    TargetZone("BONBON_COMMUN", [STORAGE_CONSTANT.CHEST_BONBON_T1_1, STORAGE_CONSTANT.CHEST_BONBON_T1_2, STORAGE_CONSTANT.CHEST_BONBON_T1_3], ["Bonbon de familier", COLORS_CONSTANT.COMMUN], HOME_CONSTANT.BONBON),
    TargetZone("BONBON_PEU_COMMUN", [STORAGE_CONSTANT.CHEST_BONBON_T2_1, STORAGE_CONSTANT.CHEST_BONBON_T2_2, STORAGE_CONSTANT.CHEST_BONBON_T2_3], ["Bonbon de familier", COLORS_CONSTANT.PEU_COMMUN], HOME_CONSTANT.BONBON),
    TargetZone("BONBON_RARE", [STORAGE_CONSTANT.CHEST_BONBON_T3_1, STORAGE_CONSTANT.CHEST_BONBON_T3_2, STORAGE_CONSTANT.CHEST_BONBON_T3_3], ["Bonbon de familier", COLORS_CONSTANT.RARE], HOME_CONSTANT.BONBON),
    TargetZone("BONBON_EPIC", [STORAGE_CONSTANT.CHEST_BONBON_T4_1, STORAGE_CONSTANT.CHEST_BONBON_T4_2, STORAGE_CONSTANT.CHEST_BONBON_T4_3], ["Bonbon de familier", COLORS_CONSTANT.EPIC], HOME_CONSTANT.BONBON),
    TargetZone("BONBON_LEGENDAIRE", [STORAGE_CONSTANT.CHEST_BONBON_T4_1, STORAGE_CONSTANT.CHEST_BONBON_T4_2, STORAGE_CONSTANT.CHEST_BONBON_T4_3], ["Bonbon de familier", COLORS_CONSTANT.LEGENDARY], HOME_CONSTANT.BONBON),
    TargetZone("BONBON_MYTHIQUE", [STORAGE_CONSTANT.CHEST_BONBON_T4_1, STORAGE_CONSTANT.CHEST_BONBON_T4_2, STORAGE_CONSTANT.CHEST_BONBON_T4_3], ["Bonbon de familier", COLORS_CONSTANT.MYTHIQUE], HOME_CONSTANT.BONBON),
    
    TargetZone("BOITE_BONBON", STORAGE_CONSTANT.CHEST_BOITE_BONBON, "Boite de bonbons", HOME_CONSTANT.BONBON),
    


    # THUNE

    TargetZone("SAC_ARGENT", STORAGE_CONSTANT.CHEST_THUNE, ["Sac d", "argent", "une somme"], HOME_CONSTANT.THUNE),
    
    
    
]
    





def filter_inventory(inventory: List[ItemStack]):
    """
    exclude the off-hand item and the armor items
    """
    return [item for item in inventory if item.slot < 36]







def storage():
    inv = player_inventory()
    inv = filter_inventory(inv)
    
    
    
    last_tp_zone = HOME_CONSTANT.GOLDEN
    for item in inv:
        # print(item.slot)
        for config in STORAGE_CONFIG:
            if config.matches(item.nbt):
                
                
                config.store(last_tp_zone, item.slot)

                
                last_tp_zone = config.tp_zone
                
                break
    keyUp('shift')
    

storage()