import pygame
import random
import time


class ComputerGame:
    def __init__(self, win, buttons, bgImg):
        self.win = win
        self.board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]
        self.buttons = buttons
        self.backgroundImage = bgImg

    def setPlayerButtonsActive(self):
        for btn in range(7, len(self.buttons)):
            btn.active = True

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
            for i in range(7, 13):
                if self.board[i] != 0:
                    done = False
            if done:
                return 1
            else:
                return -1

    def playGame(self):
        self.updateWindow()
        ok = 1
        run = True
        clock = pygame.time.Clock()
        while run:
            poz = 0
            clock.tick(60)
            if ok == 0:
                poz = random.randint(0, 6)
                while self.board[poz] == 0:
                    poz = random.randint(0, 6)
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in self.buttons:
                            if btn.click(pos) and self.board[self.buttons.index(btn)] != 0:
                                poz = self.buttons.index(btn)
            seeds = self.board[poz]
            self.board[poz] = 0
            for i in range(seeds):
                if ok == 0:
                    if poz + 1 == 13:
                        poz = -1
                else:
                    if poz + 1 == 6:
                        poz = poz + 1
                self.board[poz + 1] += 1
            self.updateWindow()
            ok = (ok + 1) % 2
            done = self.is_finished()
            if done != -1:
                font = pygame.font.SysFont("javanesetext", 60)
                if done == 0:
                    text = font.render("You Lost!", True, (108, 7, 7))
                else:
                    ext = font.render("You Won", True, (108, 7, 7))
                self.win.blit(text, (150, 10))
                pygame.display.update()
                time.sleep(1)
                pygame.quit()