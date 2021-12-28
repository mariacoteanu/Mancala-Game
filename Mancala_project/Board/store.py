"""
this file contain the blueprint of a rectangular, is the storage of every player points
"""
import pygame
pygame.font.init()


class Store:
    def __init__(self, x, y, width, height, color, text):
        """Store constructor where are initialized the position where is created, width, height,
        color and text on this storage"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, py_window):
        """in this function is draw on pygame window an rectangular"""
        pygame.draw.rect(py_window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (255, 255, 255))
        py_window.blit(text, (self.x+round(self.width/2)-round(text.get_width()/2),
                              self.y+round(self.height/2)-round(text.get_height()/2)))

    def click(self, pos):
        """this storage can not be clicked/modified by user"""
        return False

    def set_text(self, text):
        """update the text on the store, is used by all inherited classes"""
        self.text = text
