import pygame
import random

# Определение констант
WIDTH = 800
HEIGHT = 600
FPS = 30
CELL_SIZE = 40
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
BOMB_COUNT = 10

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Сапер")
clock = pygame.time.Clock()


def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))


def generate_bombs():
    bombs = []
    while len(bombs) < BOMB_COUNT:
        bomb = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if bomb not in bombs:
            bombs.append(bomb)
    return bombs


def count_neighbor_bombs(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < GRID_WIDTH and 0 <= y + j < GRID_HEIGHT:
                if grid[x + i][y + j] == "bomb":
                    count += 1
    return count


def reveal_cells(grid, revealed_grid, x, y):
    if grid[x][y] == "bomb":
        return
    if revealed_grid[x][y]:
        return
    revealed_grid[x][y] = True
    if grid[x][y] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= x + i < GRID_WIDTH and 0 <= y + j < GRID_HEIGHT and not revealed_grid[x + i][y + j]:
                    reveal_cells(grid, revealed_grid, x + i, y + j)


def toggle_marker(grid, x, y):
    if grid[x][y] == "marker":
        grid[x][y] = 0
    elif grid[x][y] == 0:
        grid[x][y] = "marker"


def check_win(revealed_grid, grid):
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if not revealed_grid[x][y] and grid[x][y] != "bomb":
                return False
    return True


def main():
    grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    revealed_grid = [[False] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    bombs = generate_bombs()
    for bomb in bombs:
        grid[bomb[0]][bomb[1]] = "bomb"
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y] != "bomb":
                grid[x][y] = count_neighbor_bombs(grid, x, y)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // CELL_SIZE
                    cell_y = pos[1] // CELL_SIZE
                    if not revealed_grid[cell_x][cell_y]:
                        reveal_cells(grid, revealed_grid, cell_x, cell_y)
                elif event.button == 3:
                    pos = pygame.mouse.get_pos()
                    cell_x = pos[0] // CELL_SIZE
                    cell_y = pos[1] // CELL_SIZE
                    toggle_marker(grid, cell_x, cell_y)

        screen.fill(BLACK)
        draw_grid()

        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                if revealed_grid[x][y]:
                    if grid[x][y] == "bomb":
                        pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    else:
                        pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                        if grid[x][y] > 0:
                            font = pygame.font.Font(None, 24)
                            text = font.render(str(grid[x][y]), True, BLACK)
                            text_rect = text.get_rect(center=(x * CELL_SIZE + CELL_SIZE // 2,
                                                               y * CELL_SIZE + CELL_SIZE // 2))
                            screen.blit(text, text_rect)
                elif grid[x][y] == "marker":
                    pygame.draw.rect(screen, RED, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if check_win(revealed_grid, grid):
            font = pygame.font.Font(None, 36)
            text = font.render("You Win!", True, WHITE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
