import random
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']
game_is_on = True
user_list = []

def create_board(alphabet,length,sewer_number):
    # Creating Position Dictionary
    core_dict = {}
    for i in alphabet:
        for j in range(length):
            core_dict[f"{i}{j}"] = "  "
            
    # Random Sewer Position
    key_list = list(core_dict.keys())
    sewer_position = random.sample(key_list,sewer_number)
    for pos in sewer_position:
        core_dict[pos] = '🕳️'
    return core_dict

def create_flag(alphabet, length):
    # Creating Position Dictionary
    core_dict = {}
    for i in alphabet:
        for j in range(length):
            core_dict[f"{i}{j}"] = False
    return core_dict

def create_number(board, length):
    # Count number around point
    node = [(-1,-1), (-1,0), (-1,1),
            ( 0,-1),         ( 0,1),
            ( 1,-1), ( 1,0), ( 1,1)]
    
    for i in range(len(alphabet)):
        for j in range(length):
            pos = f"{alphabet[i]}{j}" # Current position
            if board[pos] != '🕳️':
                count = 0
                # Check around point
                for x,y in node:
                    check_x = i + x
                    check_y = j + y
                    if 0 <= check_x < len(alphabet) and 0 <= check_y < length:
                        now_pos = f"{alphabet[check_x]}{check_y}" # Position want to check
                        if board[now_pos] == '🕳️':
                            count += 1
                board[pos] = count
    return board

def open_chain(board, flag, length, user_list, start):
    # Open value
    if board[start] == '🕳️':
        return board, user_list

    node = [(-1,-1), (-1,0), (-1,1),
            ( 0,-1),         ( 0,1),
            ( 1,-1), ( 1,0), ( 1,1)]
    start_x = alphabet.index(start[0])
    start_y = int(start[1:])

    # BFS
    travel_node = [(start_x,start_y)] # Queue want to FIFO

    while travel_node:
        r, c = travel_node.pop(0) # Pop first value
        pos = f"{alphabet[r]}{c}"
        if pos in user_list: # Check opened??
            continue
        if board[pos] == '🕳️': # Check have sewer??
            continue
        if flag[pos]:
            continue
        user_list.append(pos) # Add to opened

        # If value is 0 travel around
        if board[pos] == 0:
            for x,y in node:
                check_x = r + x
                check_y = c + y
                if 0 <= check_x < len(alphabet) and 0 <= check_y < length:
                    now_pos = f"{alphabet[check_x]}{check_y}" # Position want to check
                    if now_pos not in user_list and board[now_pos] != '🕳️':
                        travel_node.append((check_x,check_y))

def display_board(core,flag,length,user_list):
    n = 0
    while n < len(core):
        for key in core:
            len_key = len(key)
            if n % length == 0:
                print()
            if str(key) in user_list:
                print(f'{core[key]:>{len_key}}',end='  ')
            else:
                if flag[key]:
                    print(f'{"🚧":>{len_key-1}}',end="  ")
                else:
                    print(f'{key:>{len_key}}',end="  ")
            n += 1

def endgame_display(core,length,user_list):
    n = 0
    while n < len(core):
        for key in core:
            if n % length == 0:
                print()
            if str(key) in user_list:
                print(core[key],end='  ')
            else:
                print(core[key],end="  ")
                #print(core[key],end="  ") # Check value
            n += 1

# Main Game
print()
print("""   ______________________________
 / \                             \.
|   |                            |.
 \_ |                            |.
    |                            |.
    |                            |.
    |                            |.
    |                            |.
    |       Before playing 💡    |.
    |                            |.
    |                            |.
    |                            |.
    |                            |.
    |                            |.
    |                            |.
    |   _________________________|___
    |  /                            /.
    \_/____________________________/.""")

print()
print()
while True:
    diff = input("\nPlease select your difficulty!\nEasy: 20 sewers, Normal: 40 sewers, Hard: 50 sewers\n")
    sewer = 0
    if diff == "Easy":
        sewer = 20
        break
    elif diff == "Normal":
        sewer = 40
        break
    elif diff == "Hard":
        sewer = 50
        break
    else:
        print("Please Enter valid difficulty!")
print()
print("There's two action in this game, Open and Flag.\n" \
"Open them if you think there is no SEWER and flag them if you think they had.\n" 
'If you want to change mode simply type "C".')
sewer_total = sewer
sewer_now = 0
game_pos = create_board(alphabet,16,sewer_total)
game_pos = create_number(game_pos,16)
game_pos_flag = create_flag(alphabet,16)
mode = "Open"

while game_is_on:
    
    try:
        print('\n' * 2)
        display_board(game_pos,game_pos_flag,16,user_list)
        print('\n')
        
        user = input(f"Select your Tile ({mode}): ")

        # Change mode
        if user == "C" and mode == "Open":
            mode = "Flag"
            continue
        if user == "C" and mode == "Flag":
            mode = "Open"
            continue

        # Flag
        if mode == "Flag":
            if game_pos_flag[user]:
                game_pos_flag[user] = False
                if game_pos[user] == "🕳️":
                    sewer_now -= 1
            else:
                game_pos_flag[user] = True
                if game_pos[user] == "🕳️":
                    sewer_now += 1
        else:
            if user == "off":
                game_is_on = False
        
            # Open and Edit pos that have 0 near user open
            open_chain(game_pos,game_pos_flag,16,user_list,user)

            # User Interaction and Creating Map
            #display_board(game_pos,game_pos_flag,16,user_list)

            print('\n' * 2)

            # Game Over Condition
            if game_pos[user] == "🕳️" and not game_pos_flag[user]:
                print("\nGame over! You fall into the sewer!")
                endgame_display(game_pos,16,user_list)
                game_is_on = False
        
        if sewer_now == sewer_total:
            print("Congrats!🎉 You won this game, now you are able to survive in Thailand!💪⚔️")
            game_is_on = False
    
    except KeyError:
        print()
        print("Please enter a tile that is in the board. Try again!")