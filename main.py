import pygame

WINDOW_WIDTH = 15 * 64
WINDOW_HEIGHT = 15 * 33
SQUARE_SIZE = 15
CAMERA_SPEED = 8  # Speed of the camera movement

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

    def draw(self, surface, offset_x, offset_y, zoom):
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
                    (
                        x * SQUARE_SIZE * zoom + offset_x,
                        y * SQUARE_SIZE * zoom + offset_y,
                        SQUARE_SIZE * zoom,
                        SQUARE_SIZE * zoom,
                    ),
                )


class Player:
    def __init__(self, start_x, start_y):
        self.x = start_x
        self.y = start_y

    def draw(self, surface):
        pygame.draw.circle(
            surface, (139, 69, 19), (int(self.x), int(self.y)), 25
        )  # Brown color for the player

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Остров Сокровищ")
clock = pygame.time.Clock()

map_instance = Map("Project/map.txt")
player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
offset_x, offset_y = 0, 0
zoom = 4

while True:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            player.move(0, -CAMERA_SPEED)
        if event.key == pygame.K_s:
            player.move(0, CAMERA_SPEED)
        if event.key == pygame.K_a:
            player.move(-CAMERA_SPEED, 0)
        if event.key == pygame.K_d:
            player.move(CAMERA_SPEED, 0)

    offset_x = WINDOW_WIDTH / 2 - player.x
    offset_y = WINDOW_HEIGHT / 2 - player.y

    screen.fill(BACKGROUND_COLOR)
    map_instance.draw(screen, offset_x, offset_y, zoom)
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
