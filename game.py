import pygame
import json
import sys
import os
from pygame import Rect, Surface, Color
from pygame.sprite import Sprite, Group
from boxes import Box, Building
from boundaries import Door
from typing import List, Tuple


class Player(Sprite):
    """The player class, holds player sprite, pos, and size"""

    def __init__(self, name: str, color: Color, rect: Rect = Rect((0, 0), (50, 50))):
        self.name = name
        self.image = Surface(rect.size)
        self.rect = rect
        pygame.draw.ellipse(self.image, color, self.rect)
        self.radius = self.rect.size
        
    def get_pos(self):
        """Returns position of the player"""
        return (self.rect.x, self.rect.y)

    def draw(self, screen: Surface):
        """Draws player to screen"""
        screen.blit(self.image, self.get_pos())

    def update(self, game):
        """Moves the player rect based on collision detection"""
        self.rect.move_ip(game.move[1], game.move[0])


class Map(Group):
    """The map class, holds all of the sprites in the map and its own background"""
    
    def __init__(self, image: Surface, rect: Rect, sprites: List[Sprite], doors: List[Door]):
        self.rect = rect
        self.image = pygame.transform.scale(image, self.rect.size)
        super().__init__(sprites)
        self.doors = doors
        if self.doors:
            self.entrance = self.doors[0]
        else:
            self.entrance = (0, 0)
        self.points = []
        self.boundaries = Building.get_segments(Box.get_points(self.rect))
        for sprite in sprites:
            self.points.extend(sprite.points)
            if sprite is Building:
                self.doors.extend(sprite.doors)
                self.boundaries.extend(sprite.boundaries)

    def draw(self, screen: Surface):
        """Draws background and sprites to screen"""
        screen.blit(self.image, self.rect)
        super().__init__()

    def update(self, game):
        """Updates sprites boundaries and map
        boundaries but passes in game as well"""
        player = game.player
        radius = player.radius
        for i in range(2):
            new = player.get_pos()[i] + game.move[i]
            if new - radius[i] > self.rect.size[i] or new + radius[i] < 0:
                game.move[i-1] = 0
        for sprite in self.sprites():
            sprite.update(game)


class Game(object):
    """Controls the entire game, holds all maps and player, and game loop"""
    
    def __init__(self, save: str = json.load(open("save.json", 'r+').read()).get("save")):
        """Initialized pygame and parses json file"""
        pygame.init()
        self.map = None
        if not save:
            sys.exit()
        self.save = save
        self.path = os.path.join('./', "saves/", self.save)
        os.chdir(self.path)
        with open("data.json", 'r+') as file:
            self.parse(json.load(file))

    def start(self) -> int:
        """
        Game loop detects the button clicks, changes move var,
        and updates & draws all sprites on map
        """
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.move = [0, 0]
        while True:
            self.map.draw(self.screen)
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    i, movement = self.get_movement(event)
                    if i is not None:
                        self.move[i] = movement
                elif event.type == pygame.KEYUP:
                    i, movement = self.get_movement(event)
                    if i is not None:
                        self.move[i] = 0
            self.update(self.map)
            self.update(self.player)
            print("MOVE:", self.move)
            print("POS:", self.player.get_pos())
            pygame.display.update()
        return 0

    def get_movement(self, event):
        """Gets movement index (0 or 1) and movement val (50/-50),
        so if it returned (0, 50), then the game.move var would be
        turned into (x, 50). If None returns, then it stays the same"""
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            key = event.key
            if key == pygame.K_w or key == pygame.K_COMMA:
                return 0, -50
            elif key == pygame.K_a:
                return 1, -50
            elif key == pygame.K_s or key == pygame.K_o:
                return 0, 50
            elif key == pygame.K_d or key == pygame.K_e:
                return 1, 50
        return None, None

    def update(self, obj):
        """Updates and draws a map or player"""
        obj.update(self)
        obj.draw(self.screen)
        
    def change_map(self, new_map: Map):
        """Changes map another map"""
        self.map = new_map
        self.player.rect.pos = self.map.entrance

    def parse(self, data: dict):
        """
        Parses data from json, including
        size, caption, maps, and player
        """
        self.size = data.get("size")
        self.caption = data.get("caption")
        self.maps = []
        for raw_map in data.get("maps"):
            sprites = []
            global SpriteType
            for raw_sprite in raw_map.get("sprites"):
                exec(
                    f'global SpriteType\nSpriteType = {raw_sprite.get("type")}')
                SpriteType(
                    Rect(raw_sprite.get("pos"), raw_sprite.get("size")),
                    pygame.image.load(raw_sprite.get("image")),
                    [Door(
                        tuple(door.get("pos")[0]),
                        tuple(door.get("pos")[1]),
                        door.get("dest")
                    ) for door in raw_sprite.get("doors")]
                )
            self.maps.append(Map(
                pygame.image.load(raw_map.get("image")),
                Rect(raw_map.get("pos"), raw_map.get("size")),
                sprites,
                [Door(
                    tuple(door.get("pos")[0]),
                    tuple(door.get("pos")[1]),
                    door.get("dest")
                ) for door in raw_map.get("doors")]
            ))
        raw_player = data.get("player")
        self.map = self.maps[raw_player.get("current").get("map")]
        self.player = Player(
            raw_player.get("name"),
            Color(tuple(raw_player.get("color"))),
            Rect(raw_player.get("current").get("pos"), raw_player.get("size"))
        )
