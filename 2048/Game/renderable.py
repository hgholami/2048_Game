import pygame
from abc import ABC, abstractmethod

class Renderable(ABC):
    """
    Abstract class of Renderables in game.
    A type that can be rendered onto a surface.
    """
    @abstractmethod
    def draw(self, screen: pygame.surface.Surface) -> None:
        """Render to the provided surface."""
        pass