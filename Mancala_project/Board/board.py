import pygame
from circleButton import CircleButton
from button import Button
from store import Store
from computerGame import ComputerGame
pygame.init()

window_width = 600
window_height = 400

size = (window_width, window_height)
win = pygame.display.set_mode(size)

pygame.display.set_caption("Game of Mancala")

background_image = pygame.image.load("wood.jpg").convert()
WOOD = (186, 140, 99)
LIGHT_WOOD = (149, 112, 79)
ROSIATIC = (108, 7, 7)
HOVERED = (114, 68, 33)
buttons = [CircleButton(450, 70, 30, WOOD, "4"), CircleButton(390, 70, 30, WOOD, "4"),
           CircleButton(330, 70, 30, WOOD, "4"), CircleButton(270, 70, 30, WOOD, "4"),
           CircleButton(210, 70, 30, WOOD, "4"), CircleButton(150, 70, 30, WOOD, "4"),
           Store(70, 75, 50, 200, WOOD, "0"),
           CircleButton(150, 270, 30, LIGHT_WOOD, "4"), CircleButton(210, 270, 30, LIGHT_WOOD, "4"),
           CircleButton(270, 270, 30, LIGHT_WOOD, "4"), CircleButton(330, 270, 30, LIGHT_WOOD, "4"),
           CircleButton(390, 270, 30, LIGHT_WOOD, "4"), CircleButton(450, 270, 30, LIGHT_WOOD, "4"),
           Store(480, 75, 50, 200, LIGHT_WOOD, "0")]
mancala_board = [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0]


def setButtonsActive(p):
    if p == 0:
        for i, btn in zip(range(len(buttons)), buttons):
            if i < 6:
                btn.active = True
            elif 6 < i < 13:
                btn.active = False
    else:
        for i, btn in zip(range(len(buttons)), buttons):
            if i < 6:
                btn.active = False
            elif 6 < i < 13:
                btn.active = True


def run_game():
    run = True
    clock = pygame.time.Clock()
    p = 0
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            setButtonsActive(p)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
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
            p = (p + 1) % 2
        win.blit(background_image, [0, 0])
        for btn in buttons:
            btn.setText(str(mancala_board[buttons.index(btn)]))
            btn.draw(win)
        pygame.display.flip()


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    win.blit(background_image, [0, 0])
    font = pygame.font.SysFont("javanesetext", 60)
    text = font.render("MANCALA", 1, ROSIATIC)
    win.blit(text, (150, 10))
    font2 = pygame.font.SysFont("comicsans", 50)
    text2 = font2.render("Choose your partner", 1, ROSIATIC)
    win.blit(text2, (70, 150))

    type_player = [Button(100, 250, 180, 40, WOOD, "computer"), Button(330, 250, 180, 40, LIGHT_WOOD, "human")]

    for btn in type_player:
        btn.draw(win)
    pygame.display.update()

    index = -1
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for types in type_player:
                    if types.click(pos):
                        index = type_player.index(types)
                        run = False
    if index == 0:
        game = ComputerGame(win, buttons, background_image)
        game.playGame()
    elif index == 1:
        run_game()


if __name__ == "__main__":
    while True:
        try:
            menu_screen()
            # run_game()
        except Exception as e:
            print(str(e))
            break