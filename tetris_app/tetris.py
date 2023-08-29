import pygame
import random

# 游戏窗口的宽度和高度
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 游戏区域的宽度和高度
PLAY_WIDTH = 300
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

# 初始化 Pygame
pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("俄罗斯方块")

# 游戏区域的矩阵表示
play_matrix = [[0] * (PLAY_WIDTH // BLOCK_SIZE) for _ in range(PLAY_HEIGHT // BLOCK_SIZE)]


# 创建一个新的方块
def create_new_piece():
    shape = random.choice(SHAPES)
    piece = {
        'shape': shape,
        'color': random.randint(1, len(COLORS) - 1),
        'x': (PLAY_WIDTH // BLOCK_SIZE) // 2 - len(shape[0]) // 2,
        'y': 0
    }
    return piece


# 检查方块是否与游戏区域碰撞
def check_collision(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                if (piece['y'] + i >= PLAY_HEIGHT // BLOCK_SIZE or
                        piece['x'] + j < 0 or piece['x'] + j >= PLAY_WIDTH // BLOCK_SIZE or
                        play_matrix[piece['y'] + i][piece['x'] + j] != 0):
                    return True
    return False


# 将方块放入游戏区域
def place_piece(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                play_matrix[piece['y'] + i][piece['x'] + j] = piece['color']


# 消除满行的方块
def clear_rows():
    rows_cleared = 0
    for i in range(len(play_matrix)):
        if all(play_matrix[i]):
            del play_matrix[i]
            play_matrix.insert(0, [0] * (PLAY_WIDTH // BLOCK_SIZE))
            rows_cleared += 1
    return rows_cleared


# 绘制游戏区域和方块
def draw():
    window.fill(COLORS[0])
    for i in range(len(play_matrix)):
        for j in range(len(play_matrix[0])):
            pygame.draw.rect(window, COLORS[play_matrix[i][j]],
                             (PLAY_X + j * BLOCK_SIZE, PLAY_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    pygame.draw.rect(window, COLORS[7], (PLAY_X, PLAY_Y, PLAY_WIDTH, PLAY_HEIGHT), 5)


# 绘制当前方块
def draw_piece(piece):
    for i in range(len(piece['shape'])):
        for j in range(len(piece['shape'][0])):
            if piece['shape'][i][j] == 1:
                pygame.draw.rect(window, COLORS[piece['color']],
                                 (PLAY_X + (piece['x'] + j) * BLOCK_SIZE, PLAY_Y + (piece['y'] + i) * BLOCK_SIZE,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)


# 主游戏循环
def main():
    clock = pygame.time.Clock()
    piece = create_new_piece()
    game_over = False
    score = 0
    drop_timer = 0
    drop_interval = 1000  # 方块下落的时间间隔（毫秒）

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece['x'] -= 1
                    if check_collision(piece):
                        piece['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    piece['x'] += 1
                    if check_collision(piece):
                        piece['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    piece['y'] += 1
                    if check_collision(piece):
                        piece['y'] -= 1
                elif event.key == pygame.K_UP:
                    # 方块形状变换
                    rotated_shape = list(zip(*reversed(piece['shape'])))
                    if not check_collision({'shape': rotated_shape, 'x': piece['x'], 'y': piece['y']}):
                        piece['shape'] = rotated_shape

        drop_timer += clock.get_rawtime()
        clock.tick()
        if drop_timer >= drop_interval:
            drop_timer = 0
            piece['y'] += 1
            if check_collision(piece):
                piece['y'] -= 1
                place_piece(piece)
                rows_cleared = clear_rows()
                if rows_cleared > 0:
                    score += 100 * (2 ** (rows_cleared - 1))
                piece = create_new_piece()
                if check_collision(piece):
                    game_over = True

        draw()
        draw_piece(piece)
        pygame.display.update()

    pygame.quit()


# 启动游戏
if __name__ == '__main__':
    main()
