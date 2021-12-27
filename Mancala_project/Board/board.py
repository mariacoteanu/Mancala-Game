import pygame
import time
from circleButton import CircleButton
from button import Button
from store import Store
from computerGame import ComputerGame
from connection import Connection

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


def setButtonsActive(p):
    if p == 0:
        for i, btn in zip(range(len(buttons)), buttons):
            if i < 6:
                btn.active = True
    else:
        for i, btn in zip(range(len(buttons)), buttons):
            if 6 < i < 13:
                btn.active = True


def setButtonsInactive():
    for i, btn in zip(range(len(buttons)), buttons):
        btn.active = False


def updateWindow(game):
    win.blit(background_image, [0, 0])
    if not game.connected():
        font = pygame.font.SysFont("javanesetext", 60)
        text = font.render("Waiting for opponent...", True, (51, 7, 7))
        win.blit(text, (50, 100))
        pygame.display.update()
        ready = False
        while not ready:
            if game.connected():
                ready = True
    
    for btn in buttons:
        btn.setText(str(game.board[buttons.index(btn)]))
        btn.draw(win)
    pygame.display.flip()


def run_game():
    run = True
    clock = pygame.time.Clock()
    n = Connection()
    player = int(n.getP())
    tour = 0
    setButtonsInactive()
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except Exception as ex:
            run = False
            print(str(ex), "\nCouldn't get game")
            break
        if game.done:
            font = pygame.font.SysFont("inkfree", 80)
            if game.winner == player:
                text = font.render("You Lost!", True, (51, 7, 7))
            else:
                text = font.render("You Won", True, (51, 7, 7))
            win.blit(text, (170, 300))
            pygame.display.update()
            time.sleep(1)
            break

        if tour == player:
            setButtonsActive(player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in buttons:
                        if btn.click(pos) and game.board[buttons.index(btn)] != 0:
                            if (player == 0 and game.p1Went) or (player == 1 and game.p0Went):
                                n.send(str(buttons.index(btn)))
        updateWindow(game)
        tour = (tour + 1) % 2


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    win.blit(background_image, [0, 0])
    font = pygame.font.SysFont("javanesetext", 60)
    text = font.render("MANCALA", True, ROSIATIC)
    win.blit(text, (150, 10))
    font2 = pygame.font.SysFont("comicsans", 50)
    text2 = font2.render("Choose your partner", True, ROSIATIC)
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
        menu_screen()
    elif index == 1:
        run_game()
        menu_screen()


if __name__ == "__main__":
    while True:
        try:
            menu_screen()
            # run_game()
        except Exception as e:
            print(str(e))
            break
