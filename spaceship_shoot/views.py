import pygame
import random
import os
from django.shortcuts import render
from django.http import JsonResponse
import json

# 加载玩家飞船图片
play_ship_img = "game_info/game_image/汤姆猫.jpg"

# 设置游戏窗口尺寸
width = 800
height = 600

image_size = 50
# 加载玩家飞船图片
play_ship_x = width // 2 - image_size // 2
play_ship_y = height - image_size
# 加载敌人飞船图片
enemy_ship_img = "game_info/game_image/杰利鼠.png"
enemies_location = []

# 定义子弹列表
bullets = []
bullet_size = 4
score = 0


def generate_enemy(n):
    for _ in range(n):
        enemy_x = random.randint(0, width - image_size)
        enemy_y = random.randint(-250, -50)
        enemies_location.append({"loc_x": enemy_x, "loc_y": enemy_y})


def generate_bullet(_bullet_x):
    bullet_x = _bullet_x+image_size//2
    bullet_y = height - image_size - bullet_size
    bullets.append({"bullet_x": bullet_x,
                    "bullet_y": bullet_y})


# 修改 update_space_ship_state 函数
def update_space_ship_state(request):
    global score
    game_data = {
        'game_over': False,
        'cur_bullets': bullets,
        'score': score,
        'cur_enemies': enemies_location,
        'cur_play_ship_x': play_ship_x
    }
    if request.method == 'POST':
        data_json = request.body.decode('utf-8')
        data = json.loads(data_json)

        key_event = data.get('key_event', None)
        cur_bullets = data.get('cur_bullets', None)
        cur_enemies = data.get('cur_enemies', None)
        cur_play_ship_x = data.get('cur_play_ship_x', None)
        print("request.method :", key_event)
        if key_event == 'ArrowLeft':
            cur_play_ship_x -= 10
        elif key_event == 'ArrowRight':
            cur_play_ship_x += 10
        elif key_event == 'ArrowUp':
            generate_bullet(cur_play_ship_x)
            cur_bullets.extend(bullets)
        # 碰撞则 #删除子弹 删除敌机
        for each_bullet in cur_bullets:
            for each_enemy in cur_enemies:
                if each_bullet['bullet_x'] >= each_enemy['loc_x'] \
                        and each_bullet['bullet_x'] <= each_enemy['loc_x'] + image_size \
                        and each_bullet['bullet_y'] <= each_enemy['loc_y'] + image_size:
                    cur_bullets.remove(each_bullet)
                    generate_enemy(1)
                    score += 1

        # 敌机到底部则消失
        for each_enemy in cur_enemies:
            each_enemy['loc_y'] += 2
            print("YY")
            if each_enemy['loc_y'] >= height:
                cur_enemies.remove(each_enemy)
                generate_enemy(1)
        # 子弹到顶部则消失
        for each_bullet in cur_bullets:
            each_bullet['bullet_y']-=2
            if each_bullet['bullet_y'] >= height:
                cur_bullets.remove(each_bullet)
        # 战机碰撞敌机则游戏结束
        for each_enemy in cur_enemies:
            if (play_ship_x - each_enemy['loc_x'] < image_size or each_enemy['loc_x'] - play_ship_x < image_size) and \
                    each_enemy['loc_y'] + image_size >= play_ship_y:
                game_data['game_over'] = True
        game_data['cur_enemies'] = cur_enemies
        game_data['cur_bullets'] = cur_bullets
        game_data['score'] = score
        game_data['cur_play_ship_x'] = cur_play_ship_x
        print("game_data:",game_data)
        return JsonResponse(game_data)


def spaceship_shoot(request):
    generate_enemy(5)
    context = {'play_ship_x': play_ship_x,
               'play_ship_y': play_ship_y,
               'play_ship_img': json.dumps(play_ship_img),
               'enemies_location': json.dumps(enemies_location),
               'enemy_ship_img': json.dumps(enemy_ship_img),
               'score': 0,
               "bullets": json.dumps(bullets),
               'image_size': image_size,
               'bullet_size': bullet_size}
    print(context)
    return render(request, "spaceship_shoot/spaceship_shoot_v1.html", context)
