import pygame
from enum import IntEnum

from .actor import Actor

ROW: int = 0
COLUMN: int = 1

class Tile(Actor):
    """
    Tiles to place onto board, holding colours and value.
    Tiles are Actors, therefore they are Actors and Renderable (Inheritance)
    Tiles override draw and update (Polymorphism)
    """
    def __init__(self, consts, pos: pygame.math.Vector2, value: int = 0) -> None:
        super().__init__()
        self._pos = pos
        self._consts = consts
        self._value = value
        self._font = pygame.font.SysFont(consts["font"], consts["font_size"], bold=True)
        self._combined = False
    
    # Example of polymorphism, overwrites the Actor class update
    def update(self, scene: "scene.Scene", dT) -> None:
        self._combined = False
    
    # Example of polymorphism, overwrites the Actor class draw, Actor inherites from Renderable class
    def draw(self, screen: pygame.surface.Surface) -> None:
        colour = tuple(self._consts["colour"][str(self._value)])
        box = self._consts["size"] // 4
        padding = self._consts["padding"]
        pygame.draw.rect(screen, colour, (self._pos[COLUMN] * box + padding,
                                              self._pos[ROW] * box + padding,
                                              box - 2 * padding,
                                              box - 2 * padding), 0)
        if self._value != 0:
                if self._value in (2, 4):
                    text_colour = tuple(self._consts["colour"]["dark"])
                else:
                    text_colour = tuple(self._consts["colour"]["light"])
                # display the number at the centre of the tile
                screen.blit(self._font.render("{:>4}".format(
                    self._value), 1, text_colour),
                    # 2.5 and 7 were obtained by trial and error
                    (self._pos[COLUMN] * box + 2.5 * padding, self._pos[ROW] * box + 7 * padding))
    
    def value(self) -> int:
        """Returns current value of tile"""
        return self._value
    
    def set_value(self, value) -> None:
        """Set current value of tile"""
        self._value = value
    
    def can_combine(self, other: "Tile") -> bool:
        """Returns true if can combine with given tile (has the same value), false otherwise"""
        return self == other and not self._combined and not other._combined

    def combine(self) -> int:
        """Doubles value and returns it"""
        self._value *= 2
        self._combined = True
        return self._value
    
    def is_zero(self) -> bool:
        """Returns true if value is 0, false otherwise"""
        return self._value == 0
    
    def reset_value(self) -> int:
        """Resets the value to 0, returns it"""
        self._value = 0
        return self._value
    
    def __str__(self):
        return f"{self._value}"

    def __eq__(self, other: "Tile") -> bool:
        return self._value == other._value
    
    def __ne__(self, other: "Tile") -> bool:
        return self._value != other._value
    
    def __lt__(self, other: "Tile") -> bool:
        return self._value < other._value
    
    def __gt__(self, other: "Tile") -> bool:
        return  self._value > other._value
    
    def __ge__(self, other: "Tile") -> bool:
        return self._value >= other._value
    
    def __le__(self, other: "Tile") -> bool:
        return self._value <= other._value
    
from . import scene
