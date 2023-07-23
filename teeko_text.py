import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
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
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        # TODO: detect drop phase
        # determine if it is drop phase or not
        num_piece = 0
        for row in state:
            for column in row:
                if column != ' ':
                    num_piece += 1

        drop_phase = True if num_piece < 8 else False  
        
        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better

        # case if it is drop phase
        if drop_phase:
            drop_move = []
            best_state = None
            best_score = None
            # find the best possible state use minimax
            for succ in self.succ(state, self.my_piece):
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
            for succ in self.succ(state, self.my_piece):
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
                    if state[i][j] == ' ' and best[i][j] == self.my_piece:
                        target_row = i
                        target_col = j
                    
                    # if original is piece but new state is empty, the source point
                    if state[i][j] == self.my_piece and best[i][j] == ' ':
                        source_row = i
                        source_col = j

            move.append((source_row, source_col))
            move.insert(0, (target_row, target_col))
            return move
        # ensure the destination (row,col) tuple is at the beginning of the move list
        # move.insert(0, (row, col))
        # return move

    def succ(self, state, curr_piece):
        """
        Get all the successors of the current state
        param: state: the current state of board, to generate new states. curr_piece: which player's move, r or b
        return: a list of lists of list -  a list of possible states the board could be
        """
        # return value here
        legal_succs = []

        # check if it is in drop phase or not
        num_piece = 0
        for row in state:
            for column in row:
                if column != ' ':
                    num_piece += 1

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
                    if state[i][j] == self.my_piece:
                        if i == 0:
                            if j == 0:
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i, j+1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i+1, j], curr_piece))
                                if state[i+1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i+1, j+1], curr_piece))
                            if j > 0 and j < len(state[0]) - 1:
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j-1], curr_piece))
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j+1], curr_piece))
                                if state[i+1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1,j], curr_piece))
                                if state[i+1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j+1], curr_piece))
                            if j == len(state[0]):
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j-1], curr_piece))
                                if state[i+1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j], curr_piece))
                        elif i > 0 and i < len(state) - 1:
                            if j == 0:
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j], curr_piece))
                                if state[i-1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j+1], curr_piece))
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i, j+1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i+1, j], curr_piece))
                                if state[i+1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i+1, j+1], curr_piece))
                            if j > 0 and j < len(state[0]) - 1:
                                if state[i-1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1,j], curr_piece))
                                if state[i-1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1,j+1], curr_piece))
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j-1], curr_piece))
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j+1], curr_piece))
                                if state[i+1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1,j], curr_piece))
                                if state[i+1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j+1], curr_piece))
                            if j == len(state[0]):
                                if state[i-1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1,j-1], curr_piece))
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1,j], curr_piece))
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j-1], curr_piece))
                                if state[i+1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j-1], curr_piece))
                                if state[i+1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i+1, j], curr_piece))
                        elif i == len(state) - 1:
                            if j == 0:
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i-1, j], curr_piece))
                                if state[i-1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i-1, j+1], curr_piece))
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i, j], [i, j+1], curr_piece))
                            if j > 0 and j < len(state[0]) - 1:
                                if state[i-1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j], curr_piece))
                                if state[i-1][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j+1], curr_piece))
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i,j-1], curr_piece))
                                if state[i][j+1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i,j+1], curr_piece))
                            if j == len(state[0]):
                                if state[i-1][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j-1], curr_piece))
                                if state[i-1][j] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i-1, j], curr_piece))
                                if state[i][j-1] == ' ':
                                    legal_succs.append(self.get_possible_case(state, [i,j], [i, j-1], curr_piece))
        return legal_succs

    def get_possible_case(self, state, source, to, piece):
        """
        Helper functions return a new case base on source and destination
        param: state - current state of board. source - list of form [x,y] source point. to. list of form [x,y] of destination point. piece - r or b, current player
        return temp - a state where piece moved from source to destination
        """
        temp = copy.deepcopy(state)
        temp[source[0]][source[1]] = ' '
        temp[to[0]][to[1]] = piece
        return temp

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
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
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ':
                    if state[row][col] == state[row+1][col+1] == state[row+2][col+2] == state[row+3][col+3]:
                        return 1 if state[row][col] == self.my_piece else -1
        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(3, 5):
                if state[row][col] != ' ':
                    if state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                        return 1 if state[row][col] == self.my_piece else -1

        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ':
                    if state[row][col] == state[row][col + 1] == state[row+1][col] == state[row+1][col+1]:
                        return 1 if state[row][col] == self.my_piece else -1
        return 0  # no winner yet

    def heuristic_game_value(self, state):
        """
        Evaluate the game heuristically by calculating the distances between pieces.
        param: state, the current state of the game
        return: a value between -1 and 1 indicating the distance between pieces.
        """
        if self.game_value(state) == -1 or self.game_value(state) == 1:
            return self.game_value(state)
        index_ai = []
        index_opp = []
        # find index where ai's piece is and opponents piece is at
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] != ' ':
                    piece = state[i][j]
                    if piece == self.my_piece:
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
                            ai_dist_score += 1/(self.dist(index_ai[i], index_ai[j]) + 2)
                    elif index_ai[i][1] == index_ai[j][1]:
                        if index_ai[i][0] - index_ai[j][0] <= 1:
                            ai_dist_score += 1
                        elif index_ai[i][0] - index_ai[j][0] <= 2:
                            ai_dist_score += 0.5
                        else:
                            ai_dist_score += 1/(self.dist(index_ai[i], index_ai[j]) + 2)
                    # if not, use distance function to evaluate the distance, and then normalize it to give a score
                    else:
                        ai_dist_score += 1/(self.dist(index_ai[i], index_ai[j]) + 2)
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
                            opp_dist_score += 1/(self.dist(index_opp[i], index_opp[j]) + 2) 
                    elif index_opp[i][1] == index_opp[j][1]:
                        if index_opp[i][0] - index_opp[j][0] <= 1:
                            opp_dist_score += 1
                        elif index_opp[i][0] - index_opp[j][0] <= 2:
                            opp_dist_score += 0.5
                        else:
                            opp_dist_score += 1/(self.dist(index_opp[i], index_opp[j]) + 2)
                    else:
                        opp_dist_score += 1/(self.dist(index_opp[i], index_opp[j]) + 2)
        #opp_total = (opp_pos_score + opp_dist_score) / 10
        opp_total = (opp_dist_score) / count_opp 

        # return the difference between their score (has to be <1 or >1)
        return ai_total - opp_total

    def dist(self, index1, index2):
        """
        Helper function to calculate the euclidian distance between two indexes.
        param: two indices
        return: their euclidean distances
        """
        return (abs(index1[0] - index2[0])**2 + abs(index1[1] - index2[1])**2)**0.5
    
    def max_value(self, state, depth):
        """
        Minimax function, return the max between current state's value and successfor's value
        """
        # if already terminal state
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state)
        # depth of 2 guarantees run time under 5 min
        elif depth == 2:
            return self.heuristic_game_value(state)
        else:
            value = -999 # we know game value must be at least -1 and most 1
            for s in self.succ(state, self.my_piece):
                value = max(value, self.min_value(s, depth+1)) # recursive case - we look for the max value
            return value
        
    def min_value(self, state, depth):
        """
        Min part of the minimax. Return the min value between state and successors.
        """
        # if already at terminal state
        if self.game_value(state) == 1 or self.game_value(state) == -1:
            return self.game_value(state)
        # if reached depth already, evaluate heuristically
        elif depth == 2: 
            return self.heuristic_game_value(state)
        else:
            value = 999 # we know value must be at least -1 and at most 1.
            for s in self.succ(state, self.opp):
                value = min(value, self.max_value(s, depth + 1)) # look for min
            return value
            


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
            print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp + "'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                      (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
