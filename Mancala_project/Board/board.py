import pygame
from button import Button
from store import Store

pygame.init()

window_width = 600
window_height = 400

size = (window_width, window_height)
win = pygame.display.set_mode(size)

pygame.display.set_caption("Hello World")

background_image = pygame.image.load("wood.jpg").convert()

buttons = [Button(450, 70, 30, (186, 140, 99), "4"), Button(390, 70, 30, (186, 140, 99), "4"),
           Button(330, 70, 30, (186, 140, 99), "4"), Button(270, 70, 30, (186, 140, 99), "4"),
           Button(210, 70, 30, (186, 140, 99), "4"), Button(150, 70, 30, (186, 140, 99), "4"),
           Store(70, 75, 50, 200, (186, 140, 99), "0"),
           Button(150, 270, 30, (149, 112, 79), "4"), Button(210, 270, 30, (149, 112, 79), "4"),
           Button(270, 270, 30, (149, 112, 79), "4"), Button(330, 270, 30, (149, 112, 79), "4"),
           Button(390, 270, 30, (149, 112, 79), "4"), Button(450, 270, 30, (149, 112, 79), "4"),
           Store(480, 75, 50, 200, (149, 112, 79), "0")]
mancala_board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]

if __name__ == "__main__":
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.click(pos) and mancala_board[buttons.index(btn)] != 0:
                        index = buttons.index(btn)
                        nr = mancala_board[index]
                        mancala_board[index] = 0
                        btn.setText(str(mancala_board[index]))
                        btn.draw(win)
                        if index == 13:
                            index = -1
                        for i in range(nr):
                            mancala_board[index + 1] += 1
                            btn.setText(str(mancala_board[index + 1]))
                            btn.draw(win)
                            pygame.display.update()
                            index += 1
                            if index == 13:
                                index = -1
        win.blit(background_image, [0, 0])
        for btn in buttons:
            btn.setText(str(mancala_board[buttons.index(btn)]))
            btn.draw(win)
        pygame.display.flip()
