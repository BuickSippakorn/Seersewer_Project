import random
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
game_is_on = True
user_list = []

def create_board(alphabet,length,bomb_number):
    # Creating Position Dictionary
    core_dict = {}
    for i in alphabet:
        for j in range(length):
            core_dict[f"{i}{j}"] = "  "
            
    # Random Bomb Position
    key_list = list(core_dict.keys())
    bomb_position = random.sample(key_list,bomb_number)
    for pos in bomb_position:
        core_dict[pos] = '🕳️'
    return core_dict

def display_board(core,length,user_list):
    n = 0
    while n < len(core):
        for key in core:
            if n % length == 0:
                print()
            if str(key) in user_list:
                print(core[key],end='  ')
            else:
                print(key,end="  ")
            n += 1

# Main Loop
game_pos = create_board(alphabet,16,41)

while game_is_on:
    print('\n' * 2)
    user = input("Select your Tile: ")
    if user == "off":
        game_is_on = False

    user_list.append(user)

    # User Interaction and Creating Map
    display_board(game_pos,16,user_list)

    print('\n' * 2)

    # Game Over Condition
    if game_pos[user] == "🕳️":
        print("\nGame over! You fall into the sewer!")
        game_is_on = False
