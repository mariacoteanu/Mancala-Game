class Game:
    def __init__(self, gameId):
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.gameId = gameId
        self.ready = False
        self.p1Went = False
        self.p2Went = False

    def connected(self):
        return self.ready

    def updateTour(self, p):
        if p == 0:
            self.p1Went = True
            self.p2Went = False
        else:
            self.p2Went = True
            self.p1Went = False

    def is_final(self):
        done = True
        for i in range(0, 6):
            if self.board[i] != 0:
                done = False
        if done:
            return 0
        else:
            for i in range(7, 13):
                if self.board[i] != 0:
                    done = False
            if done:
                return 1
            else:
                return -1

    def move(self, index, p):
        seeds = self.board[index]
        self.board[index] = 0
        for i in range(seeds):
            if p == 0:
                if index + 1 == 13:
                    index = -1
            else:
                if index + 1 == 6:
                    index = index + 1
            self.board[index + 1] += 1
        self.updateTour(p)
        return self.is_final()

    def resetGame(self):
        self.p1Went = False
        self.p2Went = False
