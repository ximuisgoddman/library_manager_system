import json
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


origin_foods = new_food(random.randint(3, 5))

# 初始贪吃蛇长度
Origin_snakes = []
location_x = WINDOW_WIDTH // 2
location_y = WINDOW_HEIGHT // 2
first_snake = {"x": location_x, "y": location_y}
Origin_snakes.append(first_snake)


# snake_speed_x, snake_speed_y = 0, 0


def update_snake_state(request):
    # x1 = WINDOW_WIDTH // 2
    # y1 = WINDOW_HEIGHT // 2

    game_data = {
        "game_over": False,
        "foods": origin_foods,
        "snakes": Origin_snakes
    }
    # 使用全局变量获取方向键，如果没有按键，则延续上一次的方向
    # global snake_speed_x
    # global snake_speed_y
    # 判断是否出界

    if request.method == 'POST':
        data_json = request.body.decode('utf-8')
        data = json.loads(data_json)
        # key_event = request.POST.get('key_event', None)
        # 获取食物和蛇的字符串数据

        # 将字符串转换为 Python 对象
        foods = data.get("foods", [])
        snakes = data.get("snakes", [])
        x1 = int(data.get('x1', 0))
        y1 = int(data.get('y1', 0))
        if_extend_food = data.get('if_extend_food', False)
        length_of_snake = data.get('length_of_snake', 1)


        if x1 >= WINDOW_WIDTH or x1 < 0 or y1 >= WINDOW_HEIGHT or y1 < 0:
            game_data['game_over'] = True

        # 吃到食物的逻辑
        for each_food in foods:
            if x1 == each_food['x'] and y1 == each_food['y']:
                foods.remove(each_food)
                length_of_snake += 1
        print(len(snakes), length_of_snake, len(foods), if_extend_food)
        # 移除蛇尾的块，如果吃到食物，则不需要移除
        if len(snakes) > length_of_snake:
            del snakes[0]
        snake_head = {"x": x1, "y": y1}
        # 蛇咬到自己，游戏结束
        for x in snakes[:-1]:
            if x == snake_head:
                game_data['game_over'] = True

        if if_extend_food:
            foods.extend(new_food(5))

        game_data["foods"] = json.dumps(foods)
        game_data["snakes"] = json.dumps(snakes)
        game_data["length_of_snake"] = length_of_snake
        print(game_data['game_over'])
        return JsonResponse(game_data)


def snake(request):
    return render(request, "snake/snake_v1.html", {"WINDOW_WIDTH": WINDOW_WIDTH,
                                                   "WINDOW_HEIGHT": WINDOW_HEIGHT,
                                                   "move_speed": move_speed,
                                                   "snake_size": snake_size,
                                                   "Origin_foods": json.dumps(origin_foods),
                                                   "Origin_Snakes": json.dumps(Origin_snakes)})
