import pygame
import random
import time
import threading


class ComputerGame:
    def __init__(self, win, buttons, bgImg):
        self.win = win
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.buttons = buttons
        self.backgroundImage = bgImg
        self.setAIButtonsInactive()
        self.setPlayerButtonsInactive()

    def setAIButtonsInactive(self):
        for btn in range(7):
            self.buttons[btn].active = False

    def setPlayerButtonsActive(self):
        for btn in range(7, len(self.buttons) - 1):
            self.buttons[btn].active = True

    def setPlayerButtonsInactive(self):
        for btn in range(7, len(self.buttons)):
            self.buttons[btn].active = False

    def updateWindow(self):
        self.win.blit(self.backgroundImage, [0, 0])
        for btn in self.buttons:
            btn.setText(str(self.board[self.buttons.index(btn)]))
            btn.draw(self.win)
        pygame.display.update()

    def is_finished(self):
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
        '''

        :return:
        '''
        global text
        self.updateWindow()
        ok = 1
        run = True
        clock = pygame.time.Clock()
        lock = threading.Lock()
        while run:
            poz = 0
            clock.tick(60)
            if ok == 0:
                poz = random.randint(0, 5)
                while self.board[poz] == 0:
                    poz = random.randint(0, 5)
                seeds = self.board[poz]
                self.board[poz] = 0
                for i in range(seeds):
                    poz += 1
                    if poz == 13:
                        poz = 0
                    self.board[poz] += 1
            else:
                lock.acquire()
                self.setPlayerButtonsActive()
                start = time.time()
                end = start
                entered = False
                while end - start < 7:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.quit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            for btn in self.buttons:
                                if btn.click(pos) and self.board[self.buttons.index(btn)] != 0:
                                    poz = self.buttons.index(btn)
                                    entered = True
                            seeds = self.board[poz]
                            self.board[poz] = 0
                            for i in range(seeds):
                                poz += 1
                                if poz == 6:
                                    poz += 1
                                if poz == 14:
                                    poz = 0
                                self.board[poz] += 1
                    if entered:
                        end = start + 8
                    else:
                        end = time.time()
                self.setPlayerButtonsInactive()
                lock.release()
            print(f'ok = {ok} ==> BOARD: \n {self.board}')
            self.updateWindow()
            ok = (ok + 1) % 2
            done = self.is_finished()
            if done != -1:
                font = pygame.font.SysFont("inkfree", 80)
                if done == 0:
                    text = font.render("You Lost!", True, (51, 7, 7))
                else:
                    text = font.render("You Won", True, (51, 7, 7))
                self.win.blit(text, (170, 300))
                pygame.display.update()
                time.sleep(2)
                return
