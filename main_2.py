import pygame

TILE_SIZE = 15
FPS = 50
WIDTH = 41 * TILE_SIZE
HEIGHT = 41 * TILE_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        raise SystemExit(e)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def load_level(filename):
    filename = "maps/" + filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))

def terminate():
    pygame.quit()
    exit()

tile_images = {
    "rocks": pygame.transform.scale(load_image("data/Rock.png"), (TILE_SIZE, TILE_SIZE)),
    "water": pygame.transform.scale(load_image("data/Water.png"), (TILE_SIZE, TILE_SIZE)),
}
player_image = pygame.transform.scale(load_image("data/Ship.png"), (TILE_SIZE, TILE_SIZE))

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
        if tile_type == "rocks":
            rocks_group.add(self)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y -7)
    
    def update(self, dx, dy):
        new_x = self.rect.x + dx * TILE_SIZE
        new_y = self.rect.y + dy * TILE_SIZE

        # if 0 <= new_x < WIDTH - TILE_SIZE and 0 <= new_y < HEIGHT - TILE_SIZE:
        #     new_rect = pygame.Rect(new_x, new_y, TILE_SIZE, TILE_SIZE)

        if not any(tile.rect.colliderect(new_x, new_y, TILE_SIZE, TILE_SIZE) for tile in rocks_group):
            self.rect.x = new_x
            self.rect.y = new_y
        
        tile_x = new_x // TILE_SIZE
        tile_y = new_y // TILE_SIZE
        if 0 <= tile_y < len(level) and 0 <= tile_x < len(level[tile_y]):
                if level[tile_y][tile_x] == "*":
                    show_transition_image()
                    start_level_2()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
rocks_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "+":
                Tile("water", x, y)
            elif level[y][x] == "#":
                Tile("rocks", x, y)
            elif level[y][x] == "@":
                Tile("water", x, y)
                new_player = Player(x, y+0.5)
            elif level[y][x] == "*":
                Tile("water", x, y)
    return new_player, x, y


def show_transition_image():
    transition_image = pygame.transform.scale(
        load_image("data/Background/Island.png"), (800, 550)
    )
    screen.blit(transition_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)


def start_level_2():
    pygame.quit()
    import main_3
    
    main_3.main() 
    
def main():
    global player, level
    level = load_level("map1.txt")
    player, level_x, level_y = generate_level(level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player.update(0, -1)
                elif event.key == pygame.K_s:
                    player.update(0, 1)
                elif event.key == pygame.K_a:
                    player.update(-1, 0)
                elif event.key == pygame.K_d:
                    player.update(1, 0)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

main()