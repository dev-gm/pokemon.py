"""The module which holds the game class, the main
module which attaches the rest of the objects together"""

import sys
import os
import pygame
from pygame import Rect
from pygame.locals import (
    QUIT, KEYDOWN, KEYUP,
    K_UP, K_w, K_COMMA,
    K_LEFT, K_a,
    K_DOWN, K_s, K_o,
    K_RIGHT, K_d, K_e
)
from game.maps import Map, Player
from game.boundaries import Door
from game.boxes import Box, Building, WildArea
from game.parse.save import Save


class Game:
    """Controls the entire game, holds all maps and player, and game loop"""

    def __init__(self, save: Save = Save()):
        """Initialized pygame and parses json file -
        pass in save name (saves/{save}/)"""
        pygame.init()
        if not save:
            sys.exit()
        self.save = save
        os.chdir(self.save.save_folder)
        self.move = [0, 0]
        data = self.save.get_data()
        self.size = data.get("size")
        self.maps = []
        for raw_map in data.get("maps"): # Gets maps from raw maps
            sprites = []
            for raw_sprite in raw_map.get("sprites"): # Gets sprites for map from raw sprites
                try:
                    sprite = globals().get(raw_sprite.get("type"))(
                        Rect(raw_sprite.get("pos"), raw_sprite.get("size")),
                        pygame.image.load(os.path.join('.', "img", raw_sprite.get("image"))),
                        [Door(
                            tuple(door.get("pos")[0]),
                            tuple(door.get("pos")[1]),
                            door.get("dest")
                        ) for door in raw_sprite.get("doors")]
                    )
                except TypeError:
                    print(f"{raw_sprite.get('type')} sprite type does not exist")
                else:
                    sprites.append(sprite)
            self.maps.append(Map(
                pygame.image.load(os.path.join('.', "img", raw_map.get("image"))),
                Rect(raw_map.get("pos"), raw_map.get("size")),
                sprites,
                [Door(
                    tuple(door.get("pos")[0]),
                    tuple(door.get("pos")[1]),
                    door.get("dest")
                ) for door in raw_map.get("doors")],
                raw_map.get("caption")
            ))
        raw_player = data.get("player")
        self.speed = raw_player.get("speed")
        if not self.speed:
            self.speed = 25
        self.map = self.maps[raw_player.get("current").get("map")]
        self.player = Player(
            raw_player.get("name"),
            pygame.image.load(os.path.join('.', "img", raw_player.get("image"))),
            Rect(raw_player.get("current").get("pos"), raw_player.get("size"))
        )
        self.reset_next_turn = False

    def start(self):
        """Game loop detects the button clicks, changes
        move var, and updates & draws all sprites on map"""
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.map.caption)
        while True:
            self.map.draw(self.screen)
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                self.get_movement(event)
            self.update(self.map, self.player)
            pygame.display.update()

    def get_movement(self, event):
        """Detects keypresses and changes game.move to match it"""
        self.move = [0, 0] if self.reset_next_turn else self.move
        speed = self.speed if event.type == KEYDOWN else 0
        if event.type in (KEYDOWN, KEYUP): # a key was pressed
            if event.key in (K_UP, K_w, K_COMMA): # up
                self.move[1] = -speed
            elif event.key in (K_DOWN, K_s, K_o): # down
                self.move[1] = speed
            if event.key in (K_LEFT, K_a): # left
                self.move[0] = -speed
            elif event.key in (K_RIGHT, K_d, K_e): # right
                self.move[0] = speed
            self.reset_next_turn = False

    def update(self, *objects):
        """Updates and draws the map or player"""
        for obj in objects:
            obj.update(self)
            obj.draw(self.screen)

    def change_map(self, new_map: Map):
        """Changes map to a new map"""
        self.map = new_map
        self.player.rect.pos = self.map.entrance

    def save_game(self):
        """Saves the game to the json game info file"""
        self.save.update_file()