import pygame

WINDOW_WIDTH = 15 * 64
WINDOW_HEIGHT = 15 * 33
SQUARE_SIZE = 15

COLOR_N = (0, 0, 255)
COLOR_S = (255, 165, 0)
COLOR_W = (0, 100, 0)
COLOR_R = (128, 128, 128)
COLOR_HASH = (0, 0, 0)
COLOR_B = (0, 0, 0)
COLOR_G = (169, 169, 169)
COLOR_QUESTION = (0, 0, 139)
BACKGROUND_COLOR = (255, 255, 255)


class Map:
    def __init__(self, filename):
        self.grid = self.load_map(filename)

    def load_map(self, filename):
        with open(filename, "r") as f:
            return [line.strip() for line in f]

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                color = BACKGROUND_COLOR
                if char == "N":
                    color = COLOR_N
                elif char == "S":
                    color = COLOR_S
                elif char == "W":
                    color = COLOR_W
                elif char == "R":
                    color = COLOR_R
                elif char == "#":
                    color = COLOR_HASH
                elif char == "B":
                    color = COLOR_B
                elif char == "G":
                    color = COLOR_G
                elif char == "?":
                    color = COLOR_QUESTION

                pygame.draw.rect(
                    surface,
                    color,
                    (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                )


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Остров Сокровищ")
clock = pygame.time.Clock()

map_instance = Map("Project/map.txt")

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = event.pos
        grid_x = mouse_x // SQUARE_SIZE
        grid_y = mouse_y // SQUARE_SIZE

        if (
            grid_x >= 0
            and grid_x < len(map_instance.grid[0])
            and grid_y >= 0
            and grid_y < len(map_instance.grid)
        ):
            if map_instance.grid[grid_y][grid_x] == "#":
                map_instance = Map("Project/umap.txt")
            elif map_instance.grid[grid_y][grid_x] == "?":
                map_instance = Map("Project/map.txt")
                
                
    screen.fill(BACKGROUND_COLOR)
    map_instance.draw(screen)
    pygame.display.flip()
    clock.tick(60)
