import pygame
import random 
import copy

# pieces
ai_piece = random.choice(['r', 'b'])
player_piece = 'r' if ai_piece == 'b' else 'b'
# AI's functions
def make_move(state):
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
    num_piece = 0
    for row in state:
        for column in row:
            if column != ' ':
                num_piece += 1

    drop_phase = True if num_piece < 8 else False  
        
    # select an unoccupied space randomly

    # case if it is drop phase
    if drop_phase:
        drop_move = []
        best_state = None
        best_score = None
        # find the best possible state use minimax
        for succ in self.succ(state, ai_piece):
            score = self.max_value(succ, 0)
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
        for succ in self.succ(state, ai_piece):
            score = self.max_value(succ, 0)
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

            # update game state
            game_state[cell_y][cell_x] = 1

    # fill
    screen.fill(dark_gray)

    # pieces
    for y in range(grid_size):
        for x in range(grid_size):
            if game_state[y][x] == 1:
                pygame.draw.circle(screen, (0, 255, 0), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5)
            elif game_state[y][x] == 2:
                pygame.draw.circle(screen, (255, 0, 0), (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2), cell_size // 2 - 5)

    #grid
    for x in range(0, window_size[0], cell_size):
        pygame.draw.line(screen, light_gray, (x, 0), (x, window_size[1]), 1)
    for y in range(0, window_size[1], cell_size):
        pygame.draw.line(screen, light_gray, (0, y), (window_size[0], y), 1)

    pygame.display.flip()

pygame.quit()