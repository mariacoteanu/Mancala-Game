"""
This file is the client from TCP connection
where the GUI is created and the logic for AI game and networking
From __main__, first appear the menu_screen() where user choose which type of game he want to play
when the game is over he is returned to the menu again.
If he choose the computer partner, will be created a ComputerGame object and start the playGame function
but if he want to play with a person, then must run the server.py to accept connections, when are 2
users connected for a game, then will be send through socket the game object and is
updated the window.
"""

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
py_window = pygame.display.set_mode(size)

pygame.display.set_caption("Game of Mancala")

background_image = pygame.image.load("wood.jpg").convert()
WOOD = (186, 140, 99)
LIGHT_WOOD = (149, 112, 79)
BLACK_RED = (108, 7, 7)
buttons = [CircleButton(450, 70, 30, WOOD, "4"), CircleButton(390, 70, 30, WOOD, "4"),
           CircleButton(330, 70, 30, WOOD, "4"), CircleButton(270, 70, 30, WOOD, "4"),
           CircleButton(210, 70, 30, WOOD, "4"), CircleButton(150, 70, 30, WOOD, "4"),
           Store(70, 75, 50, 200, WOOD, "0"),
           CircleButton(150, 270, 30, LIGHT_WOOD, "4"), CircleButton(210, 270, 30, LIGHT_WOOD, "4"),
           CircleButton(270, 270, 30, LIGHT_WOOD, "4"), CircleButton(330, 270, 30, LIGHT_WOOD, "4"),
           CircleButton(390, 270, 30, LIGHT_WOOD, "4"), CircleButton(450, 270, 30, LIGHT_WOOD, "4"),
           Store(480, 75, 50, 200, LIGHT_WOOD, "0")]


def set_buttons_active(playerId):
    """
    called only in networking game
    this function enable the player's buttons
    if is his tour, then he can press them an choose element
    :param playerId: the player id
    :return: nothing to return, only make an effect
    """
    if playerId == 0:  # if is the first player, he have the first 6 buttons to choose from, the 6 is the store
        for index, btn in zip(range(len(buttons)), buttons):
            if index < 6:
                btn.active = True
    else:  # but he is the second one, then he have the buttons from 7 -> 12, the 13 is the store
        for index, btn in zip(range(len(buttons)), buttons):
            if 6 < index < 13:
                btn.active = True


def set_buttons_inactive():
    """
    called only in networking game
    this function is called to disable all the buttons, especially after is tour
    because when is not his tour he can't choose element
    :return: nothing to return, only make an effect
    """
    for index, btn in zip(range(len(buttons)), buttons):
        btn.active = False


def update_window(game):
    """
    called only in networking game
    as this function name, is called to update user's window, the buttons numbers
    :param game: is the object game send via socket, I use the game.board to update text from buttons
                    and the game.connected() to find pair to play and display the waiting window
    :return: nothing to return, only update window
    """
    py_window.blit(background_image, [0, 0])

    if not game.connected():
        font = pygame.font.SysFont("javanesetext", 60)
        text = font.render("Waiting for opponent...", True, (51, 7, 7))
        py_window.blit(text, (50, 100))
        pygame.display.update()
    else:
        for btn in buttons:
            btn.set_text(str(game.board[buttons.index(btn)]))
            btn.draw(py_window)
        pygame.display.flip()


def run_game():
    """
    the main function where is the networking logics between players
    :return: nothing to return, when is ended, then the game is over and is returned to menu_screen()
    """
    run = True
    clock = pygame.time.Clock()
    network = Connection()  # create TCP connection with socket
    player = int(network.get_player_id())
    set_buttons_inactive()  # set all buttons inactive
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = network.send("get")  # i receive from server the updated game object
        except Exception as ex:
            print(str(ex), "\nCouldn't get game")
            break
        if game.done:  # if game is over
            update_window(game)  # I update one last time window
            font = pygame.font.SysFont("inkfree", 80)

            if game.winner != player:  # display if the player win or lost
                text = font.render("You Lost!", True, (51, 7, 7))
            else:
                text = font.render("You Won", True, (51, 7, 7))

            py_window.blit(text, (170, 300))
            pygame.display.update()
            time.sleep(5)
            break  # get out from while and the the function is ended

        if (player == 0 and game.p1_went) or (player == 1 and game.p0_went):
            # if is player's tour and the partner went, then he can choose new element
            set_buttons_active(player)  # I set the player's button active
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for btn in buttons:
                        if btn.click(pos) and game.board[buttons.index(btn)] != 0:
                            # if i press a button and is active and the value is different than 0, then is valid
                            network.send(str(buttons.index(btn)))  # send the value to socket to update game
                            set_buttons_inactive()  # after he moved, then he no longer can to choose another button
        update_window(game)  # if is not his tour and after he moved, then he must update the window


def menu_screen():
    """
    this function welcome the user and make him to choose a partner to play,
    then start game and send to different window
    :return: nothing is return, only display the menu gui
    """
    run = True
    clock = pygame.time.Clock()

    py_window.blit(background_image, [0, 0])
    font = pygame.font.SysFont("javanesetext", 60)
    text = font.render("MANCALA", True, BLACK_RED)
    py_window.blit(text, (150, 10))
    font2 = pygame.font.SysFont("comicsans", 50)
    text2 = font2.render("Choose your partner", True, BLACK_RED)
    py_window.blit(text2, (70, 150))

    type_player = [Button(100, 250, 180, 40, WOOD, "computer"), Button(330, 250, 180, 40, LIGHT_WOOD, "human")]

    for btn in type_player:
        btn.draw(py_window)
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

    if index == 0:  # if user want to play with computer, is created ComputerGame object
        # and called the playGame function for game logics
        # when is over, the user is returned to menu screen
        game = ComputerGame(py_window, buttons, background_image)
        game.playGame()
        menu_screen()
    elif index == 1:  # the if he want to play with human, then run game function from above is called and
        # returned to menu screen when the game is over
        run_game()
        menu_screen()


if __name__ == "__main__":
    while True:
        try:
            menu_screen()  # here start the gui
        except Exception as e:
            print(str(e))
            break
