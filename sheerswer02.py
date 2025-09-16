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

def open_chain(board, length, user_list, start):
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
                #print(core[key],end="  ") # Check value
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
# Main Loop
game_pos = create_board(alphabet,16,41)
game_pos = create_number(game_pos,16)

while game_is_on:
    print('\n' * 2)
    user = input("Select your Tile: ")
    if user == "off":
        game_is_on = False
    
    # Open and Edit pos that have 0 near user open
    open_chain(game_pos,16,user_list,user)

    # ตรงนี้ถ้าไม่ใส่ตอนแพ้จะไม่ปริ้นท่อออกมา ใครแก้ได้ช่วยด้วย
    if game_pos[user] == "🕳️":
        user_list.append(user)

    # User Interaction and Creating Map
    display_board(game_pos,16,user_list)

    print('\n' * 2)

    # Game Over Condition
    if game_pos[user] == "🕳️":
        print("\nGame over! You fall into the sewer!")
        endgame_display(game_pos,16,user_list)
        game_is_on = False
