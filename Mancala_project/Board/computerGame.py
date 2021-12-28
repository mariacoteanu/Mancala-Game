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
        self.py_window = win
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.buttons = buttons
        self.background_image = bgImg
        self.set_player_buttons_inactive()

    def set_player_buttons_active(self):
        """when is user's tour, make his buttons active to choose the move"""
        for btn in range(7, len(self.buttons) - 1):
            self.buttons[btn].active = True

    def set_player_buttons_inactive(self):
        """after user's tour, make his buttons inactive because is AI's tour"""
        for btn in range(7, len(self.buttons)):
            self.buttons[btn].active = False

    def update_window(self):
        """after every move, pygame window is updated"""
        self.py_window.blit(self.background_image, [0, 0])
        for btn in self.buttons:
            btn.set_text(str(self.board[self.buttons.index(btn)]))
            btn.draw(self.py_window)
        pygame.display.update()

    def is_finished(self):
        """
        this function verify if the game is over and who is the winner
        :return: winner( 0 / 1) , or -1 if the game is not over
        """
        done = True
        for index in range(0, 6):
            if self.board[index] != 0:
                done = False

        if done:
            return 0
        else:
            done = True
            for index in range(7, len(self.buttons) - 1):
                if self.board[index] != 0:
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

        self.update_window()
        player_tour = 1  # user start the game
        run = True
        clock = pygame.time.Clock()
        lock = threading.Lock()

        while run:
            position = 0
            clock.tick(60)
            if player_tour == 0:  # Computer moving logics
                position = random.randint(0, 5)  # make random choose from his available elements, from 0 to 5

                while self.board[position] == 0:
                    position = random.randint(0, 5)
                nr_seeds = self.board[position]  # take value from that board index
                self.board[position] = 0  # make that index 0

                for loop_times in range(nr_seeds):
                    position += 1
                    if position == 13:  # AI can not add point to user's store and reinitialize position
                        position = 0
                    self.board[position] += 1  # add point to neighbours

            else:  # user moving logics
                # I'm using lock for making AI to wait the user to interact with gui
                lock.acquire()
                self.set_player_buttons_active()  # setting user's buttons active

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
                                    position = self.buttons.index(btn)  # if is valid move, then update board
                                    entered = True
                            nr_seeds = self.board[position]
                            self.board[position] = 0

                            for loop_times in range(nr_seeds):
                                position += 1
                                if position == 6:  # user can not add point in ai's store
                                    position += 1
                                if position == 14:  # position 14 is not valid index, then restart position
                                    position = 0
                                self.board[position] += 1
                self.set_player_buttons_inactive()  # after user moved, he wait his tour and disable buttons
                lock.release()
            self.update_window()  # update user window
            player_tour = (player_tour + 1) % 2  # set next player

            done = self.is_finished()  # find if the game is over
            if done != -1:
                font = pygame.font.SysFont("inkfree", 80)
                if done == 0:  # then AI win
                    text = font.render("You Lost!", True, (51, 7, 7))
                else:  # user win
                    text = font.render("You Won", True, (51, 7, 7))
                self.py_window.blit(text, (170, 300))
                pygame.display.update()
                time.sleep(4)
                run = False  # get out from while and go to menu screen
