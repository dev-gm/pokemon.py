import pygame
from pygame import Surface, Rect
from game import Map, Game
from boxes import Box, Building
from typing import Tuple, Union
from math import sqrt


class Point(tuple):
    def __init__(self, x: int, y: int):
        super().__init__([x, y])

    def closeness(self, pos: Tuple[int, int]):
        return abs(pos[0] - self[0]) + abs(pos[1] - self[1])


class Segment(tuple):
    def __init__(self, point_a: Point, point_b: Point):
        super().__init__([point_a, point_b])
        self.slope = Segment.get_slope(self[0], self[1])
        self.y_intercept = Segment.get_y_intercept(self[0], self.slope)
        self.axis = None
        for i in range(2):
            if point_a[i] == point_b[i]:
                self.axis = i


    def collided(self, player: Player):
        if not straight:
            return collided_diagonal
        new = player.rect.position[] + move[i]
        if new - radius[i] > self.rect.size[i] or new + radius[i] < 0:
            move[i] = 0


    def collided_diagonal(self, player: Player):
        pos = player.rect.position
        radius = player.radius
        for x in range(self[0][0], self[1][0]):
            y = (self.slope * x) + self.y_intercept
            slope = Segment.get_slope(pos, (x, y))
            if self.slope * slope != -1:
                continue
            length = Segment.get_diagonal((x - pos[0]), (y - pos[1]))
            if length <= radius:
                return (0, 0)
        return (0, 0)

    @staticmethod
    def get_slope(point_a: Union[Point, Tuple[int, int]], point_b: Union[Point, Tuple[int, int]]):
        return (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])

    @staticmethod
    def get_y_intercept(point: Point, slope: int):
        return point[1] - (slope * point[0])

    @staticmethod
    def get_diagonal(width: int, height: int):
        return sqrt(width ** 2 + height ** 2)


class Door(Segment):
    def __init__(self, point_a: Point, point_b: Point, dest: Map):
        super().__init__(point_a, point_b)
        self.dest = dest
