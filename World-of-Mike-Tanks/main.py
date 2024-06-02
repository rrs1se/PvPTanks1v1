import pygame

pygame.init()

monitor_width = 1600
monitor_height = 850

bg = pygame.image.load("image.png")

bg = pygame.transform.scale(bg, (monitor_width, monitor_height))

monitor = pygame.display.set_mode((monitor_width, monitor_height))

pygame.display.set_caption("World of Mike Tanks")

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        monitor.blit(self.image, (self.rect.x, self.rect.y))

class Tanks(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed


class Enemy(GameSprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__(new_image, x, y, width, height)

exit = False

while not exit:
    monitor.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()