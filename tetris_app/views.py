from django.shortcuts import render
from django.http import JsonResponse
import pygame
import random
import json

# 游戏窗口的宽度和高度
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 游戏区域的宽度和高度
PLAY_WIDTH = 400
PLAY_HEIGHT = 600
# 游戏区域的位置
PLAY_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
PLAY_Y = WINDOW_HEIGHT - PLAY_HEIGHT
# 方块大小
BLOCK_SIZE = 10

# 方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 1, 0]]  # T
]

# 颜色列表
COLORS = [
    (0, 0, 0),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 255, 255),
    (128, 0, 128)
]

# 全局变量
current_piece = None
play_matrix = [[0] * (PLAY_WIDTH // BLOCK_SIZE) for _ in range(PLAY_HEIGHT // BLOCK_SIZE)]


def create_new_piece():
    shape = random.choice(SHAPES)
    piece = {
        'shape': shape,
        'color': random.randint(1, len(COLORS) - 1),
        'x': (PLAY_WIDTH // BLOCK_SIZE) // 2 - len(shape[0]) // 2,
        'y': 0
    }
    return piece


def check_collision(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                if (piece['y'] + i >= PLAY_HEIGHT // BLOCK_SIZE or
                        piece['x'] + j < 0 or piece['x'] + j >= PLAY_WIDTH // BLOCK_SIZE or
                        play_matrix[piece['y'] + i][piece['x'] + j] != 0):
                    return True
    return False


def place_piece(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                play_matrix[piece['y'] + i][piece['x'] + j] = piece['color']


def clear_rows():
    rows_cleared = 0
    for i in range(len(play_matrix)):
        if all(play_matrix[i]):
            del play_matrix[i]
            play_matrix.insert(0, [0] * (PLAY_WIDTH // BLOCK_SIZE))
            rows_cleared += 1
    return rows_cleared


def draw(window):
    window.fill(COLORS[0])
    for i in range(len(play_matrix)):
        for j in range(len(play_matrix[0])):
            pygame.draw.rect(window, COLORS[play_matrix[i][j]],
                             (PLAY_X + j * BLOCK_SIZE, PLAY_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(window, COLORS[7], (PLAY_X, PLAY_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


def draw_piece(piece, window):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                pygame.draw.rect(window, COLORS[piece['color']],
                                 (PLAY_X + (piece['x'] + j) * BLOCK_SIZE, PLAY_Y + (piece['y'] + i) * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)


def update_game_state(request):
    global current_piece

    game_data = {
        'game_over': False,
        'play_matrix': play_matrix,
        'score': 0,
        'current_piece': current_piece
    }

    if current_piece is None:
        current_piece = create_new_piece()
        if check_collision(current_piece):
            game_data['game_over'] = True
    print("request.POST:", request.POST)
    if request.method == 'POST':
        key_event = request.POST.get('key_event', None)
        print("key_event:", request.POST.get('key_event', None))
        if key_event == 'ArrowLeft':
            current_piece['x'] -= 1
            if check_collision(current_piece):
                current_piece['x'] += 1
        elif key_event == 'ArrowRight':
            current_piece['x'] += 1
            if check_collision(current_piece):
                current_piece['x'] -= 1
        elif key_event == 'ArrowDown':
            current_piece['y'] += 1
            if check_collision(current_piece):
                current_piece['y'] -= 1
        elif key_event == 'ArrowUp':
            # 处理旋转方块的代码
            rotated_shape = list(zip(*reversed(current_piece['shape'])))
            if not check_collision({'shape': rotated_shape, 'x': current_piece['x'], 'y': current_piece['y']}):
                current_piece['shape'] = rotated_shape
    print("current_piece", current_piece)
    current_piece['y'] += 1
    if check_collision(current_piece):
        current_piece['y'] -= 1
        place_piece(current_piece)
        rows_cleared = clear_rows()
        if rows_cleared > 0:
            game_data['score'] += 100 * (2 ** (rows_cleared - 1))
        current_piece = create_new_piece()
        if check_collision(current_piece):
            game_data['game_over'] = True
    game_data['current_piece'] = current_piece
    game_data['play_matrix'] = play_matrix
    print(game_data)
    return JsonResponse(game_data)


def tetris(request):
    shapes_data = json.dumps(SHAPES)
    colors_data = json.dumps(COLORS)
    play_matrix = [[0] * (PLAY_WIDTH // BLOCK_SIZE) for _ in range(PLAY_HEIGHT // BLOCK_SIZE)]

    return render(request, 'tetris_app/tetris.html', {'SHAPES_DATA': shapes_data,
                                                      'COLORS_DATA': colors_data,
                                                      'WINDOW_WIDTH': WINDOW_WIDTH,
                                                      'WINDOW_HEIGHT': WINDOW_HEIGHT,
                                                      'PLAY_WIDTH': PLAY_WIDTH,
                                                      'PLAY_HEIGHT': PLAY_HEIGHT,
                                                      'PLAY_X': PLAY_X,
                                                      'PLAY_Y': PLAY_Y,
                                                      'BLOCK_SIZE': BLOCK_SIZE,
                                                      'PLAY_MATRIX': json.dumps(play_matrix),
                                                      'score': 0})
