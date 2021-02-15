"""The module which holds the game class, the main
module which attaches the rest of the objects together"""

import json
import sys
import os
from typing import List
import pygame
from pygame import Rect
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_w, K_COMMA, K_a, K_s, K_o, K_d, K_e
from pokemon.game.map import Map, Player
from pokemon.game.boundaries import Door
from pokemon.db.parse import Save


class Game:
    """Controls the entire game, holds all maps and player, and game loop"""

    def __init__(self, save: Save = Save()):
        """Initialized pygame and parses json file -
        pass in save name (saves/{save}/)"""
        pygame.init()
        if not save:
            sys.exit()
        self.save = save
        self.parse()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.move = [0, 0]
        self.movement = 50

    def start(self) -> int:
        """Game loop detects the button clicks, changes
        move var, and updates & draws all sprites on map"""
        while True:
            self.map.draw(self.screen)
            for event in [pygame.event.wait()]+pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                i, movement = self.get_movement(event)
                if i is not None:
                    self.move[i] = movement
            self.update(self.map)
            self.update(self.player)
            pygame.display.update()
        return 0

    def get_movement(self, event):
        """Gets movement index (0 or 1) and movement val (50/-50),
        so if it returned (0, 50), then the game.move var would be
        turned into (x, 50). If None returns, then it stays the same"""
        i, movement = None, None
        possible_keys = (K_w, K_COMMA, K_a, K_d, K_e, K_s, K_o)
        if event.type in (KEYDOWN, KEYUP): # Check if event has key attribute
            movement = 0
            key = event.key
            if key in possible_keys: # Check if key is in possible keys
                if key in possible_keys[2:5]: # left or right
                    i = 0
                else: # top or bottom
                    i = 1
                if event.type == KEYDOWN:
                    if key in possible_keys[:3]: # forward or left (+)
                        movement = -self.movement
                    else: # backward or right (-)
                        movement = self.movement
        return i, movement

    def update(self, obj):
        """Updates and draws the map or player"""
        obj.update(self)
        obj.draw(self.screen)

    def change_map(self, new_map: Map):
        """Changes map another map"""
        self.map = new_map
        self.player.rect.pos = self.map.entrance

    def parse(self, data: dict):
        """Parses data from json, including
        size, caption, maps, and player"""
        self.size = data.get("size")
        self.caption = data.get("caption")
        self.maps = []
        print(os.listdir("./img"))
        for raw_map in data.get("maps"): # Gets maps from raw maps
            sprites = []
            for raw_sprite in raw_map.get("sprites"): # Gets sprites for map from raw sprites
                try:
                    globals().get(raw_sprite.get("type"))(
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
            self.maps.append(Map(
                pygame.image.load(os.path.join('.', "img", raw_map.get("image"))),
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
            pygame.image.load(os.path.join('.', "img", raw_player.get("image"))),
            Rect(raw_player.get("current").get("pos"), raw_player.get("size"))
        )
