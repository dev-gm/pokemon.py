import pygame, json, sys
from pygame import Rect, Surface
from pygame.sprite import Sprite, Group
from boxes import Box, Building
from typing import List, Union, Tuple, Optional


class Map(Group):
    def __init__(self, image: Surface, rect: Rect, sprites: List[Sprite], doors: List[Door]):
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        super().__init__(sprites)
        self.outline = Building.get_segments(Box.get_points(self.rect))
        self.doors = doors
        self.points = []
        self.boundaries = []
        for sprite in sprites:
            self.points.extend(sprite.points)
                if sprite is Building:
                    self.doors.extend(sprite.doors)
                    self.boundaries.extend(sprite.boundaries)

    def detect_collision(self, move: Tuple[int, int], player: Player):
        radius = player.radius
        for i in range(2):
            new = player.rect.position[i] + move[i]
            if new - radius[i] > self.rect.size[i] or new + radius[i] < 0:
                move[i] = 0
        for boundary in self.boundaries:
            move = boundary.collide(move, player)

    def draw(self, screen: Surface):
        super().__init__(self.image)
        screen.blit(self.image, self.rect)

    def update(self, game: Optional[Game]):
        for sprite in self.sprites():
            sprite.update(game)


class Player(Sprite):
    def __init__(self, name: str, image: Surface = Surface(50, 50), rect: Rect = Rect((0, 0), (50, 50))):
        self.name = name
        self.image = image
        self.rect = rect

    def update(self, game: Game):
        move = game.map.detect_collision(Game.move, self)
        self.rect.move(move[0], move[1])


class Game(object):
    def __init__(self, size: Tuple[int, int] = (1920, 1080), path: Union[Path, str] = "./saves/untitled.json"):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.maps = []
        self.map = None
        self.path = path
        with open(self.path, 'r+') as file:
            self.parse(json.load(file))
        self.move = (0, 0)
        while True:
            self.map.draw(self.screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_COMMA:
                        self.move = (-50, 0)
                    elif event.key == pygame.K_a:
                        self.move = (0, -50)
                    elif event.key == pygame.K_s or event.key == pygame.K_o:
                        self.move = (50, 0)
                    elif event.key == pygame.K_d or event.key == pygame.K_e:
                        self.move = (0, 50)
                elif event.type == pygame.KEYUP:
                    self.move = (0, 0)
            self.map.update(self)
            pygame.display.update()

    def change_map(self, new_map: Map):
        if self.map:
            self.player.remove(self.map)
        self.map = new_map
        self.player.add(self.map)

    def parse(self, data: dict):
        self.maps = []
        for raw_map in data.get("maps"):
            sprites = []
            for raw_sprite in raw_map.get("sprites"):
                SpriteType: TypeAlias = raw_sprite.get("type")
                image = pygame.image.load(os.abspath(raw_sprite.get("image"))).convert_alpha()
                SpriteType(
                    Rect(raw_sprite.get("pos"), image.get_size()),
                    image,
                    [Door(pos[0], pos[1], dest_id) for dest_id, pos in raw_sprite.get("doors")]
                )
            self.maps.append(Map(
                pygame.image.load(raw_map.get("image")).convert_alpha(),
                Rect(raw_map.get("pos"), raw_map.get("size")),
                sprites,
                [Door(pos[0], pos[1], dest_id) for dist_id, pos in raw_map.get("doors")]
            ))
        raw_player = data.get("player")
        self.player = Player(
            raw_player.get("name"),
            pygame.image.load(os.abspath(raw_player.get("image"))).convert_alpha(),
            Rect(raw_player.get("current").get("pos"), raw_player.get(image.get_size()))
        )
        self.change_map(self.maps[raw_player.get("current").get("map")])
