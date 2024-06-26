# Houman's 2048 Game

## Getting Started

1. Install fontconfig `sudo apt install fontconfig`
2. Create a virtual environment for development `python -m venv .venv`
3. Activate the environment `source .venv/bin/activate`
4. Install the requirements `pip install -r requirements.txt`
5. Start the application `python -m Game` from directory `2048/`

## Classes
- Game
    - Holds the game loop
    - Sets up pygame 
    - Has the scene, board
    - Handles user input
    - Handles behaviour based on game state

- Renderable
    - Abstract class for drawing to screen

- Actor
    - Abstract class for updating actors.
    - Is Renderable

- Scene
    - Holds all actors
    - Updates and draws all actors

- Board
    - Is an Actor
    - Holds all tiles
    - Handles moving tiles
    - Handles telling tiles to combine
    - Handles checking board state

- Tile
    - Is an Actor
    - Holds a value and behaviour to manipulate value

## Inheritance
1. Actor is a Renderable
2. Tiles, Board, and Scene are Actors

## Polymorphism
1. Tiles, Board, and Scene override Actors update()
2. Tiles, Board, and Scene override Renderables draw()

When the game calls Scene.update() and Scene.draw()
Those in turn call update() and draw for all actors in game.
This includes the board and Tiles which overrides the parent class update() and draw()

## Abstraction
1. The game reads user input, and calls move in a direction on the board. The board abstracts the implementation of the actual move.
2. Within the board move functions, tiles asked if they can be combined, and are told to combine. Tiles abstract the implementation of combining.

1. The game calls update() and draw() on scene. Scene handles the implementation.
2. Scene in turn calls update() and render() on each actor, and each handle the implementation based on their polymorphic natures.

## Non primitive types
1. A 2D List used for board. The board does not change size. It holds mutable Tiles. It is easy to grab data based on index and no tile needs to be removed. Tile values are updated, tiles are not moved.
2. Tuples were used to hold data such as colours since they should not be changed by code once grabbed from the constants.json file.

## Changes from Design
1. Tiles do not move, instead their values are updated: More simple design, did not need more complex data types to hold these tiles
2. Tiles do break into further children classes of Random and Existing: This implementation is handled in creation and update of Tile class
3. Game Objects renamed to Actors
4. Grid and Board are one class Board, is Actor, is Renderable. The grid is a 2D Array in Board, acts as data with functionality implemented in Board class.
5. Game Manager is called Game. Game holds a Scene and Board.