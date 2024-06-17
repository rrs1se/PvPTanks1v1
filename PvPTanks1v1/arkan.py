import pygame
import pygame.font
 
 
 
pygame.init()
 
win_width = 500
win_height = 500
 
bg = pygame.image.load("background.png")
 
bg = pygame.transform.scale(bg, (win_width, win_height))
 
clock = pygame.time.Clock()
 
window = pygame.display.set_mode((win_width, win_height))
window_rect = window.get_rect()
 
pygame.display.set_caption("Arcanoid")
 
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(new_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed) -> None:
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.init_x = x
        self.init_y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.width = width
    
    def restart(self):
        self.rect.x = self.init_x
        self.rect.y = self.init_y

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.x < win_width - self.width:
            self.rect.x += self.speed
    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Enemy(GameSprite):
    def __init__(self, new_image, x, y, width, height) -> None:
        super().__init__(new_image, x, y, width, height)
 
class Ball(GameSprite):
    def __init__(self, new_image, x, y, width, height, speed) -> None:
        super().__init__(new_image, x, y, width, height)
        self.width = width
        self.init_x = x
        self.init_y = y
        self.init_speed = speed
        self.velocity = [speed, -speed]

    def restart(self):
        self.rect.x = self.init_x
        self.rect.y = self.init_y
        self.velocity = [self.init_speed, -self.init_speed]
 
    def update(self):
        # Проверяем столкновение мяча с платформой
        if pygame.sprite.collide_rect(self, platform):
            # Расчет точки столкновения
            ball_center_x = self.rect.centerx
            platform_center_x = platform.rect.centerx
            platform_width = platform.rect.width
 
            # Динамическая смена направления мяча в зависимости от точки столкновения
            hit_position = (ball_center_x - platform_center_x) / (platform_width / 2)
            self.velocity[0] = self.velocity[0] + hit_position * 2  # Множитель для изменения скорости по X
            self.velocity[1] = -self.velocity[1]  # Инверсия скорости по Y
        if pygame.sprite.spritecollide(self, enemies, True):
            self.velocity[1] = -self.velocity[1]
        if self.rect.x > win_width - self.width:
            self.velocity[0] = -self.velocity[0]
        if self.rect.x < 0:
            self.velocity[0] = abs(self.velocity[0])
        if self.rect.y < 0:
            self.velocity[1] = abs(self.velocity[1])
        # Двигаем мяч
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
 
enemies = pygame.sprite.Group()

def calculate_enemy_positions(screen_width, enemy_width, enemy_height):
    rows = [8, 7, 6]  # Количество врагов в каждом ряду
    y = 0
    positions = []
    for enemy_count in rows:
        total_width = enemy_width * enemy_count
        spacing = (screen_width - total_width) / (enemy_count + 1)
        
        for i in range(enemy_count):
            x = spacing + i * (enemy_width + spacing)
            positions.append((x, y))
        y += enemy_height
    
    return positions
 
def spawn_enemy():
    enemy_width, enemy_height = 80, 80
 
    enemy_positions = calculate_enemy_positions(win_width, enemy_width, enemy_height)

    for pos in enemy_positions:
        enemies.add(Enemy('enemy.png', pos[0], pos[1], enemy_width, enemy_height))
 
platform = Platform(win_width/2, win_height * 0.8, 100, 20, 8)
ball = Ball('ball.png', win_width/2, win_height/2, 50, 50, 5)
 
finish = False
 
paused = True
 
game_over_text = ''
 
font = pygame.font.SysFont(None, 36)
 
exit = False
spawn_enemy()
 
while not exit:
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:
            exit = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and not finish:
                paused = not paused  # Toggle the paused state
            if event.key == pygame.K_r and finish:
                platform.restart()
                ball.restart()
                enemies.empty()
                spawn_enemy()
                finish = False
                paused = True
    
    if ball.rect.y > platform.rect.y + 50:
        game_over_text = font.render("Ти програв!", True, (255, 0, 0))
        finish = True
    if not enemies.sprites():
        game_over_text = font.render("Ти переміг!", True, (0, 255, 0))
        finish = True

    window.blit(bg, (0, 0))
 
    if not finish and not paused:
        platform.update()
        ball.update()
 
    platform.show()
    ball.show()
    enemies.draw(window)
 
    if finish:
        canavs_rect = window.get_rect()
        window.blit(game_over_text, (canavs_rect.centerx - 70, canavs_rect.centery))
        window.blit(font.render('Натисніть R для продовження.', True, (255,255,255)), (canavs_rect.centerx - 170, canavs_rect.centery + 40))
    if paused:
        canavs_rect = window.get_rect()
        window.blit(font.render('Гру зупинено!', True, (255,255,255)), (canavs_rect.centerx - 100, canavs_rect.centery))
        window.blit(font.render('Натисніть ESC для продовження.', True, (255,255,255)), (canavs_rect.centerx - 200, canavs_rect.centery + 40))
 
    pygame.display.update()
    clock.tick(60)