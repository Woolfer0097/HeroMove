import pygame
import sys
import os

WIDTH, HEIGHT = 550, 400
FPS = 50


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * pos[0] + 15, tile_height * pos[1] + 5)
        self.pos = (x, y)


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Перемещение героя",
                  "Ходите стрелками",
                  "Влево Вверх Вниз Вправо"]

    bg = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(bg, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
            pygame.display.flip()
            clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move_hero(hero, direction):
    x, y = hero.pos
    if direction == "down":
        if y < level_y and level[x][y + 1] == ".":
            hero.move(x, y + 1)
    elif direction == "up":
        if y > 0 and level[x][y - 1] == ".":
            hero.move(x, y - 1)
    elif direction == "left":
        if y > 0 and level[x - 1][y] == ".":
            hero.move(x - 1, y)
    elif direction == "right":
        if y < level_x and level[x + 1][y] == ".":
            hero.move(x + 1, y)


def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    move_hero(player, "down")
                elif event.key == pygame.K_UP:
                    move_hero(player, "up")
                elif event.key == pygame.K_LEFT:
                    move_hero(player, "left")
                elif event.key == pygame.K_RIGHT:
                    move_hero(player, "right")
        tiles_group.draw(screen)
        player_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color("black"))
    tile_images = {
        'wall': load_image('box.png'),
        'empty': load_image('grass.png')
    }
    player_image = load_image('mario.png')
    tile_width = tile_height = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    level = [i.replace("@", ".") for i in load_level('map.txt')]
    player, level_x, level_y = generate_level(load_level('map.txt'))
    clock = pygame.time.Clock()
    start_screen()
    game()
