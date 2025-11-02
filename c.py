import string
from system.lib.minescript import player_get_targeted_entity


print(entity := player_get_targeted_entity())


def has_unprintable_char(s: str) -> bool:
    """Return True if the string contains at least one unprintable character."""
    printable = set(string.printable)
    return any(ch not in printable for ch in s)

if has_unprintable_char(entity.name):
    print("oui")