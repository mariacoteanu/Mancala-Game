import pygame
from store import Store
pygame.font.init()


class Button(Store):
    def __init__(self, x, y, width, height, color, text):
        super().__init__(x, y, width, height, color, text)
        self.hovered = False

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
