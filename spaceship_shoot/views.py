import pygame
import random
import os
base_dir=os.path.dirname(os.path.dirname(__file__))
# 加载玩家飞船图片
player_ship = pygame.image.load(os.path.join(base_dir,"my_resource/game_info/game_image/汤姆猫.jpg"))
player_ship = pygame.transform.scale(player_ship, (50, 50))
import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置游戏窗口尺寸
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

# 设置游戏标题
pygame.display.set_caption("飞行射击游戏")

# 加载玩家飞船图片
# player_ship = pygame.image.load("player_ship.png")
player_rect = player_ship.get_rect()
player_rect.centerx = width // 2
player_rect.bottom = height - 10

# 加载敌人飞船图片
enemy_ship = pygame.image.load(os.path.join(base_dir,"my_resource/game_info/game_image/杰利鼠.png"))
enemy_ship = pygame.transform.scale(enemy_ship, (50, 50))
enemies = []
for _ in range(5):
    enemy = enemy_ship.get_rect()
    enemy.x = random.randint(0, width - enemy.width)
    enemy.y = random.randint(-200, -50)
    enemies.append(enemy)

# 定义子弹列表
bullets = []

# 设置字体
font = pygame.font.Font(None, 36)

# 设置得分
score = 0

# 游戏循环
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(pygame.Rect(player_rect.centerx - 2, player_rect.top, 4, 10))  # 创建一个子弹矩形

    # 移动玩家飞船
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.move_ip(-5, 0)
    if keys[pygame.K_RIGHT]:
        player_rect.move_ip(5, 0)

    # 移动子弹
    for bullet in bullets:
        bullet.move_ip(0, -10)
        if bullet.bottom <= 0:
            bullets.remove(bullet)

    # 移动敌人
    for enemy in enemies:
        enemy.y += 2
        if enemy.y > height:
            enemy.y = random.randint(-200, -50)
            enemy.x = random.randint(0, width - enemy.width)

    # 检测碰撞
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            running = False
        for bullet in bullets:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemy.y = random.randint(-200, -50)
                enemy.x = random.randint(0, width - enemy.width)
                score += 10

    # 绘制背景
    screen.fill((0, 0, 0))

    # 绘制玩家飞船
    screen.blit(player_ship, player_rect)

    # 绘制敌人
    for enemy in enemies:
        screen.blit(enemy_ship, enemy)

    # 绘制子弹
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 255), bullet)

    # 绘制得分
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# 退出游戏
pygame.quit()
