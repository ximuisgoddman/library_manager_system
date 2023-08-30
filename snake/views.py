# import pygame
# import random
from django.shortcuts import render


#
# # 初始化 pygame
# pygame.init()
#
# # 游戏窗口设置
# win_width, win_height = 640, 480
# win = pygame.display.set_mode((win_width, win_height))
# pygame.display.set_caption("Snake Game")
#
# # 颜色定义
# white = (255, 255, 255)
# green = (0, 255, 0)
# red = (255, 0, 0)
# black = (0, 0, 0)
#
# # 贪吃蛇相关设置
# snake_block = 10
# snake_speed = 5
#
# # 字体设置
# font_style = pygame.font.SysFont(None, 50)
# score_font = pygame.font.SysFont(None, 35)
#
#
# # 显示分数
# def Your_score(score):
#     value = score_font.render("Your Score: " + str(score), True, white)
#     win.blit(value, [0, 0])
#
#
# def gameLoop():
#     game_over = False
#     game_close = False
#
#     # 初始贪吃蛇位置
#     x1 = win_width // 2
#     y1 = win_height // 2
#
#     # 初始贪吃蛇速度
#     x1_change = 0
#     y1_change = 0
#
#     # 初始贪吃蛇长度
#     snake_list = []
#     length_of_snake = 1
#
#     # 食物初始位置
#     foods = new_food(random.randint(3, 5))
#
#     # 游戏循环
#     while not game_over:
#
#         while game_close == True:
#             win.fill(black)
#             message("You Lost! Press Q-Quit or C-Play Again", red)
#             Your_score(length_of_snake - 1)
#             pygame.display.update()
#
#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_q:
#                         game_over = True
#                         game_close = False
#                     if event.key == pygame.K_c:
#                         gameLoop()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 game_over = True
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     x1_change = -snake_block
#                     y1_change = 0
#                 elif event.key == pygame.K_RIGHT:
#                     x1_change = snake_block
#                     y1_change = 0
#                 elif event.key == pygame.K_UP:
#                     y1_change = -snake_block
#                     x1_change = 0
#                 elif event.key == pygame.K_DOWN:
#                     y1_change = snake_block
#                     x1_change = 0
#
#         # 判断是否出界
#         if x1 >= win_width or x1 < 0 or y1 >= win_height or y1 < 0:
#             game_close = True
#
#         x1 += x1_change
#         y1 += y1_change
#         win.fill(black)
#         for foodx, foody in foods:
#             # 绘制食物
#             pygame.draw.rect(win, green, [foodx, foody, snake_block, snake_block])
#
#         # 绘制贪吃蛇
#         snake_head = []
#         snake_head.append(x1)
#         snake_head.append(y1)
#         snake_list.append(snake_head)
#         if len(snake_list) > length_of_snake:
#             del snake_list[0]
#
#         for x in snake_list[:-1]:
#             if x == snake_head:
#                 game_close = True
#
#         our_snake(snake_block, snake_list)
#         Your_score(length_of_snake - 1)
#
#         pygame.display.update()
#
#         # 在 gameLoop 函数中修改吃到食物的逻辑
#         for food_x, food_y in foods:
#             if x1 == food_x and y1 == food_y:
#                 foods.remove((food_x, food_y))
#                 length_of_snake += 1
#         if len(foods) < 5:
#             foods.extend(new_food(5))
#
#         pygame.display.update()
#
#         pygame.time.Clock().tick(snake_speed)
#
#     pygame.quit()
#     quit()
#
#
# # 在 gameLoop 函数中定义一个新的函数用于生成新点的位置
# def new_food(n):
#     # 初始化食物点的位置列表
#     food_positions = []
#
#     # 在游戏初始化时，生成5个食物点的位置
#     for _ in range(n):
#         food_x = round(random.randrange(0, win_width - snake_block) / 10.0) * 10.0
#         food_y = round(random.randrange(0, win_height - snake_block) / 10.0) * 10.0
#         food_positions.append((food_x, food_y))
#     return food_positions
#
#
# def our_snake(block, snake_list):
#     for x in snake_list:
#         pygame.draw.rect(win, white, [x[0], x[1], block, block])
#
#
# def message(msg, color):
#     mesg = font_style.render(msg, True, color)
#     win.blit(mesg, [win_width / 6, win_height / 3])
#
#
# 游戏开始
# gameLoop()
#
#
def snake(request):
    return render(request, "snake/snake_v1.html")
