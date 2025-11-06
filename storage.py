
from time import sleep
from system.lib.minescript import execute, player_look_at


CHEST_SAC_POINT_FARM = (41, 110, -25)
CHEST_BOITE_BOOST = (42, 110, -25)
CHEST_BOITES_PETS = (43, 110, -25)
CHEST_RUNES_OUTILS = (43.2, 110, -25)

CHEST_SAC_AMES = (41, 109.1, -25)
CHEST_ARMES = (42, 109.1, -25)
CHEST_PETS = (43, 109.1, -25)
CHEST_RUNES_COMBATS = (43.2, 109.1, -25)

CHEST_VIDE_1 = (41, 108.9, -25)
CHEST_ARMURES_DONJON = (42, 108.9, -25)
CHEST_ARMURES_MINAGE = (43, 108.9, -25)
CHEST_ARMURES_FARM = (43.2, 108.9, -25)

CHEST_CLEF_LEG_COSMETIQUE = (45.5, 110, -25)
CHEST_CLEF_DONJON = (46, 110, -25)
CHEST_VIDE_2 = (47, 110, -25)
CHEST_VIDE_3 = (48, 110, -25)

CHEST_CLEF_EPIC = (45.5, 109.1, -25)
CHEST_SLOT_GENS = (46, 109.1, -25)
CHEST_VIDE_4 = (48, 109.1, -25)

CHEST_CLEF_RARE = (45.5, 108.9, -25)
CHEST_POTION_DONJON = (46, 108.9, -25)
CHEST_VIDE_5 = (47, 108.9, -25)
CHEST_VIDE_6 = (48, 108.9, -25)





execute("home storage")
sleep(.3)
player_look_at(*CHEST_CLEF_RARE)
sleep(.3)
player_look_at(*CHEST_POTION_DONJON)
sleep(.3)
player_look_at(*CHEST_VIDE_5)
sleep(.3)
player_look_at(*CHEST_VIDE_6)


# def storage():
    