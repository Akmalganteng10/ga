import pygame
import random

# Ukuran layar dan grid
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Warna-warna untuk blok Tetris
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Bentuk blok Tetris
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],  # T
    [[1, 1],
     [1, 1]],      # O
    [[0, 1, 1],
     [1, 1, 0]],  # S
    [[1, 1, 0],
     [0, 1, 1]],  # Z
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0],
     [1, 0, 0]],    # L
    [[0, 1, 1],
     [0, 0, 1]]    # J
]

SHAPES_COLORS = [CYAN, YELLOW, GREEN, RED, BLUE, ORANGE, PURPLE]


# Fungsi untuk menggambar grid
def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y))


# Fungsi untuk menggambar tetromino
def draw_tetromino(screen, shape, color, x, y):
    for i, row in enumerate(shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, (x + j * GRID_SIZE, y + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))


# Kelas untuk membuat objek game Tetris
class Tetris:
    def __init__(self):
        self.board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.game_over = False
        self.current_shape = None
        self.current_color = None
        self.x = GRID_WIDTH // 2 - 2
        self.y = 0
        self.new_tetromino()

    def new_tetromino(self):
        self.current_shape = random.choice(SHAPES)
        self.current_color = random.choice(SHAPES_COLORS)
        self.x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.current_shape = [list(row) for row in zip(*self.current_shape[::-1])]

    def valid_move(self, dx, dy, shape=None):
        shape = shape or self.current_shape
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dx
                    new_y = self.y + i + dy
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or self.board[new_y][new_x]:
                        return False
        return True

    def lock_tetromino(self):
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell:
                    self.board[self.y + i][self.x + j] = self.current_color
        self.clear_lines()
        self.new_tetromino()

    def clear_lines(self):
        full_lines = [i for i, row in enumerate(self.board) if all(cell != 0 for cell in row)]
        for i in full_lines:
            self.board.pop(i)
            self.board.insert(0, [0] * GRID_WIDTH)

    def move_left(self):
        if self.valid_move(-1, 0):
            self.x -= 1

    def move_right(self):
        if self.valid_move(1, 0):
            self.x += 1

    def move_down(self):
        if self.valid_move(0, 1):
            self.y += 1
        else:
            self.lock_tetromino()

    def drop(self):
        while self.valid_move(0, 1):
            self.y += 1
        self.lock_tetromino()

    def draw(self, screen):
        draw_grid(screen)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.board[y][x]:
                    pygame.draw.rect(screen, self.board[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        draw_tetromino(screen, self.current_shape, self.current_color, self.x * GRID_SIZE, self.y * GRID_SIZE)


# Main function untuk menjalankan game
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    game = Tetris()

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    game.drop()

        screen.fill((0, 0, 0))
        game.draw(screen)
        pygame.display.flip()
        clock.tick(10)  # Kecepatan game (frame per second)

    pygame.quit()


if __name__ == "__main__":
    main()