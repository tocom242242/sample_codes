import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

WIDTH, HEIGHT = 40, 40

WINDOW_SIZE = [450, 450]

MARGIN = 5

# 行動の集合
ACTIONS = {
    "UP": 0,
    "DOWN": 1,
    "LEFT": 2,
    "RIGHT": 3,
    "STAY": 4}

def is_in_grid(x, y):
    """
        x, yがグリッドワールド内かの確認
    """
    if len(grid) > y >= 0:
        if len(grid[0]) > x  >= 0:
            return True
    return False


def update_agent_pos(x, y):
    """
        エージェントの位置の更新 
    """

    while True:
        to_y, to_x = y, x
        action = np.random.randint(6)
        if action == ACTIONS["UP"]:
            to_y += -1
        elif action == ACTIONS["DOWN"]:
            to_y += 1
        elif action == ACTIONS["LEFT"]:
            to_x += -1
        elif action == ACTIONS["RIGHT"]:
            to_x += 1

        if is_in_grid(to_y, to_x) is True:
            return to_x, to_y


def draw_grid_world():
    """
        grid world自体の再描画
    """
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            pygame.draw.rect(screen,
                             color,
                             [(MARGIN + WIDTH) * column + MARGIN,
                              (MARGIN + HEIGHT) * row + MARGIN,
                              WIDTH,
                              HEIGHT])


if __name__ == '__main__':

    # pygameの初期化
    pygame.init()

    # grid情報の初期化
    grid = []
    for row in range(10):
        grid.append([])
        for column in range(10):
            grid[row].append(0)

    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption("Grid World")

    clock = pygame.time.Clock()

    # エージェントの初期位置
    x, y = 1, 5
    grid[y][x] = 1

    while True:
        screen.fill(BLACK)

        # grid worldの描画
        draw_grid_world()

        clock.tick(1)

        # 再描画
        pygame.display.flip()


        # エージェントの位置の更新
        to_x, to_y = update_agent_pos(x, y)

        grid[y][x] = 0
        grid[to_y][to_x] = 1
        x, y = to_x, to_y

    pygame.quit()
