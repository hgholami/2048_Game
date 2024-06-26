from abc import ABC, abstractmethod

import pygame

from .renderable import Renderable

class Actor(Renderable, ABC):
    """
    Abstract class of Actors in game. Actors are renderables.
    """
    
    @abstractmethod
    def update(self, scene: "scene.Scene", dT) -> None:
        """Update this actor given that the provided amount of time has passed."""
        pass

from . import scene