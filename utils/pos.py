# import pyperclip

from system.lib.minescript import player_get_targeted_block
from pyperclip import copy

def main():
    block = player_get_targeted_block()
    if block:
        coords = f"{tuple(i for i in block.position)}"
        copy(coords)
        print(f"Copied block coordinates to clipboard: {coords}")
    else:
        print("No block targeted.")

if __name__ == "__main__":
    main()