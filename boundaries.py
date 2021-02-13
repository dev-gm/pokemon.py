"""The module which holds the boundary classes in the
program, like Segment and Door"""

from typing import Tuple


class SegmentNotStraightException(Exception):
    """Exception for when the points provided for a
    segment's creation are not aligned with each other"""
    def __init__(self, point_a: Tuple[int, int], point_b: Tuple[int, int]):
        super().__init__(f"""{point_a} is not on the same line as
                         {point_b}, while initializing Segment object.""")


class Segment:
    """Connects two points together, can be used for boundaries"""

    def __init__(self, point_a: Tuple[int, int], point_b: Tuple[int, int]):
        self.mid = None
        for i in range(2):
            if point_a[i] == point_b[i]:
                self.mid = i
        if self.mid is None:
            raise SegmentNotStraightException(point_a, point_b)
        self.points = (point_a, point_b)

    def get_mid(self):
        """Gets midpoint of segment (i.e. for (1, 3) and (5, 3) it would return 3)"""
        return self.points[self.mid]

# static functions to get slope, y-intercept, and diagonal,
# for before I decided to not have any diagonal lines in the program.
#    @staticmethod
#    def get_slope(point_a: Tuple[int, int], point_b: Tuple[int, int]):
#        return (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
#
#    @staticmethod
#    def get_y_intercept(point: Tuple[int, int], slope: int):
#        return point[1] - (slope * point[0])
#
#    @staticmethod
#    def get_diagonal(width: int, height: int):
#        return sqrt(width ** 2 + height ** 2)


class Door(Segment):
    """A segment that, when the player collides, instead of just
    blocking the movement, it moves the player to another map."""

    def __init__(self, point_a: Tuple[int, int], point_b: Tuple[int, int], dest_id: int):
        super().__init__(point_a, point_b)
        self.dest_id = dest_id

    def go_through(self, game):
        """Since the init function only takes in the destination index,
        this function gets the game object and returns the correct destination"""
        game.change_map(game.maps[self.dest_id])
