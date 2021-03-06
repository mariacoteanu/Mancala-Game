"""
in this file is the blueprint of CircleButton class, inherited from Button class
"""
from button import Button
import pygame


class CircleButton(Button):
    def __init__(self, x, y, radius, color, text):
        """
        the CircleButton constructor where first initialize the parent and added private variables
        radius and the button status -- if is active or not
        """
        super().__init__(x, y, radius, radius, color, text)
        self.radius = radius
        self.active = False

    def draw(self, py_window):
        """
        overridden function from parent where draw circle button
        :param py_window: pygame window where add elements
        :return: nothing is returned, only draw circle buttons on user window
        """
        pygame.draw.circle(py_window, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, True, (255, 255, 255))
        py_window.blit(text, (self.x-round(text.get_width()/2),
                              self.y-round(text.get_height()/2)))

    def click(self, click_position):
        """
        overridden function from parent where is defined the effect of MousePressed
        the different thant the parent's function is the area where the click might be valid around button
        :param click_position: mouse pressed position
        :return: True, if is inside of circle, and False otherwise
        """
        if self.active:
            x1 = click_position[0]
            y1 = click_position[1]

            if self.x-self.radius <= x1 <= self.x+self.radius \
                    and self.y-self.radius <= y1 <= self.y+self.radius:
                return True
            else:
                return False
        else:
            return False
