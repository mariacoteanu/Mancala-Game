"""
in this file is the blueprint of networking game
"""


class NetworkGame:
    def __init__(self, gameId):
        """
        NetworkGame constructor, have as private variables the board, gameId, if the game is ready,
        if player moved and if the game is over and who is the winner
         """
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.game_id = gameId
        self.ready = False
        self.p0_went = False
        self.p1_went = True
        self.winner = -1
        self.done = False

    def connected(self):
        """return if the game is ready -- if are 2 players connected to server to start new game"""
        return self.ready

    def update_tour(self, player_id):
        """
        after player "p" moved, then the private variables are update so the other player can move
        :param player_id: which player moved
        :return: nothing to return, only update players tour
        """
        if player_id == 0:
            self.p0_went = True
            self.p1_went = False

        else:
            self.p0_went = False
            self.p1_went = True

    def is_final(self):
        """looking after winner in every players elements and update private variables 'done' and 'winner' """
        done = True
        for index in range(0, 6):  # first player elements are from 0 to 5
            if self.board[index] != 0:
                done = False

        if done:  # if all his elements are 0, he is the winner and game is over
            self.done = True
            self.winner = 0
        else:  # if first player is not the winner, we look for next player
            done = True

            for index in range(7, len(self.board)-1):  # second player elements are from 7 to 12
                if self.board[index] != 0:
                    done = False

            if done:  # if all his elements are 0, he is the winner and game is over
                self.done = True
                self.winner = 1
            else:  # else the game is not over
                self.done = False

    def move(self, index, player_id):
        """
        the player's moving logics
        the player choose an index to take the seeds from. in this place remain 0
        and all the seeds are added to next neighbours
        if i reach to 14 position, it not exist so i start from 0
        the first player cannot add point in next player's store (index 13) and vice-versa
        the second player cannot add point in first player's store (index 6)
        :param index: the position player choose to start giving seeds to neighbours positions
        :param player_id: player who made the move ( 0 / 1 )
        :return: nothing to return, only is performed updating of board and if game is over
        """
        nr_seeds = self.board[index]
        self.board[index] = 0

        for index in range(nr_seeds):
            index += 1
            if index == 14:
                index = 0
            if player_id == 0:
                if index == 13:
                    index = 0
            else:
                if index == 6:
                    index = index+1
            self.board[index] += 1

        self.update_tour(player_id)
        self.is_final()
