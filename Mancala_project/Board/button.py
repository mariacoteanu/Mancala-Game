import pygame

pygame.font.init()

class Button:
    def __init__(self, x, y, radius, color, text):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text

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

    def setText(self, text):
        self.text = text