"""
in this file is the blueprint of computer game
"""
import pygame
import random
import time
import threading


class ComputerGame:
    def __init__(self, win, buttons, bgImg):
        """ComputerGame constructor where are initialized the board, the gui window, the buttons from gui
        and making buttons inactive
        """
        self.win = win
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.buttons = buttons
        self.backgroundImage = bgImg
        self.setPlayerButtonsInactive()

    def setPlayerButtonsActive(self):
        """when is user's tour, make his buttons active to choose the move"""
        for btn in range(7, len(self.buttons) - 1):
            self.buttons[btn].active = True

    def setPlayerButtonsInactive(self):
        """after user's tour, make his buttons inactive because is AI's tour"""
        for btn in range(7, len(self.buttons)):
            self.buttons[btn].active = False

    def updateWindow(self):
        """after every move, pygame window is updated"""
        self.win.blit(self.backgroundImage, [0, 0])
        for btn in self.buttons:
            btn.setText(str(self.board[self.buttons.index(btn)]))
            btn.draw(self.win)
        pygame.display.update()

    def is_finished(self):
        """
        this function verify if the game is over and who is the winner
        :return: winner( 0 / 1) , or -1 if the game is not over
        """
        done = True
        for i in range(0, 6):
            if self.board[i] != 0:
                done = False
        if done:
            return 0
        else:
            done = True
            for i in range(7, len(self.buttons) - 1):
                if self.board[i] != 0:
                    done = False
            if done:
                return 1
            else:
                return -1

    def playGame(self):
        """
        game logics with ai tour and user's tour
        :return: nothing is returned, when game is over, user is returned to menu screen
        """

        self.updateWindow()
        ok = 1  # user start the game
        run = True
        clock = pygame.time.Clock()
        lock = threading.Lock()
        while run:
            poz = 0
            clock.tick(60)
            if ok == 0:  # Computer moving logics
                poz = random.randint(0, 5)  # make random choose from his available elements, from 0 to 5
                while self.board[poz] == 0:
                    poz = random.randint(0, 5)
                seeds = self.board[poz]  # take value from that board index
                self.board[poz] = 0   # make that index 0
                for i in range(seeds):
                    poz += 1
                    if poz == 13:  # AI can not add point to user's store and reinitialize position
                        poz = 0
                    self.board[poz] += 1  # add point to neighbours
            else:  # user moving logics
                # I'm using lock for making AI to wait the user to interact with gui
                lock.acquire()
                self.setPlayerButtonsActive()  # setting user's buttons active

                entered = False
                while not entered:  # wait until user choose valid move
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            for btn in self.buttons:
                                if btn.click(pos) and self.board[self.buttons.index(btn)] != 0:
                                    poz = self.buttons.index(btn)  # if is valid move, then update board
                                    entered = True
                            seeds = self.board[poz]
                            self.board[poz] = 0
                            for i in range(seeds):
                                poz += 1
                                if poz == 6:  # user can not add point in ai's store
                                    poz += 1
                                if poz == 14:  # position 14 is not valid index, then restart position
                                    poz = 0
                                self.board[poz] += 1
                self.setPlayerButtonsInactive()  # after user moved, he wait his tour and disable buttons
                lock.release()
            self.updateWindow()  # update user window
            ok = (ok + 1) % 2  # set next player
            done = self.is_finished()  # find if the game is over
            if done != -1:
                font = pygame.font.SysFont("inkfree", 80)
                if done == 0:  # then AI win
                    text = font.render("You Lost!", True, (51, 7, 7))
                else:  # user win
                    text = font.render("You Won", True, (51, 7, 7))
                self.win.blit(text, (170, 300))
                pygame.display.update()
                time.sleep(4)
                run = False  # get out from while and go to menu screen
