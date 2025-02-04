import pygame

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
    with open(filename, "r") as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, "."), level_map))


def terminate():
    pygame.quit()
    exit()


tile_images = {
    "N": pygame.transform.scale(load_image("data/Water.png"), (TILE_SIZE, TILE_SIZE)),
    "S": pygame.transform.scale(load_image("data/Sand.png"), (TILE_SIZE, TILE_SIZE)),
    "R": pygame.transform.scale(load_image("data/Rocks.png"), (TILE_SIZE, TILE_SIZE)),
    "K": pygame.transform.scale(load_image("data/box.png"), (TILE_SIZE, TILE_SIZE)),
    "W": pygame.transform.scale(load_image("data/grass.png"), (TILE_SIZE, TILE_SIZE)),
    "P": pygame.transform.scale(load_image("data/grass.png"), (TILE_SIZE, TILE_SIZE)),
}

player_image = load_image("data/Hero/Idle/0.png")


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
        if tile_type in ["N", "R", "K"]:
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

            level_width = len(load_level("map.txt")[0]) * TILE_SIZE
            level_height = len(load_level("map.txt")) * TILE_SIZE

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
                self.check_attack()  # Überprüfen, ob ein Gegner in der Nähe ist

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

    def check_attack(self):
        for enemy in enemy_group:
            if self.rect.colliderect(enemy.rect.inflate(TILE_SIZE, TILE_SIZE)):
                enemy.take_damage(1)

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
            self.die()
        self.image = self.dead_images[int(self.dead_animation_frame)]

    def take_damage(self, amount):
        if not self.is_hurt and not self.is_dead:
            self.health = max(0, self.health - amount)
            self.is_hurt = True
            self.hurt_frame = 0
            if self.health == 0:
                self.is_dead = True
                self.dead_animation_frame = 0

    def die(self):
        print("Spieler gestorben!")
        pygame.time.wait(2000)
        game_over_screen()


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.idle_images = [load_image(f"data/Enemy_1/Idle/{i}.png") for i in range(6)]
        self.run_images = [load_image(f"data/Enemy_1/Run/{i}.png") for i in range(10)]
        self.attack_images = [
            load_image(f"data/Enemy_1/Attack/{i}.png") for i in range(4)
        ]
        self.hurt_images = [load_image(f"data/Enemy_1/Hurt/{i}.png") for i in range(3)]
        self.dead_images = [load_image(f"data/Enemy_1/Dead/{i}.png") for i in range(4)]
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
        self.health = 3
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_speed = 0.25
        self.attack_cooldown = 0
        self.is_attacking = False
        self.is_dead = False
        self.facing_right = True
        self.death_timer = 0  # Timer für das Entfernen des Gegners nach dem Tod

    def update(self, player):
        if self.is_dead:
            self.death_timer += 1 / FPS  # Timer aktualisieren
            if self.death_timer >= 2:  # Nach 2 Sekunden entfernen
                self.kill()
            return

        distance_to_player = (
            (self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2
        ) ** 0.5

        if distance_to_player < 5 * TILE_SIZE:
            self.move_towards_player(player)
            if distance_to_player < TILE_SIZE:
                self.attack(player)
        else:
            self.idle()

        self.animate()

    def move_towards_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += (dx / distance) * SPEED * TILE_SIZE
        self.rect.y += (dy / distance) * SPEED * TILE_SIZE
        self.current_animation = "run"

        if dx > 0:
            self.facing_right = True
        else:
            self.facing_right = False

    def idle(self):
        self.current_animation = "idle"

    def attack(self, player):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 3 * FPS
            self.current_animation = "attack"
            self.animation_frame = 0
            if self.rect.colliderect(player.rect.inflate(TILE_SIZE, TILE_SIZE)):
                player.take_damage(2)
        else:
            self.attack_cooldown -= 1

    def animate(self):
        if self.is_dead:
            self.animation_frame = (
                self.animation_frame + self.animation_speed - 0.2
            ) % len(self.dead_images)

            self.image = self.dead_images[int(self.animation_frame)]
            return

        if self.current_animation == "idle":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.idle_images
            )
            self.image = self.idle_images[int(self.animation_frame)]
        elif self.current_animation == "run":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.run_images
            )
            self.image = self.run_images[int(self.animation_frame)]
        elif self.current_animation == "attack":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.attack_images
            )
            self.image = self.attack_images[int(self.animation_frame)]
            if self.animation_frame >= len(self.attack_images) - 1:
                self.is_attacking = False
                self.current_animation = "idle"

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.current_animation = "dead"
        self.animation_frame = 0
        self.animate()


class Enemy2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_group, all_sprites)
        self.idle_images = [load_image(f"data/Enemy_2/Idle/{i}.png") for i in range(6)]
        self.run_images = [load_image(f"data/Enemy_2/Run/{i}.png") for i in range(8)]
        self.attack_images = [
            load_image(f"data/Enemy_2/Attack/{i}.png") for i in range(5)
        ]
        self.hurt_images = [load_image(f"data/Enemy_2/Hurt/{i}.png") for i in range(2)]
        self.dead_images = [load_image(f"data/Enemy_2/Dead/{i}.png") for i in range(4)]
        self.image = self.idle_images[0]
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)
        self.health = 2
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_speed = 0.25
        self.attack_cooldown = 0
        self.is_attacking = False
        self.is_dead = False
        self.facing_right = True
        self.death_timer = 0  # Timer für das Entfernen des Gegners nach dem Tod

    def update(self, player):
        if self.is_dead:
            self.death_timer += 1 / FPS  # Timer aktualisieren
            if self.death_timer >= 2:  # Nach 2 Sekunden entfernen
                self.kill()
            return

        distance_to_player = (
            (self.rect.x - player.rect.x) ** 2 + (self.rect.y - player.rect.y) ** 2
        ) ** 0.5

        if distance_to_player < 5 * TILE_SIZE:
            self.move_towards_player(player)
            if distance_to_player < TILE_SIZE:
                self.attack(player)
        else:
            self.idle()

        self.animate()

    def move_towards_player(self, player):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = max(1, (dx**2 + dy**2) ** 0.5)
        self.rect.x += (dx / distance) * SPEED * TILE_SIZE
        self.rect.y += (dy / distance) * SPEED * TILE_SIZE
        self.current_animation = "run"

        if dx > 0:
            self.facing_right = True
        else:
            self.facing_right = False

    def idle(self):
        self.current_animation = "idle"

    def attack(self, player):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 4 * FPS
            self.current_animation = "attack"
            self.animation_frame = 0
            if self.rect.colliderect(player.rect.inflate(TILE_SIZE, TILE_SIZE)):
                player.take_damage(3)
        else:
            self.attack_cooldown -= 1

    def animate(self):
        if self.is_dead:
            self.animation_frame = min(
                self.animation_frame + self.animation_speed, len(self.dead_images) - 1
            )
            self.image = self.dead_images[int(self.animation_frame)]
            return

        if self.current_animation == "idle":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.idle_images
            )
            self.image = self.idle_images[int(self.animation_frame)]

        elif self.current_animation == "run":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.run_images
            )
            self.image = self.run_images[int(self.animation_frame)]
        elif self.current_animation == "attack":
            self.animation_frame = (self.animation_frame + self.animation_speed) % len(
                self.attack_images
            )
            self.image = self.attack_images[int(self.animation_frame)]
            if self.animation_frame >= len(self.attack_images) - 1:
                self.is_attacking = False
                self.current_animation = "idle"

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.current_animation = "dead"
        self.animation_frame = 0
        self.animate()


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = pygame.transform.scale(load_image("data/Key.png"), (30, 30))
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(door_group, all_sprites)
        self.image = pygame.transform.scale(
            load_image("data/Door.png"), (TILE_SIZE, TILE_SIZE)
        )
        self.rect = self.image.get_rect().move(TILE_SIZE * pos_x, TILE_SIZE * pos_y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()


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
            reset_game()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def reset_game():
    global all_sprites, tiles_group, wall_group, player_group, enemy_group, key_group, door_group

    # Alle Gruppen leeren
    all_sprites.empty()
    tiles_group.empty()
    wall_group.empty()
    player_group.empty()
    enemy_group.empty()
    key_group.empty()
    door_group.empty()

    # Spiel neu starten
    game_loop()


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == "#":
                Tile("W", x, y)
                new_player = Player(x, y)
            elif level[y][x] == "P":
                Tile("W", x, y)
                Key(x + 0.4, y + 0.4)
            elif level[y][x] == "O":
                Tile("W", x, y)
                Door(x, y)
            elif level[y][x] in tile_images:
                Tile(level[y][x], x, y)
            elif level[y][x] == "E":
                Tile("W", x, y)
                Enemy1(x, y)
            elif level[y][x] == "D":
                Tile("W", x, y)
                Enemy2(x, y)

    if new_player is None:
        print("Error: No player start point ('#') found in level!")
        terminate()

    return new_player


def game_loop():
    player = generate_level(load_level("map.txt"))
    camera = Camera()  # Kamera initialisieren
    running = True
    while running:
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

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
                player.take_damage(3)  # Testen des Schadenssystems
            else:
                player.update(0, 0, is_running, is_attacking)
        else:
            player.play_dead_animation()

        for enemy in enemy_group:
            enemy.update(player)

        for key in key_group:
            if player.rect.colliderect(key.rect):
                player.inventory["Key"] = 1
                key.kill()

        for door in door_group:
            if player.rect.colliderect(door.rect) and "Key" in player.inventory:
                print("Boss Level startet!")

        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        enemy_group.draw(screen)
        key_group.draw(screen)
        door_group.draw(screen)

        draw_hearts(screen, player)

        pygame.display.flip()
        clock.tick(FPS)


game_loop()
