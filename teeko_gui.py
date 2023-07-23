import pygame
import random 
import copy

# pieces
ai_piece = random.choice(['R', 'B'])
player_piece = 'R' if ai_piece == 'B' else 'B'
# AI's functions
def make_move(state, num_piece):
    """ Selects a (row, col) space for the next move. You may assume that whenever
    this function is called, it is this player's turn to move.

    Args:
        state (list of lists): should be the current state of the game as saved in
            this TeekoPlayer object. Note that this is NOT assumed to be a copy of
            the game state and should NOT be modified within this method (use
            place_piece() instead). Any modifications (e.g. to generate successors)
            should be done on a deep copy of the state.

            In the "drop phase", the state will contain less than 8 elements which
            are not ' ' (a single space character).

    Return:
        move (list): a list of move tuples such that its format is[(row, col), (source_row, source_col)]
            where the (row, col) tuple is the location to place a piece and the
            optional (source_row, source_col) tuple contains the location of the
            piece the AI plans to relocate (for moves after the drop phase). In
            the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
        and will eventually take over the board. This is not a valid strategy and
        will earn you no points.
        """
       
    # determine if it is drop phase or not
    drop_phase = True if num_piece < 8 else False  
        
    # select an unoccupied space randomly

    # case if it is drop phase
    if drop_phase:
        drop_move = []
        best_state = None
        best_score = None
        # find the best possible state use minimax
        for succ in success(state, ai_piece, num_piece):
            score = max_value(succ, 0, num_piece)
            if best_state == None or score > best_score:
                best_state = succ
                best_score = score
            # find the index of new piece dropped, if old state is ' ' and new state is not' ' , then piece is there.
        row = 0
        col = 0
        for i in range(len(best_state)):
            for j in range(len(best_state[i])):
                if best_state[i][j] != ' ' and state[i][j] == ' ':
                    row = i
                    col = j
        drop_move.append((row, col))
        return drop_move
        
        #(row, col) = (random.randint(0, 4), random.randint(0, 4))
        #while not state[row][col] == ' ':
         #   (row, col) = (random.randint(0, 4), random.randint(0, 4))
        
        # the case if it is not drop phase
    if not drop_phase:
        move = []
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!

            # find the best possible state using minimax.
        best = None
        max_score = None
        for succ in success(state, ai_piece, num_piece):
            score = max_value(succ, 0, num_piece)
            if best == None or score > max_score:
                best = succ
                max_score = score
        # find source point and target point.
        source_row = 0
        source_col = 0
        target_row = 0
        target_col = 0
        for i in range(len(best)):
            for j in range(len(best[i])):
                # if original is empty but new state is taken by piece, then target point
                if state[i][j] == ' ' and best[i][j] == ai_piece:
                    target_row = i
                    target_col = j
                    
                # if original is piece but new state is empty, the source point
                if state[i][j] == ai_piece and best[i][j] == ' ':
                    source_row = i
                    source_col = j

        move.append((source_row, source_col))
        move.insert(0, (target_row, target_col))
        return move
    
def success(state, curr_piece, num_piece):
    """
    Get all the successors of the current state
    param: state: the current state of board, to generate new states. curr_piece: which player's move, r or b
    return: a list of lists of list -  a list of possible states the board could be
    """
    # return value here
    legal_succs = []

    # check if it is in drop phase or not
    drop_phase = True if num_piece < 8 else False

    # if drop phase, just replace one space a time with the current player's piece
    if drop_phase:
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == ' ':
                    tmp = copy.deepcopy(state)
                    tmp[i][j] = curr_piece
                    legal_succs.append(tmp)
                    
    else:
        # if not in drop phase, move each possible piece
        for i in range(len(state)):
            for j in range(len(state[0])):
                # depend on different position, check for different possible position to go to
                if state[i][j] == ai_piece:
                    if i == 0:
                        if j == 0:
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i, j+1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i+1, j], curr_piece))
                            if state[i+1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i+1, j+1], curr_piece))
                        if j > 0 and j < len(state[0]) - 1:
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j-1], curr_piece))
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j+1], curr_piece))
                            if state[i+1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1,j], curr_piece))
                            if state[i+1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j+1], curr_piece))
                        if j == len(state[0]):
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j-1], curr_piece))
                            if state[i+1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j], curr_piece))
                    elif i > 0 and i < len(state) - 1:
                        if j == 0:
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j], curr_piece))
                            if state[i-1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j+1], curr_piece))
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i, j+1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i+1, j], curr_piece))
                            if state[i+1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i+1, j+1], curr_piece))
                        if j > 0 and j < len(state[0]) - 1:
                            if state[i-1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1,j], curr_piece))
                            if state[i-1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1,j+1], curr_piece))
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j-1], curr_piece))
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j+1], curr_piece))
                            if state[i+1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1,j], curr_piece))
                            if state[i+1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j+1], curr_piece))
                        if j == len(state[0]):
                            if state[i-1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1,j-1], curr_piece))
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1,j], curr_piece))
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j-1], curr_piece))
                            if state[i+1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                            if state[i+1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i+1, j], curr_piece))
                    elif i == len(state) - 1:
                        if j == 0:
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i-1, j], curr_piece))
                            if state[i-1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i-1, j+1], curr_piece))
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i, j], [i, j+1], curr_piece))
                        if j > 0 and j < len(state[0]) - 1:
                            if state[i-1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j], curr_piece))
                            if state[i-1][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j+1], curr_piece))
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i,j-1], curr_piece))
                            if state[i][j+1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i,j+1], curr_piece))
                        if j == len(state[0]):
                            if state[i-1][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                            if state[i-1][j] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i-1, j], curr_piece))
                            if state[i][j-1] == ' ':
                                legal_succs.append(get_possible_case(state, [i,j], [i, j-1], curr_piece))
    return legal_succs

def get_possible_case(state, source, to, piece):
    """
    Helper functions return a new case base on source and destination
    param: state - current state of board. source - list of form [x,y] source point. to. list of form [x,y] of destination point. piece - r or b, current player
    return temp - a state where piece moved from source to destination
    """
    temp = copy.deepcopy(state)
    temp[source[0]][source[1]] = ' '
    temp[to[0]][to[1]] = piece
    return temp

def game_value(state):
    """ Checks the current board status for a win condition

    Args:
    state (list of lists): either the current state of the game as saved in
        this TeekoPlayer object, or a generated successor state.

    Returns:
        int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

    TODO: complete checks for diagonal and box wins
    """
    # check horizontal wins
    for row in state:
        for i in range(2):
            if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                return 1 if row[i] == ai_piece else -1

    # check vertical wins
    for col in range(5):
        for i in range(2):
            if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                return 1 if state[i][col] == ai_piece else -1

    # TODO: check \ diagonal wins
    for row in range(2):
        for col in range(2):
            if state[row][col] != ' ':
                if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                    return 1 if state[row][col] == ai_piece else -1
    # TODO: check / diagonal wins
    for row in range(2):
        for col in range(3, 5):
            if state[row][col] != ' ':
                if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    return 1 if state[row][col] == ai_piece else -1

    # TODO: check box wins
    for row in range(4):
        for col in range(4):
            if state[row][col] != ' ':
                if state[row][col] == state[row][col + 1] == state[row+1][col] == state[row+1][col+1]:
                    return 1 if state[row][col] == ai_piece else -1
    return 0  # no winner yet

def heuristic_game_value(state):
    """
    Evaluate the game heuristically by calculating the distances between pieces.
    param: state, the current state of the game
    return: a value between -1 and 1 indicating the distance between pieces.
    """
    if game_value(state) == -1 or game_value(state) == 1:
        return game_value(state)
    index_ai = []
    index_opp = []
    # find index where ai's piece is and opponents piece is at
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != ' ':
                piece = state[i][j]
                if piece == ai_piece:
                    index_ai.append([i,j])
                else:
                    index_opp.append([i,j])

    # evaluate AI's distance 
    ai_dist_score = 0
    count_ai = 6 # a total of 6 comparison
    for i in range(len(index_ai)):
        for j in range(i, len(index_ai)):
            # calcualting between each two pieces.
            if i != j:
                count_ai+=1
                # prioritize in a row or column, Bgive higher score for those.
                if index_ai[i][0] == index_ai[j][0]: 
                    if index_ai[i][1] - index_ai[j][1] <= 1:
                        ai_dist_score += 1
                    elif index_ai[i][1] - index_ai[j][1] <= 2:
                        ai_dist_score += 0.5
                    else:
                        ai_dist_score += 1/(dist(index_ai[i], index_ai[j]) + 2)
                elif index_ai[i][1] == index_ai[j][1]:
                    if index_ai[i][0] - index_ai[j][0] <= 1:
                        ai_dist_score += 1
                    elif index_ai[i][0] - index_ai[j][0] <= 2:
                        ai_dist_score += 0.5
                    else:
                        ai_dist_score += 1/(dist(index_ai[i], index_ai[j]) + 2)
                # if not, use distance function to evaluate the distance, and then normalize it to give a score
                else:
                    ai_dist_score += 1/(dist(index_ai[i], index_ai[j]) + 2)
    #ai_total = (ai_pos_score + ai_dist_score) / 10
    ai_total = ai_dist_score / count_ai 

    # do the same for opponent
    opp_dist_score = 0
    count_opp = 6
    for i in range(len(index_opp)):
        for j in range(i, len(index_opp)):
            if i != j:
                count_opp += 1
                if index_opp[i][0] == index_opp[j][0]: 
                    if index_opp[i][1] - index_opp[j][1] <= 1:
                        opp_dist_score += 1
                    elif index_opp[i][1] - index_opp[j][1] <= 2:
                        opp_dist_score += 0.5
                    else:
                        opp_dist_score += 1/(dist(index_opp[i], index_opp[j]) + 2) 
                elif index_opp[i][1] == index_opp[j][1]:
                    if index_opp[i][0] - index_opp[j][0] <= 1:
                        opp_dist_score += 1
                    elif index_opp[i][0] - index_opp[j][0] <= 2:
                        opp_dist_score += 0.5
                    else:
                        opp_dist_score += 1/(dist(index_opp[i], index_opp[j]) + 2)
                else:
                    opp_dist_score += 1/(dist(index_opp[i], index_opp[j]) + 2)
    #opp_total = (opp_pos_score + opp_dist_score) / 10
    opp_total = (opp_dist_score) / count_opp 

    # return the difference between their score (has to be <1 or >1)
    return ai_total - opp_total

def dist(index1, index2):
    """
    Helper function to calculate the euclidian distance between two indexes.
    param: two indices
    return: their euclidean distances
    """
    return (abs(index1[0] - index2[0])**2 + abs(index1[1] - index2[1])**2)**0.5

def max_value(state, depth, num_piece):
    """
    Minimax function, return the max between current state's value and successfor's value
    """
    # if already terminal state
    if game_value(state) == 1 or game_value(state) == -1:
        return game_value(state)
    # depth of 2 guarantees run time under 5 min
    elif depth == 2:
        return heuristic_game_value(state)
    else:
        value = -999 # we know game value must be at least -1 and most 1
        for s in success(state, ai_piece, num_piece):
            value = max(value, min_value(s, depth+1, num_piece)) # recursive case - we look for the max value
        return value
    
def min_value(state, depth, num_piece):
    """
    Min part of the minimax. Return the min value between state and successors.
    """
    # if already at terminal state
    if game_value(state) == 1 or game_value(state) == -1:
        return game_value(state)
    # if reached depth already, evaluate heuristically
    elif depth == 2: 
        return heuristic_game_value(state)
    else:
        value = 999 # we know value must be at least -1 and at most 1.
        for s in success(state, player_piece, num_piece):
            value = min(value, max_value(s, depth + 1, num_piece)) # look for min
        return value
    
def adjacent(cell1, cell2):
    return abs(cell1[0] - cell2[0]) <= 1 and abs(cell1[1] - cell2[1]) <= 1

    

# initialize pygame
pygame.init()

# screen
window_size = [600, 600]
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Teeko")

#colors
dark_gray = (40, 40, 40)
light_gray = (60, 60, 60)

# grid size
grid_size = 5
cell_size = window_size[0] // grid_size

# initial game state
game_state = [[' ' for _ in range(grid_size)] for _ in range(grid_size)]

# track if a piece is selected
piece_selected = False
piece_location = None

num_piece = 0

first_move = random.choice(['player', 'ai'])

if first_move == 'ai':
    ai_move = make_move(game_state, num_piece)
    game_state[ai_move[0][0]][ai_move[0][1]] = ai_piece
    num_piece += 1
    
# game loop
running = True
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            # user call
            mouse_pos = pygame.mouse.get_pos()
            cell_x = mouse_pos[0] // cell_size
            cell_y = mouse_pos[1] // cell_size

            # if in move phase
            if num_piece >= 8:
                # piece selected
                if piece_selected:
                    if game_state[cell_y][cell_x] == ' ' and adjacent(piece_location, (cell_y, cell_x)):
                        game_state[cell_y][cell_x] = player_piece
                        game_state[piece_location[0]][piece_location[1]] = ' '
                        piece_selected = False
                        piece_location = None

                        status = game_value(game_state)
                        if status != 0:
                            if status == 1:
                                print("AI wins!")
                                running = False
                                break
                            elif status == -1:
                                print("Player wins!")
                                running = False
                                break

                         # determine ai move
                        ai_move = make_move(game_state, num_piece)
                        game_state[ai_move[0][0]][ai_move[0][1]] = ai_piece
                        game_state[ai_move[1][0]][ai_move[1][1]] = ' '
                        status = game_value(game_state)
                        if status != 0:
                            if status == 1:
                                print("AI wins!")
                                running = False
                                break
                            elif status == -1:
                                print("Player wins!")
                                running = False
                                break
                else:
                    if game_state[cell_y][cell_x] == player_piece:
                        piece_selected = True
                        piece_location = (cell_y, cell_x)
            # if in drop phase
            else:
                if game_state[cell_y][cell_x] == ' ':
                    game_state[cell_y][cell_x] = player_piece
                    num_piece += 1
                    status = game_value(game_state)
                    if status != 0:
                        if status == 1:
                            print("AI wins!")
                            running = False
                            break
                        elif status == -1:
                            print("Player wins!")
                            running = False
                            break

                    ai_move = make_move(game_state, num_piece)
                    game_state[ai_move[0][0]][ai_move[0][1]] = ai_piece
                    num_piece += 1
                    status = game_value(game_state)
                    if status != 0:
                        if status == 1:
                            print("AI wins!")
                            running = False
                            break
                        elif status == -1:
                            print("Player wins!")
                            running = False
                            break
    
    # fill
    screen.fill(dark_gray)

    # pieces
    for y in range(grid_size):
        for x in range(grid_size):
            if game_state[y][x] == player_piece:
                pygame.draw.circle(screen, (0, 255, 0), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5)
            elif game_state[y][x] == ai_piece:
                pygame.draw.circle(screen, (255, 0, 0), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5)

    #grid
    for x in range(0, window_size[0], cell_size):
        pygame.draw.line(screen, light_gray, (x, 0), (x, window_size[1]), 1)
    for y in range(0, window_size[1], cell_size):
        pygame.draw.line(screen, light_gray, (0, y), (window_size[0], y), 1)

    pygame.display.flip()

pygame.quit()