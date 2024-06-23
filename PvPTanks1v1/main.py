import pygame

pygame.init()

monitor_width = 800
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
    def __init__(self, new_image, x, y, width, height, speed, angle) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed
        self.width = width
        self.height = height
        self.angle = angle
        self.original = self.image.copy()
        self.rotate()
    
    def rotate(self):
        self.image = pygame.transform.rotate(self.original, 360 - self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def check_collide(self, move_vec):
        print(move_vec)
        new_rect = self.rect.move(move_vec)
        collision_sprites = pygame.sprite.spritecollide(self, game_objects, False)
        
        for obj in collision_sprites:
            obj_rect = obj.rect
            if move_vec.x > 0:
                new_rect.right = obj_rect.left
            if move_vec.x < 0:
                new_rect.left = obj_rect.right
            if move_vec.y > 0:
                new_rect.bottom = obj_rect.top
            if move_vec.y < 0:
                new_rect.top = obj_rect.bottom
        
        self.rect = new_rect
        

    def update_L(self):
        keys = pygame.key.get_pressed()
        move_vec = pygame.math.Vector2()

        if keys[pygame.K_w]:
            move_vec.from_polar((self.speed, self.angle))
            # self.rect.center += move_vec
            self.check_collide(move_vec)
        if keys[pygame.K_s]:
            move_vec.from_polar((self.speed, self.angle))
            # self.rect.center -= move_vec
            self.check_collide(-move_vec)
        if keys[pygame.K_a]:
            self.angle -= 3
            self.rotate()
        if keys[pygame.K_d]:
            self.angle += 3
            self.rotate()

    
    def update_R(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < monitor_height - self.height:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.angle -= 2
            self.rotate()
        if keys[pygame.K_RIGHT]:
            self.angle += 2
            self.rotate()

class Bullet(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= monitor_height/2 + 50:
            self.kill()  # Remove the bullet when it goes off the screen

player1 = Player("tank1.png", 100, 400, 120, 80, 3, 90)
player2 = Player("tank2.png", 1300, 400, 155, 100, 3, 270)

wall1 = GameSprite("wall.png", 535, 100, 40, 200)
wall2 = GameSprite("wall.png", 1050, 100, 40, 200)
wall3 = GameSprite("wall.png", 800, 350, 40, 200)
wall4 = GameSprite("wall.png", 500, 600, 40, 200)
wall5 = GameSprite("wall.png", 1100, 600, 40, 200)


barrel1 = GameSprite("barrel.png", 455, 220, 80, 80)
barrel2 = GameSprite("barrel.png", 1090, 220, 80, 80)
barrel3 = GameSprite("barrel.png", 840, 420, 80, 80)
barrel4 = GameSprite("barrel.png", 720, 420, 80, 80)
barrel5 = GameSprite("barrel.png", 540, 620, 80, 80)
barrel6 = GameSprite("barrel.png", 1020, 620, 80, 80)

obj = [wall1, wall2, wall3, wall4, wall5, barrel1, barrel2, barrel3, barrel4, barrel5, barrel6]

game_objects = pygame.sprite.Group()
game_objects.add(obj)

exit = False

while not exit:
    monitor.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
            
    player1.update_L()
    player2.update_R()

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