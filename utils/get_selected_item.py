from system.lib.minescript import player_inventory


def get_selected_item():
    inv = player_inventory()
    
    return next((item for item in inv if item.selected), None)





def main():
    print(get_selected_item())



if __name__ == "__main__":
    main()