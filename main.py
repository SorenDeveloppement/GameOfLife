import time
import pygame
import numpy as np
import random

# Colors
BACKGROUND = (10, 10, 10)
WHITE_SMOKE = (200, 200, 200)
WHITE = (255, 255, 255)
WILL_DIE = (100, 100, 100)

# Game variables
SIZE = 20
T = 0.001
SHOW_WILL_DIE = False

# Pygame variables
WIDTH = 1000
HEIGHT = 800


def update(screen, cells, size, progress: bool = False):
    u_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = BACKGROUND if cells[row, col] == 0 else WHITE

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if progress:
                    color = WILL_DIE if SHOW_WILL_DIE else BACKGROUND
            elif 2 <= alive <= 3:
                u_cells[row, col] = 1
                if progress:
                    color = WHITE

        else:
            if alive == 3:
                u_cells[row, col] = 1
                if progress:
                    color = WHITE

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return u_cells


def main(t=T):
    global SHOW_WILL_DIE

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    cells = np.zeros((int(HEIGHT / SIZE), int(WIDTH / SIZE)))

    screen.fill(BACKGROUND)
    update(screen, cells, SIZE)

    pygame.display.flip()
    pygame.display.update()

    run = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = not run
                    update(screen, cells, SIZE)
                    pygame.display.update()
                if event.key == pygame.K_UP:
                    if not t >= 1:
                        t += 0.05
                if event.key == pygame.K_DOWN:
                    if not t <= 0.001:
                        if not (t - 0.05) < 0.001:
                            t -= 0.05
                if event.key == pygame.K_t:
                    t = 0.001
                if event.key == pygame.K_r:
                    cells = np.zeros((int(HEIGHT / SIZE), int(WIDTH / SIZE)))
                if event.key == pygame.K_ASTERISK:
                    for i in range(1500):
                        y = random.randint(0, len(cells) - 1)
                        x = random.randint(0, len(cells[0]) - 1)

                        cells[y, x] = 1
                if event.key == pygame.K_d:
                    SHOW_WILL_DIE = not SHOW_WILL_DIE

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // SIZE, pos[0] // SIZE] = 1
                update(screen, cells, SIZE)
                pygame.display.update()
            if pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // SIZE, pos[0] // SIZE] = 0
                update(screen, cells, SIZE)
                pygame.display.update()

        screen.fill(BACKGROUND)

        if run:
            cells = update(screen, cells, SIZE, True)
            pygame.display.update()

        time.sleep(t)


if __name__ == '__main__':
    main()
