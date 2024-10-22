import pygame
import random
import sys

# Cấu hình trò chơi
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10  # Số hàng và cột
CELL_SIZE = WIDTH // GRID_SIZE
MINES_COUNT = 15

# Màu sắc
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (211, 211, 211)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont("Arial", 24)

def create_grid():
    """Tạo bảng mìn và các giá trị."""
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines = set()
    while len(mines) < MINES_COUNT:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        mines.add((x, y))
        grid[x][y] = -1  # Đặt mìn

    for x, y in mines:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] != -1:
                    grid[nx][ny] += 1
    return grid

def reset_game():
    """Đặt lại trạng thái trò chơi."""
    global grid, revealed, flags, game_over, remaining_mines
    grid = create_grid()
    revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    flags = set()
    remaining_mines = MINES_COUNT
    game_over = False

reset_game()  # Khởi tạo trò chơi

def draw_grid():
    """Vẽ bảng trò chơi."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

            if revealed[x][y]:
                if grid[x][y] == -1:
                    pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 3)
                elif grid[x][y] > 0:
                    text = font.render(str(grid[x][y]), True, BLUE)
                    screen.blit(text, text.get_rect(center=rect.center))
            elif (x, y) in flags:
                pygame.draw.circle(screen, GREEN, rect.center, CELL_SIZE // 4)

def reveal_cell(x, y):
    """Mở ô và lan ra các ô lân cận nếu giá trị là 0."""
    if revealed[x][y] or (x, y) in flags:
        return
    revealed[x][y] = True
    if grid[x][y] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    reveal_cell(nx, ny)

def reveal_all_mines():
    """Hoạt ảnh mở tất cả mìn khi thua."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] == -1:
                revealed[x][y] = True
                draw_grid()
                pygame.display.flip()
                pygame.time.delay(100)

def check_win():
    """Kiểm tra người chơi có thắng không."""
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] != -1 and not revealed[x][y]:
                return False
    return True

def display_message(text):
    """Hiển thị thông báo và nút chơi lại."""
    message = font.render(text, True, BLACK)
    rect = message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    screen.blit(message, rect)

    # Vẽ nút chơi lại
    button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2, 100, 40)
    pygame.draw.rect(screen, LIGHT_GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)

    button_text = font.render("Chơi lại", True, BLACK)
    screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    pygame.display.flip()
    return button_rect

def draw_remaining_mines():
    """Hiển thị số mìn còn lại."""
    text = font.render(f"Mìn còn lại: {remaining_mines}", True, BLACK)
    screen.blit(text, (10, 10))

def main():
    global game_over, remaining_mines
    while True:
        screen.fill(WHITE)
        draw_grid()
        draw_remaining_mines()

        if game_over:
            button_rect = display_message("Game Over! Bạn đã thua." if not check_win() else "Chúc mừng! Bạn đã thắng.")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    # Kiểm tra nếu nhấp vào nút "Chơi lại"
                    if button_rect.collidepoint(event.pos):
                        reset_game()
                else:
                    x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                    if event.button == 1:  # Nhấp chuột trái
                        if (x, y) not in flags:
                            if grid[x][y] == -1:
                                reveal_all_mines()
                                game_over = True
                            else:
                                reveal_cell(x, y)
                                if check_win():
                                    game_over = True
                    elif event.button == 3:  # Nhấp chuột phải
                        if (x, y) in flags:
                            flags.remove((x, y))
                            remaining_mines += 1
                        elif remaining_mines > 0:
                            flags.add((x, y))
                            remaining_mines -= 1

        pygame.display.flip()

if __name__ == "__main__":
    main()
