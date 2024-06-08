import pygame

pygame.init()

monitor_width = 1600
monitor_height = 850

bg = pygame.image.load("bg.png")

bg = pygame.transform.scale(bg, (monitor_width, monitor_height))

clock = pygame.time.Clock()

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

class Player(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed

player1 = Player("tank1.png", -200, 200, 900, 550, 10)
player2 = Player("tank2.png", 1000, 200, 900, 550, 10)

wall1 = GameSprite("wall.png", 535, 100, 40, 200)
wall2 = GameSprite("wall.png", 1035, 100, 40, 200)
wall3 = GameSprite("wall.png", 800, 350, 40, 200)
wall4 = GameSprite("wall.png", 485, 600, 40, 200)
wall5 = GameSprite("wall.png", 1085, 600, 40, 200)

barrel1 = GameSprite("barrel.png", 455, 200, 80, 100)
barrel2 = GameSprite("barrel.png", 1075, 200, 80, 100)
barrel3 = GameSprite("barrel.png", 840, 400, 80, 100)
barrel4 = GameSprite("barrel.png", 720, 400, 80, 100)
barrel5 = GameSprite("barrel.png", 525, 600, 80, 100)
barrel6 = GameSprite("barrel.png", 1005, 600, 80, 100)

exit = False

while not exit:
    monitor.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            
    player1.show()
    player2.show()

    wall1.show()
    wall2.show()
    wall3.show()
    wall4.show()
    wall5.show()

    barrel1.show()
    barrel2.show()
    barrel3.show()
    barrel4.show()
    barrel5.show()
    barrel6.show()

    pygame.display.update()
    clock.tick(60)