import pygame
import random
from django.shortcuts import render
from django.http import JsonResponse

# # 游戏窗口设置
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480

# 颜色定义
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)
#
# 贪吃蛇相关设置
snake_size = 10
move_speed = 5


def new_food(n):
    # 初始化食物点的位置列表
    food_positions = []

    # 在游戏初始化时，生成5个食物点的位置
    for _ in range(n):
        food_x = round(random.randrange(0, WINDOW_WIDTH - snake_size) / 10) * 10
        food_y = round(random.randrange(0, WINDOW_HEIGHT - snake_size) / 10) * 10
        food_positions.append({"x": food_x, "y": food_y})
    return food_positions


foods = new_food(random.randint(3, 5))

# 初始贪吃蛇长度
snakes = []
length_of_snake = 1
location_x = WINDOW_WIDTH // 2
location_y = WINDOW_HEIGHT // 2
first_snake = {"x": location_x, "y": location_y}
snakes.append(first_snake)


def update_snake_state(request):
    snake_speed_x, snake_speed_y = 0, 0
    global length_of_snake
    game_data = {
        "game_over": False,
        "foods": foods,
        "snakes": snakes
    }

    # 判断是否出界
    if request.method == 'POST':
        key_event = request.POST.get('key_event', None)
        # foods = request.POST.get('foods', None)
        # x1 = request.POST.get('x1', None)
        # y1 = request.POST.get('y1', None)
        # snakes = request.POST.get('snakes', None)
        x1 = WINDOW_WIDTH / 2
        y1 = WINDOW_HEIGHT / 2
        if x1 >= WINDOW_WIDTH or x1 < 0 or y1 >= WINDOW_HEIGHT or y1 < 0:
            game_data['game_over'] = True
        if key_event == 'ArrowLeft':
            snake_speed_x = -snake_size
            snake_speed_y = 0
        elif key_event == 'ArrowRight':
            snake_speed_x = snake_size
            snake_speed_y = 0
        elif key_event == 'ArrowUp':
            snake_speed_y = -snake_size
            snake_speed_x = 0
        elif key_event == 'ArrowDown':
            snake_speed_y = snake_size
            snake_speed_x = 0
        x1 += snake_speed_x
        y1 += snake_speed_y

        # 绘制贪吃蛇，snake_head在列表的队尾
        snake_head = {"x": x1, "y": y1}
        snakes.append(snake_head)

        # 吃到食物的逻辑
        for each_food in foods:
            if x1 == each_food['x'] and y1 == each_food['y']:
                foods.remove(each_food)
                length_of_snake += 1

        # 移除蛇尾的块，如果吃到食物，则不需要移除
        if len(snakes) > length_of_snake:
            del snakes[0]

        # 蛇咬到自己，游戏结束
        for x in snakes[:-1]:
            if x == snake_head:
                game_data['game_over'] = True

        if len(foods) < 5:
            foods.extend(new_food(5))

        game_data["foods"] = foods
        game_data["snakes"] = snakes

        return JsonResponse(game_data)


def snake(request):
    print(foods)
    print(snakes)
    return render(request, "snake/snake_v1.html", {"WINDOW_WIDTH": WINDOW_WIDTH,
                                                   "WINDOW_HEIGHT": WINDOW_HEIGHT,
                                                   "move_speed": move_speed,
                                                   "snake_size": snake_size,
                                                   "Origin_foods": foods,
                                                   "Snakes": snakes})
