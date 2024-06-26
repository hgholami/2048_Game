import pygame
import random
from enum import Enum

from .actor import Actor
from .tile import Tile

class State(Enum):
    """Game state: play, win, lose"""
    play = 0,
    win = 1,
    lose = 2

class Board(Actor):
    """Is an Actor (inheritance). Holds, moves, and spawns tiles. Can see state of the game."""
    def __init__(self, scene: "scene.Scene", consts) -> None:
        super().__init__()
        self._highest_val = 2
        self._score = 0
        self._board: list = [ [0]*4 for i in range(4)]
        
        # populate board with tiles
        for i in range(4):
            for j in range(4):
                tile = Tile(consts, [i, j]) 
                self._board[i][j] = tile
                scene.add_actor(tile)
        
        # Randomize 2 tiles with a value of 2 or 4
        firstTilePos: pygame.math.vector2 = [random.randrange(1, 4), random.randrange(1, 4)]
        firstTilePos2: pygame.math.vector2 = [random.randrange(1, 4), random.randrange(1, 4)]
        while(firstTilePos == firstTilePos2):
            firstTilePos2 = [random.randrange(0, 4), random.randrange(0, 4)]
        
        self._board[firstTilePos[0]][firstTilePos[1]].set_value(random.choice([2, 4]))
        self._board[firstTilePos2[0]][firstTilePos2[1]].set_value(random.choice([2, 4]))
        
        self._consts = consts
    
    # Example of polymorphism, overwrites the Actor class update
    def update(self, scene: "scene.Scene", dT) -> None:
        for row in self._board:
            for tile in row:
                if tile.value() > self._highest_val:
                    self._highest_val = tile.value()
    
    # Example of polymorphism, overwrites the Actor class draw, Actor inherites from Renderable class
    def draw(self, screen: pygame.surface.Surface) -> None:
        pass
    
    def check_state(self) -> State:
        """Checks whether the game is over and returns play, win, or lose."""
        if self._highest_val == 2048:
            return State.win
        
        for i in range(4):
            for j in range(4):
                # check if a merge is possible
                if j != 3 and self._board[i][j] == self._board[i][j+1] or \
                        i != 3 and self._board[i][j] == self._board[i + 1][j]:
                    return State.play

        # Flatten board to check if any spaces are left
        flat_board = [tile for row in self._board for tile in row]
        for tile in flat_board:
            if tile.is_zero():
                return State.lose

        return State.play
    
    def spawn_tile(self) -> bool:
        """Spawns a tile at a random empty spot with value 2 or 4"""
        flat_board = [tile for row in self._board for tile in row]
        empty_spots: list = []
        for tile in flat_board:
            if tile.is_zero():
                empty_spots.append(tile)
        if len(empty_spots) == 0:
            return False
        position: pygame.math.vector2 = random.randrange(0, len(empty_spots))
        empty_spots[position].set_value(random.choice([2, 4]))
        return True

    # Example of abstraction, hides implementation on how tiles move up
    # Starts from the second row from top
    # Then moves tiles as far up as possible, combining
    # If a tile has already combined, it won't combine again
    def move_up(self):
        """Moves tiles up"""
        for row in range (1, 4):
            for col in range(0, 4):
                currTile: Tile = self._board[row][col]
                if not currTile.is_zero():
                    for targetRow in reversed(range(0, row)):
                        targetTile: Tile = self._board[targetRow][col] 
                        if targetTile.is_zero():
                            targetTile.set_value(currTile.value())
                            currTile.reset_value()
                            currTile = targetTile
                        else:
                            if targetTile != currTile:
                                break
                            elif targetTile.can_combine(currTile):
                                self._score += targetTile.combine()
                                currTile.reset_value()
        self.spawn_tile()
    
    # Example of abstraction, hides implementation on how tiles move right
    # Starts from the second column from Right
    # Then moves tiles as far right as possible, combining where possible
    # If a tile has already combined, it won't combine again
    def move_right(self):
        """Move tiles right"""
        for col in reversed(range(0, 3)):
            for row in range(0, 4):
                currTile: Tile = self._board[row][col]
                if not currTile.is_zero():
                    for targetCol in range(col+1, 4):
                        targetTile: Tile = self._board[row][targetCol] 
                        if targetTile.is_zero():
                            targetTile.set_value(currTile.value())
                            currTile.reset_value()
                            currTile = targetTile
                        else:
                            if targetTile != currTile:
                                break
                            elif targetTile.can_combine(currTile):
                                self._score += targetTile.combine()
                                currTile.reset_value()
        self.spawn_tile()

    # Example of abstraction, hides implementation on how tiles move down
    # Starts from the second row from bottom
    # Then moves tiles as far down as possible, combining where possible
    # If a tile has already combined, it won't combine again
    def move_down(self):
        """Moves tiles down"""
        for row in reversed(range(0, 3)):
            for col in range(0, 4):
                currTile: Tile = self._board[row][col]
                if not currTile.is_zero():
                    for targetRow in range(row+1, 4):
                        targetTile: Tile = self._board[targetRow][col] 
                        if targetTile.is_zero():
                            targetTile.set_value(currTile.value())
                            currTile.reset_value()
                            currTile = targetTile
                        else:
                            if targetTile != currTile:
                                break
                            elif targetTile.can_combine(currTile):
                                self._score += targetTile.combine()
                                currTile.reset_value()
        self.spawn_tile()

    # Example of abstraction, hides implementation on how tiles move left
    # Starts from the second column from left
    # Then moves tiles as far left as possible, combining where possible
    # If a tile has already combined, it won't combine again
    def move_left(self):
        """Moves tiles left"""
        for col in range(1, 4):
            for row in range(0, 4):
                currTile: Tile = self._board[row][col]
                if not currTile.is_zero():
                    for targetCol in reversed(range(0, col)):
                        targetTile: Tile = self._board[row][targetCol] 
                        if targetTile.is_zero():
                            targetTile.set_value(currTile.value())
                            currTile.reset_value()
                            currTile = targetTile
                        else:
                            if targetTile != currTile:
                                break
                            elif targetTile.can_combine(currTile):
                                self._score += targetTile.combine()
                                currTile.reset_value()
        self.spawn_tile()
        
# Avoiding circular import
from . import scene