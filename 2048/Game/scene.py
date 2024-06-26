from collections import defaultdict
from typing import List, TypeVar, Iterable, Type, Dict, Tuple

import pygame

from .actor import Actor

class Scene(Actor):
    """
    Holds all actors in game.
    Calls update and render on all game actors. (Polymorphism and Abstraction)
    Is an Actor (inheritance) and only one scene per game.
    """
    _SINGLETON = None

    def __new__(cls) -> "Scene":
        # make the instance and return it
        # the output of this function is then passed to __init__
        if cls._SINGLETON is None:
            cls._SINGLETON = super().__new__(cls)
        
        return cls._SINGLETON

    def __init__(self):
        self._actors: List[Actor] = []
    
    def add_actor(self, actor: Actor) -> None:
        """Add actor to scene"""
        existing_entries = list(filter(lambda a: a is actor, self._actors))
        if len(existing_entries) > 0:
            return
        self._actors.append(actor)

    def update(self, dT) -> None:
        """Update all actors"""
        for actor in self._actors:
            actor.update(self, dT) # Polymorphism and abstraction
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw all actors"""
        for actor in self._actors:
            actor.draw(screen) # Polymorphism and abstraction
        pygame.display.update()
