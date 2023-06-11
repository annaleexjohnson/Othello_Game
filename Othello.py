# Author: Annalee X Johnson
# GitHub username: annaleexjohnson
# Date: 06/11/2023
# Description: contains two classes for a Player and an Othello 'game', which keeps tracks of pieces and scores,
# as well as displays the game board

class Player:
    def __init__(self, name, color):
        """
        - initializes a player object
        :param name: the name of a player
        :param color: the team color of a player
        """
        self._name = name
        self._color = color

    def get_name(self):
        """
        - returns the player's name
        """
        return self._name

    def get_color(self):
        """
        - returns the player's color
        """
        return self._color


class Othello:
    def __init__(self):
        """
        - contains methods to play Othello with two players on a 2-D array
        - contains two private data members: players and board that are initialized to empty lists
            - players: contains list of dictionaries for each player with keys for name, color, and pieces
            - board: contains a list of rows and columns to represent the grid
        """
        self._players = []
        self._board = []

    def get_players(self):
        """
        - returns dict of players
        """
        return self._players

    def initialize_board(self):
        # initializes self._board to a new board if it's a new game

        # top border
        self._board.append(["* " for x in range(10)])
        # 8x8 board
        for x in range(8):
            self._board.append([". " if x in range(1, 9) else "* " for x in range(10)])
        # bottom border
        self._board.append(["* " for x in range(10)])

        # initialize starting pieces
        self._board[4][4] = "O "
        self._board[4][5] = "X "
        self._board[5][4] = "X "
        self._board[5][5] = "O "

    def print_board(self):
        """
        - no parameters
        - prints the current board but doesn't return anything
        """
        if len(self._board) == 0:
            self.initialize_board()

        # prints each list on a new line
        for each_list in self._board:
            print("".join(each_list))

    def create_player(self, player_name, color):
        """
        - creates player object by calling player class
        - takes in two parameters for name and color
        """

        # handles if the player_name is a team color
        if player_name.lower() == 'black' or player_name.lower() == 'white':
            print("You entered the name of a team. Please enter a different name.")
            return

        # handles if there are already 2 players
        if len(self._players) == 2:
            print("There are already enough players.")
            return

        # handles if an incorrect team color is entered
        if color.lower() != 'black' and color.lower() != 'white':
            print("Please enter a valid team color. You can pick 'black' or 'white.'")
            return

        # handles if there is a player who already picked the same color
        if len(self._players) == 1 and self._players[0]["color"] == color:
            print(f"Sorry, {self._players[0]['name']} already picked {color}.")
            return

        # otherwise, create a new player obj and add it to the self._players list
        new_player = Player(player_name, color)
        self._players.append({'name': new_player.get_name(),
                              'color': new_player.get_color(),
                              'pieces': 2
                              })

    def return_winner(self):
        """
        - takes no parameters
        - checks the number of pieces each player has in the self._players dict
        - returns "Winner is [black/white] player: player’s name"
        - returns "It's a tie" if black and white player has the same number of pieces on the board when the game ends
        """

        if self._players[0]["pieces"] == self._players[1]["pieces"]:
            return "It's a tie!"

        if self._players[0]["pieces"] > self._players[1]["pieces"]:
            return f"Winner is {self._players[0]['color']} player: {self._players[0]['name']}"

        return f"Winner is {self._players[1]['color']} player: {self._players[1]['name']}"

    def return_available_positions(self, color):
        """

        """
        # set current and other team based on color argument
        if color == 'black':
            current_team = "X"
            other_team = "O"
        else:
            current_team = "O"
            other_team = "X"

        # initialize list to hold all possible positions
        possible_pos = []
        # initialize list to store current piece placements
        placed_pieces = []

        # store all the placements of the current team's pieces
        for line in self._board:
            for index in range(len(self._board)):
                if line[index].strip() == current_team:
                    placed_pieces.append({"line": self._board.index(line), "index": index})

        # for every placed piece, check for available moves
        for piece in placed_pieces:
            # each piece's placement based on the line
            curr_line = piece["line"]
            next_line = piece["line"] + 1
            prev_line = piece["line"] - 1

            # each piece's placement based on index within the line
            curr_index = piece["index"]
            next_index = piece["index"] + 1
            prev_index = piece["index"] - 1

        # ----- find horizontal/vertical positions -----
            def x_y_pos(line, index):
                # xy_cell == the value of the next/previous cell
                xy_cell = self._board[line][index].strip()

                # if the next/prev cell is not the other team, then stop recursion
                if xy_cell != other_team:
                    # if it was the first cell, then don't do anything
                    if index == (curr_index - 1) or index == (curr_index + 1):
                        return
                    if line == (curr_line - 1) or line == (curr_line + 1):
                        return
                    # if it's the border, then don't do anything
                    if xy_cell == "*":
                        return
                    # otherwise, add coordinates to possible_pos
                    possible_pos.append((line, index))
                    return

                # check prev index
                if index < curr_index:
                    index -= 1
                # check next index
                if index > curr_index:
                    index += 1
                # check prev line
                if line < curr_line:
                    line -= 1
                # check next line
                if line > curr_line:
                    line += 1

                # recursive call
                x_y_pos(line, index)

            # check left horizontal cells
            x_y_pos(curr_line, prev_index)
            # check right horizontal cells
            x_y_pos(curr_line, next_index)
            # check up vertical cells
            x_y_pos(prev_line, curr_index)
            # check down vertical cells
            x_y_pos(next_line, curr_index)

        # ----- find diagonal positions -----
            def diagonal_pos(line, index):
                diagonal_cell = self._board[line][index].strip()

                if diagonal_cell != other_team:
                    if line == curr_line + 1 or line == curr_line - 1:
                        return
                    if diagonal_cell == "*":
                        return
                    possible_pos.append((line, index))
                    return

                # move up and left
                if line < curr_line and index < curr_index:
                    line -= 1
                    index -= 1
                # move up and right
                elif line < curr_line and index > curr_index:
                    line -= 1
                    index += 1
                # move down and left
                elif line > curr_line and index < curr_index:
                    line += 1
                    index -= 1
                # move down and right
                elif line > curr_line and index > curr_index:
                    line += 1
                    index += 1

                diagonal_pos(line, index)

            # check up and left
            diagonal_pos(prev_line, prev_index)
            # check up and right
            diagonal_pos(prev_line, next_index)
            # check down and left
            diagonal_pos(next_line, prev_index)
            # check down and right
            diagonal_pos(next_line, next_index)

        if len(possible_pos) == 0:
            return False

        return possible_pos

    def make_move(self, color, piece_position):
        """
        - takes two parameters: one for team color and the coordinates where a
        player would like to place a piece
        """
        # initialize board if empty
        if len(self._board) == 0:
            self.initialize_board()

        if color.lower() == 'black':
            current_team = "X"
            other_team = "O"
        else:
            current_team = "O"
            other_team = "X"

        # if the move is possible, update the score
        for player in self._players:
            if player["color"] == color:
                current_player = player


        # if the move isn't possible, then return
        if piece_position not in self.return_available_positions(color):
            print(f"{current_player['name']} tried to place their piece at {piece_position}.")
            return False

        print(f"{current_player['name']} placed their piece at {piece_position}.")
        current_player["pieces"] += 1

        # update grid
        new_index = piece_position[1]
        new_line = piece_position[0]
        
        prev_index = new_index - 1
        next_index = new_index + 1
        prev_line = new_line - 1
        next_line = new_line + 1

        # place piece on board
        self._board[new_line][new_index] = current_team + " "

        # flip horizontal/vertical pieces
        def flip_x_y(line, index):

            # if the next piece isn't the other team's, return
            if self._board[line][index].strip() != other_team:
                return

            # update score and flip another piece
            current_player["pieces"] += 1
            self._board[line][index] = current_team + " "

            # move on to the next cell
            if line < new_line:
                line -= 1
            if index < new_index:
                index -= 1
            if line > new_line:
                line += 1
            if index > new_index:
                index += 1

            # recursive call
            flip_x_y(line, index)

        flip_x_y(prev_line, new_index)
        flip_x_y(next_line, new_index)
        flip_x_y(new_line, prev_index)
        flip_x_y(new_line, next_index)

        # flip diagonal
        def flip_diagonal(line, index):
            # if the next piece isn't the other team's, return
            if self._board[line][index].strip() != other_team:
                return

            # update score and flip another piece
            current_player["pieces"] += 1
            self._board[line][index] = current_team + " "

            # move up and left
            if line < new_line and index < new_index:
                line -= 1
                index -= 1
            # move up and right
            elif line < new_line and index > new_index:
                line -= 1
                index += 1
            # move down and left
            elif line > new_line and index < new_index:
                line += 1
                index -= 1
            # move down and right
            elif line > new_line and index > new_index:
                line += 1
                index += 1

            # recursive call
            flip_diagonal(line, index)

        flip_diagonal(prev_line, prev_index)
        flip_diagonal(prev_line, next_index)
        flip_diagonal(next_line, next_index)
        flip_diagonal(next_line, prev_index)

        return True

    def play_game(self, player_color, piece_position):
        """
        """
        # call make_move() and pass arguments
        player_move = self.make_move(player_color, piece_position)

        # check each player for total pieces
        for player in self._players:
            if player["color"] == "black":
                blk_player = player
            if player["color"] == "white":
                wht_player = player

        # checks available positions for both players
        black_moves = self.return_available_positions('black')
        white_moves = self.return_available_positions('white')

        # handles if make_move returns False
        if player_move is False:

            # if both players have no moves left, it's game over
            if len(black_moves) == 0 and len(white_moves) == 0:
                # declare winner
                print(f"Game is ended. \nWhite piece: {wht_player['pieces']}\n Black pieces: {blk_player['pieces']}")
                print(self.return_winner())
                return

            # handles if only one player has no more moves
            elif self.return_available_positions(player_color) is False:
                print("No more possible moves.")

            # handles if the move was invalid but there are moves left
            else:
                print(f"That's not a valid move. \nHere's a list {player_color}'s of available moves:",
                      self.return_available_positions(player_color))
                return "Invalid move."
