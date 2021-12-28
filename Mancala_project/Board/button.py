"""
this file contain the blueprint of Button class who is parent for CircleButton and child for Store
the different between he and his father is the fact that he can be clicked and define a base for other types of buttons
"""
import pygame
from store import Store
pygame.font.init()


class Button(Store):
    def __init__(self, x, y, width, height, color, text):
        """Button constructor where initialize the parent constructor"""
        super().__init__(x, y, width, height, color, text)

    def click(self, pos):
        """
        overrides the parent click function where define the area inside of button
        :param pos: position where mouse is pressed
        :return: True if is inside of button and False otherwise
        """
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
