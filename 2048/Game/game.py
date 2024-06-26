import json
import pygame
from .board import Board
from .board import State
from .scene import Scene

MILLISECONDS_PER_SECOND = 1000.0

class Game:
    """Handles game logic. Is singleton, only one game instance can exist at one time."""

    _SINGLETON = None

    # make the instance and return it
    # the output of this function is then passed to __init__
    # Stops more than one instance of this object
    def __new__(cls) -> "Game":
        if cls._SINGLETON is None:
            cls._SINGLETON = super().__new__(cls)

        return cls._SINGLETON

    # Initilize game
    # Loads data from constants.json
    #   - Can alter game visuals and key bindings without altering code
    # 
    def __init__(self) -> None:
        self._consts = json.load(open("./Game/constants.json", "r"))

        pygame.font.init()

        # used to limit the speed of our program so that
        # we don't waste CPU cycles running faster than necessary
        self._desired_framerate = self._consts["target_fps"]  # Frames Per Second

        # Set up pygame window
        pygame.display.set_caption("Houman's 2048")
        self._window_size = pygame.math.Vector2(self._consts["size"], self._consts["size"])
        icon = pygame.transform.scale(pygame.image.load("./Game/images/icon.ico"), (32, 32))
        pygame.display.set_icon(icon)

        # used to keep track of the passing time and framerate
        self._clock = pygame.time.Clock()

        # Holds reference to all actors, this way we can call just iterate and call update and render on them all
        self._scene = Scene()

        # Holds reference to board pieces, handles board logic like movement of tiles
        self._board = Board(self._scene, self._consts)
        self._scene.add_actor(self._board)

    def run(self) -> int:
        """Runs the game. Contains the main game loop."""
        average_fps = 0.0
        debug_font = pygame.font.SysFont('ubuntumono', 12)
        
        surface = pygame.display.set_mode(self._window_size)

        # main game loop
        while True:
            dT_millis = self._clock.tick(self._desired_framerate)
            dT_seconds = dT_millis / MILLISECONDS_PER_SECOND

            fps = 1.0/dT_seconds
            average_fps = average_fps * 0.9 + fps * 0.1

            # Event tracking, used to read user key inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    return 0
            
                if event.type == pygame.KEYDOWN:
                    if str(event.key) in self._consts["keys"]:
                        key = self._consts["keys"][str(event.key)]
                        # This is an example of abstraction
                        # The board handles implementation of movement,
                        # the game only calls which direction based on input
                        match key:
                            case "up":
                                self._board.move_up()
                            case "right":
                                self._board.move_right()
                            case "down":
                                self._board.move_down()
                            case "left":
                                self._board.move_left()

            # Another example of abstraction, update called on scene without implementation known
            # Scene updates all actors within
            self._scene.update(dT_seconds)
            
            # Grabs the current state of the board: Play, Win, Lose
            state = self._board.check_state()

            surface.fill(self._consts["colour"]["background"])

            # Another example of abstraction, render called on scene without implementation known
            # Scene renders all actors within
            self._scene.draw(surface)
            
            # Check if game has ended
            # If yes, display score and exit game loop
            if state != State.play:
                font = pygame.font.SysFont(self._consts["font"], self._consts["font_size"], bold=True)
                size = self._consts["size"]
                endScreen = pygame.Surface((size, size), pygame.SRCALPHA)
                endScreen.fill(self._consts["colour"]["over"])
                surface.blit(endScreen, (0, 0))
                text = font.render(f"Score: {self._board._score}", 1, tuple(self._consts["colour"]["dark"]))
                surface.blit(text, (size/2-text.get_rect().width/2, size/2-text.get_rect().height/2))
                pygame.display.flip()
                break
                
            # Show fps
            text_surface = debug_font.render(f"FPS: {average_fps:.02f}", False, (255, 255, 255))
            surface.blit(text_surface, (2, 2))

            # update the window contents with the surfance contents
            pygame.display.flip()

        # Show the end screen until user exits
        while(True):
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    return 0
            