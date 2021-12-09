from button import Button
import pygame


class CircleButton(Button):
    def __init__(self, x, y, radius, color, text):
        super().__init__(x, y, radius, radius, color, text)
        self.radius = radius

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x - round(text.get_width() / 2),
                        self.y - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x - self.radius <= x1 <= self.x + self.radius and self.y - self.radius <= y1 <= self.y + self.radius:
            return True
        else:
            return False
