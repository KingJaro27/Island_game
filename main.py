import pygame
import random

FPS = 50
WIDTH = 850
HEIGHT = 550
TILE_SIZE = 80
SPEED = 0.05

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
    filename = filename
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def terminate():
    pygame.quit()
    exit()


def start_screen():
    bg_image = pygame.transform.scale(
        load_image(f"data/Background/{random.randint(1, 8)}.png"), (WIDTH, HEIGHT)
    )
    screen.blit(bg_image, (0, 0))

    start_n = load_image("data/Buttons/start0.png")
    start_h = load_image("data/Buttons/start1.png")
    options_button = load_image("data/Buttons/Options.png")

    start_n = pygame.transform.scale(start_n, (150, 60))
    start_h = pygame.transform.scale(start_h, (150, 60))
    options_button = pygame.transform.scale(options_button, (150, 60))

    start_rect = start_n.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    options_rect = options_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    screen.blit(start_n, start_rect)
    screen.blit(options_button, options_rect)

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if start_rect.collidepoint(mouse_x, mouse_y):
            screen.blit(start_h, start_rect)
        else:
            screen.blit(start_n, start_rect)

        if mouse_pressed[0] and start_rect.collidepoint(mouse_x, mouse_y):
            game_loop()

        if mouse_pressed[0] and options_rect.collidepoint(mouse_x, mouse_y):
            options_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


tile_images = {
    "house": pygame.transform.scale(load_image("data/box.png"), (TILE_SIZE, TILE_SIZE)),
    "way": pygame.transform.scale(load_image("data/Way.png"), (TILE_SIZE, TILE_SIZE)),
}
player_image = load_image("data/Hero/Idle/0.png")


def options_screen():
    bg_image = pygame.transform.scale(
        load_image(f"data/Background/9.png"), (WIDTH, HEIGHT)
    )
    screen.blit(bg_image, (0, 0))

    font = pygame.font.Font(None, 36)

    key_images = {
        "W": load_image("data/Buttons/W.png"),
        "A": load_image("data/Buttons/A.png"),
        "S": load_image("data/Buttons/S.png"),
        "D": load_image("data/Buttons/D.png"),
        "SHIFT": load_image("data/Buttons/SHIFT.png"),
        "ESC": load_image("data/Buttons/ESC.png"),
        "E": load_image("data/Buttons/E.png"),
        "LMB": pygame.transform.scale(load_image("data/Buttons/LMB.png"), (60, 60)),
    }

    key_descriptions = {
        "W": "Движение вверх",
        "A": "Движение влево",
        "S": "Движение вниз",
        "D": "Движение вправо",
        "SHIFT": "Бежать (удерживайте)",
        "ESC": "Закрыть",
        "E": "Взаимодействовать/Торговля",
        "LMB": "Атака",
    }

    key_positions = {
        "W": (500, 50 * 1),
        "A": (500, 50 * 2),
        "S": (500, 50 * 3),
        "D": (500, 50 * 4),
        "SHIFT": (500, 50 * 5),
        "ESC": (500, 50 * 6),
        "E": (500, 50 * 7),
        "LMB": (500 - 20, 50 * 8),
    }

    back_button = pygame.transform.scale(load_image("data/Buttons/Back.png"), (100, 50))
    back_rect = back_button.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))

    while True:
        screen.blit(bg_image, (0, 0))

        for key, pos in key_positions.items():
            screen.blit(key_images[key], pos)
            text = font.render(key_descriptions[key], True, (0, 0, 0))
            screen.blit(text, (pos[0] + 60, pos[1] + 10))

        screen.blit(back_button, back_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0] and back_rect.collidepoint(mouse_x, mouse_y):
            start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        if tile_type == "N":
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
            wall_group.add(self)
        else:
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
            if tile_type == "house":
                self.rect.width += 20
                self.rect.height += 55
                wall_group.add(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.idle_images = [load_image(f"data/Hero/Idle/{i}.png") for i in range(4)]
        self.walk_images = [load_image(f"data/Hero/Walk/{i}.png") for i in range(10)]
        self.run_images = [load_image(f"data/Hero/Run/{i}.png") for i in range(10)]
        self.attack_images = [load_image(f"data/Hero/Attack/{i}.png") for i in range(4)]
        self.hurt_images = [load_image(f"data/Hero/Hurt/{i}.png") for i in range(3)]
        self.dead_images = [load_image(f"data/Hero/Dead/{i}.png") for i in range(5)]
        self.rect = self.image.get_rect().move(
            TILE_SIZE * pos_x + 15, TILE_SIZE * pos_y + 5
        )
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_speed = 0.25
        self.attack_in_progress = False
        self.facing_right = True
        self.mouse_was_pressed = False
        self.can_move = True
        self.coins = 0
        self.inventory = {}
        self.health = 15
        self.is_hurt = False
        self.hurt_frame = 0
        self.hurt_duration = 0.5
        self.hurt_timer = 0
        self.is_dead = False
        self.dead_animation_frame = 0
        self.dead_animation_speed = 0.25

    def update(self, dx, dy, is_running, is_attacking):
        if self.is_dead:
            self.play_dead_animation()
            return

        if self.health <= 0 and not self.is_dead:
            self.is_dead = True
            self.dead_animation_frame = 0
            return
        if not self.can_move:
            return
        if self.is_dead:
            self.play_dead_animation()
            return

        if self.is_hurt:
            self.hurt_timer += 1 / FPS
            if self.hurt_timer >= self.hurt_duration:
                self.is_hurt = False
                self.hurt_timer = 0
            self.current_animation = "hurt"
        else:
            new_x = self.rect.x + dx * TILE_SIZE
            new_y = self.rect.y + dy * TILE_SIZE

            level_width = len(load_level("map1.txt")[0]) * TILE_SIZE
            level_height = len(load_level("map1.txt")) * TILE_SIZE

            if (
                0 <= new_x <= level_width - TILE_SIZE
                and 0 <= new_y <= level_height - TILE_SIZE
            ):
                if not any(
                    tile.rect.collidepoint(new_x + 70, new_y + 120)
                    for tile in wall_group
                ):
                    self.rect.x = new_x
                    self.rect.y = new_y

            if dx < 0:
                self.facing_right = False
            elif dx > 0:
                self.facing_right = True

            if (
                is_attacking
                and not self.mouse_was_pressed
                and not self.attack_in_progress
            ):
                self.current_animation = "attack"
                self.animation_frame = 0
                self.attack_in_progress = True

            self.mouse_was_pressed = is_attacking

            if self.attack_in_progress:
                self.current_animation = "attack"
            elif is_running:
                self.current_animation = "run"
            elif dx != 0 or dy != 0:
                self.current_animation = "walk"
            else:
                self.current_animation = "idle"

        self.animate()

    def animate(self):
        if self.current_animation == "idle":
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.idle_images):
                self.animation_frame = 0
            self.image = self.idle_images[int(self.animation_frame)]
        elif self.current_animation == "walk":
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.walk_images):
                self.animation_frame = 0
            self.image = self.walk_images[int(self.animation_frame)]
        elif self.current_animation == "run":
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.run_images):
                self.animation_frame = 0
            self.image = self.run_images[int(self.animation_frame)]
        elif self.current_animation == "attack":
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.attack_images):
                self.animation_frame = 0
                self.attack_in_progress = False
            self.image = self.attack_images[int(self.animation_frame)]
        elif self.current_animation == "hurt":
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.hurt_images):
                self.animation_frame = 0
            self.image = self.hurt_images[int(self.animation_frame)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def play_dead_animation(self):
        self.dead_animation_frame += self.dead_animation_speed
        if self.dead_animation_frame >= len(self.dead_images):
            self.dead_animation_frame = len(self.dead_images) - 1
            pygame.time.wait(2000)
            game_over_screen()
        self.image = self.dead_images[int(self.dead_animation_frame)]

    def take_damage(self, amount):
        if not self.is_hurt and not self.is_dead:
            self.health = max(0, self.health - amount)
            self.is_hurt = True
            self.hurt_frame = 0
            if self.health == 0:
                self.is_dead = True
                self.dead_animation_frame = 0


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(coin_group, all_sprites)
        self.animation_images = [load_image(f"data/Coin/{i}.png") for i in range(5)]
        self.animation_frame = 0
        self.animation_speed = 0.25
        self.image = self.animation_images[0]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)

    def animate(self):
        self.animation_frame = (self.animation_frame + self.animation_speed) % len(
            self.animation_images
        )
        self.image = self.animation_images[int(self.animation_frame)]

    def update(self):
        self.animate()


class Traider(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, trader_id):
        super().__init__(traider_group, all_sprites)
        self.trader_id = trader_id
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.scroll_y = 0
        self.load_animations()
        self.current_animation = "idle1"
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.last_animation_change = pygame.time.get_ticks()
        self.show_e_key = False
        self.in_dialog = False
        self.dialog_frame = 0
        self.image = self.idle1_images[0]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
        self.e_key_image = pygame.transform.scale(
            load_image("data/Buttons/E.png"), (30, 30)
        )
        self.esc_key_image = pygame.transform.scale(
            load_image("data/Buttons/ESC.png"), (30, 30)
        )
        if trader_id == 1:
            self.inventory = {
                "Erz": 5,
                "Meat": 3,
                "Stone": 10,
                "Metall": 2,
                "Rum": 1,
                "Rope": 4,
                "Wood": 6,
                "Rubin": 1,
                "Ship": 1,
            }
            self.prices = {
                "Erz": 2,
                "Meat": 3,
                "Stone": 1,
                "Metall": 5,
                "Rum": 10,
                "Rope": 2,
                "Wood": 3,
                "Rubin": 20,
                "Ship": 30,
            }
        elif trader_id == 2:
            self.inventory = {
                "Erz": 3,
                "Meat": 5,
                "Stone": 8,
                "Metall": 4,
                "Rum": 2,
                "Rope": 6,
                "Wood": 4,
                "Rubin": 0,
            }
            self.prices = {
                "Erz": 3,
                "Meat": 2,
                "Stone": 30,
                "Metall": 6,
                "Rum": 12,
                "Rope": 3,
                "Wood": 4,
                "Rubin": 0,
            }
        elif trader_id == 3:
            self.inventory = {
                "Erz": 4,
                "Meat": 2,
                "Stone": 12,
                "Metall": 3,
                "Rum": 0,
                "Rope": 5,
                "Wood": 7,
                "Rubin": 2,
            }
            self.prices = {
                "Erz": 4,
                "Meat": 4,
                "Stone": 1,
                "Metall": 7,
                "Rum": 0,
                "Rope": 4,
                "Wood": 5,
                "Rubin": 25,
            }

    def load_animations(self):
        if self.trader_id == 1:
            self.idle1_images = [
                load_image(f"data/Trader_1/Idle_1/{i}.png") for i in range(6)
            ]
            self.idle2_images = [
                load_image(f"data/Trader_1/Idle_2/{i}.png") for i in range(11)
            ]
            self.dialog_images = [
                load_image(f"data/Trader_1/Dialog/{i}.png") for i in range(10)
            ]
        elif self.trader_id == 2:
            self.idle1_images = [
                load_image(f"data/Trader_2/Idle_1/{i}.png") for i in range(14)
            ]
            self.idle2_images = [
                load_image(f"data/Trader_2/Idle_2/{i}.png") for i in range(10)
            ]
            self.dialog_images = [
                load_image(f"data/Trader_2/Dialog/{i}.png") for i in range(4)
            ]
        elif self.trader_id == 3:
            self.idle1_images = [
                load_image(f"data/Trader_3/Idle_1/{i}.png") for i in range(6)
            ]
            self.idle2_images = [
                load_image(f"data/Trader_3/Idle_2/{i}.png") for i in range(15)
            ]
            self.dialog_images = [
                load_image(f"data/Trader_3/Dialog/{i}.png") for i in range(6)
            ]

    def update(self, player):
        distance_to_player = (
            (self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2
        ) ** 0.5

        if self.in_dialog:
            self.current_animation = "dialog"
        elif distance_to_player > 3 * TILE_SIZE:
            self.current_animation = "idle1"
            self.show_e_key = False
        else:
            self.current_animation = "idle2"
            self.show_e_key = True

            current_time = pygame.time.get_ticks()
            if current_time - self.last_animation_change > 10000:
                self.animation_frame = 0
                self.last_animation_change = current_time

        self.animate()

    def animate(self):
        if self.current_animation == "idle1":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.idle1_images
            )
            self.image = self.idle1_images[int(self.animation_frame)]
        elif self.current_animation == "idle2":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.idle2_images
            )
            self.image = self.idle2_images[int(self.animation_frame)]
        elif self.current_animation == "dialog":
            if self.dialog_frame < len(self.dialog_images) - 1:
                self.dialog_frame += self.animation_speed
            self.image = self.dialog_images[int(self.dialog_frame)]

    def draw_e_key(self, screen):
        if self.show_e_key and not self.in_dialog:
            screen.blit(self.e_key_image, (self.rect.centerx - 15, self.rect.top))

    def draw_esc_key(self, screen):
        if self.in_dialog:
            screen.blit(self.esc_key_image, (self.rect.centerx - 25, self.rect.top))

    def start_dialog(self):
        if not self.in_dialog:
            self.in_dialog = True
            self.dialog_frame = 0

    def end_dialog(self):
        self.in_dialog = False
        self.current_animation = "idle2"
        self.scroll_y = 0


player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
traider_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()


def generate_level(level):
    new_player = None
    trader_count = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "H":
                Tile("house", x, y)
            elif level[y][x] == "R":
                Tile("way", x, y)
            elif level[y][x] == "T":
                Tile("way", x, y)
                trader_count += 1
                if trader_count == 1:
                    Traider(x - 0.3, y - 0.7, 1)
                elif trader_count == 2:
                    Traider(x - 0.3, y - 0.7, 2)
                elif trader_count == 3:
                    Traider(x - 0.3, y - 0.7, 3)
            elif level[y][x] == "#":
                Tile("way", x, y)
                new_player = Player(x - 0.3, y - 0.7)
            elif level[y][x] == "C":
                Tile("way", x, y)
                Coin(x + 0.4, y + 0.4)
            elif level[y][x] == "N":
                Tile("N", x, y)

    if new_player is None:
        print("Error: No player start point ('#') found in level!")
        terminate()

    return new_player


class Camera:
    def _init_(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


camera = Camera()


def draw_coin_counter(screen, player):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Монет: {player.coins}", True, (255, 255, 255))
    screen.blit(text, (WIDTH - 150, 10))


trade_images = {
    "Erz": load_image("data/Erz.png"),
    "Meat": load_image("data/Meat.png"),
    "Stone": load_image("data/Stone.png"),
    "Metall": load_image("data/Metall.png"),
    "Rum": load_image("data/Rum.png"),
    "Rope": load_image("data/Rope.png"),
    "Wood": load_image("data/Wood.png"),
    "Rubin": load_image("data/Rubin.png"),
    "Ship": pygame.transform.scale(load_image("data/Ship.png"), (50, 50)),
}

buy_button = pygame.transform.scale(load_image("data/Buttons/Buy.png"), (50, 50))
sell_button = pygame.transform.scale(load_image("data/Buttons/Sell.png"), (50, 50))


def draw_trade_menu(screen, trader, player):
    dark_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    dark_surface.fill((0, 0, 0, 128))
    screen.blit(dark_surface, (0, 0))

    item_x = WIDTH // 4
    item_y = HEIGHT // 4
    item_spacing = 70

    font = pygame.font.Font(None, 36)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                trader.scroll_y += 20
            elif event.button == 5:
                trader.scroll_y -= 20

    trader.scroll_y = max(
        -(len(trader.inventory) * item_spacing - HEIGHT // 2), min(trader.scroll_y, 0)
    )

    draw_scrollbar(screen, trader, len(trader.inventory), item_spacing)

    for i, (item, quantity) in enumerate(trader.inventory.items()):
        if quantity > 0:
            item_pos_y = item_y + i * item_spacing + trader.scroll_y

            if item_pos_y > HEIGHT // 4 - item_spacing and item_pos_y < HEIGHT:
                screen.blit(trade_images[item], (item_x, item_pos_y))
                price_text = font.render(
                    f"Цена: {trader.prices[item]}", True, (255, 255, 255)
                )
                quantity_text = font.render(f"Кол: {quantity}", True, (255, 255, 255))
                screen.blit(price_text, (item_x + 100, item_pos_y + 10))
                screen.blit(quantity_text, (item_x + 100, item_pos_y + 40))
                buy_rect = screen.blit(buy_button, (item_x + 250, item_pos_y + 10))
                sell_rect = screen.blit(sell_button, (item_x + 310, item_pos_y + 10))

                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if mouse_pressed[0] and buy_rect.collidepoint(mouse_pos):
                    if player.coins >= trader.prices[item]:
                        player.coins -= trader.prices[item]
                        player.inventory[item] = player.inventory.get(item, 0) + 1
                        trader.inventory[item] -= 1
                        pygame.time.wait(200)

                        if item == "Ship":
                            show_transition_image()
                            start_level_2()
                            return
                    else:
                        show_message(screen, "Недостаточно монет!")
                        return

                if mouse_pressed[0] and sell_rect.collidepoint(mouse_pos):
                    if player.inventory.get(item, 0) > 0:
                        player.coins += trader.prices[item]
                        player.inventory[item] -= 1
                        trader.inventory[item] += 1
                        pygame.time.wait(200)
                    else:
                        show_message(screen, "У вас нет этого предмета!")
                        return


def draw_scrollbar(screen, trader, total_items, item_spacing):
    scrollbar_width = 10
    scrollbar_x = WIDTH - 50
    scrollbar_height = HEIGHT // 2
    scrollbar_y = HEIGHT // 4

    pygame.draw.rect(
        screen,
        (100, 100, 100),
        (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height),
    )

    max_scroll = -(total_items * item_spacing - HEIGHT // 2)
    scroll_ratio = trader.scroll_y / max_scroll
    indicator_height = scrollbar_height * (HEIGHT // 2) / (total_items * item_spacing)
    indicator_y = scrollbar_y + scroll_ratio * (scrollbar_height - indicator_height)

    pygame.draw.rect(
        screen,
        (200, 200, 200),
        (scrollbar_x, indicator_y, scrollbar_width, indicator_height),
    )


def show_message(screen, message):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def draw_hearts(screen, player):
    heart_images = [
        pygame.transform.scale(load_image(f"data/Live/{i}.png"), (30, 30))
        for i in range(6)
    ]
    heart_width = heart_images[0].get_width()
    heart_height = heart_images[0].get_height()
    x, y = 10, 10

    for i in range(3):
        heart_state = min(5, max(0, 5 - (player.health - i * 5)))
        screen.blit(heart_images[heart_state], (x + i * (heart_width + 5), y))


def show_transition_image():
    transition_image = pygame.transform.scale(
        load_image("data/Background/Ship.png"), (WIDTH, HEIGHT)
    )
    screen.blit(transition_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(5000)


def start_level_2():
    pygame.quit()
    import main_2

    main_2.main()


def game_over_screen():
    bg_image = pygame.transform.scale(
        load_image("data/Background/Lose.png"), (WIDTH, HEIGHT)
    )
    screen.blit(bg_image, (0, 0))

    restart_button = pygame.transform.scale(
        load_image("data/Buttons/Restart.png"), (150, 60)
    )
    restart_rect = restart_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:
        screen.blit(bg_image, (0, 0))
        screen.blit(restart_button, restart_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0] and restart_rect.collidepoint(mouse_x, mouse_y):
            start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def game_loop():
    running = True
    while running:
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not player.is_dead:
                    for trader in traider_group:
                        distance_to_player = (
                            (trader.rect.x - player.rect.x) ** 2
                            + (trader.rect.y - player.rect.y) ** 2
                        ) ** 0.5
                        if distance_to_player < TILE_SIZE:
                            trader.start_dialog()
                            player.can_move = False
                elif event.key == pygame.K_ESCAPE and not player.is_dead:
                    for trader in traider_group:
                        if trader.in_dialog:
                            trader.end_dialog()
                            player.can_move = True

        if not player.is_dead:
            is_shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
            is_moving = (
                keys[pygame.K_w]
                or keys[pygame.K_a]
                or keys[pygame.K_s]
                or keys[pygame.K_d]
            )
            is_running = is_shift_pressed and is_moving
            is_attacking = mouse_pressed[0]

            current_speed = SPEED * 2 if is_running else SPEED

            if keys[pygame.K_w]:
                player.update(0, -current_speed, is_running, is_attacking)
            elif keys[pygame.K_s]:
                player.update(0, current_speed, is_running, is_attacking)
            elif keys[pygame.K_a]:
                player.update(-current_speed, 0, is_running, is_attacking)
            elif keys[pygame.K_d]:
                player.update(current_speed, 0, is_running, is_attacking)
            elif keys[pygame.K_h]:
                player.take_damage(3)
            else:
                player.update(0, 0, is_running, is_attacking)
        else:
            player.play_dead_animation()
        for trader in traider_group:
            trader.update(player)

        for coin in coin_group:
            coin.update()
            if player.rect.colliderect(coin.rect):
                player.coins += 1
                coin.kill()

        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        traider_group.draw(screen)
        coin_group.draw(screen)

        for trader in traider_group:
            trader.draw_e_key(screen)
            trader.draw_esc_key(screen)

        draw_coin_counter(screen, player)
        draw_hearts(screen, player)

        for trader in traider_group:
            if trader.in_dialog:
                draw_trade_menu(screen, trader, player)

        pygame.display.flip()
        clock.tick(FPS)


player = generate_level(load_level("map1.txt"))

start_screen()
