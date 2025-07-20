# Turtle Engine

Game Engine made in pure python that uses python turtle for rendering.

---

## Features

- **Pure Python**: No external graphics dependencies—uses Python's built-in `turtle`.
- **Component-based architecture**: Behaviours, components, and objects for flexible game logic.
- **Physics**: Rigidbody and collision detection (BoxCollider).
- **Camera system**: World-to-screen transformations and camera following.
- **Input system**: Keyboard input with frame-accurate detection.
- **Shape primitives**: Easily create and manipulate squares and circles.
- **Async game loop**: Behaviours run asynchronously for smooth updates.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/IQ-GROUP/Turtle-Engine
   cd Turtle-Engine
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   - Requires Python 3.8+
   - Only dependency: `pynput` (for keyboard input)

---

## Quickstart Example

Below is a minimal example of a player controller using Turtle Engine. Save this as `assets/PlayerControllerExample.py` (already provided):

```python
from behaviours.common import CommonBehaviour
from components.rigidbody import Rigidbody
from general.camera import Camera
from general.canvas import Canvas
from general.shapes import Square
from general.inputs import Input
from maths.transform import Vector2, Point

class Test(CommonBehaviour):
    def __init__(self):
        self.tick = 0.0016  # 60 FPS
        self.enabled = True

    canvas = Canvas(640, 640)
    camera = Camera(Point.zero(), canvas)
    canvas.camera = camera

    player = None
    player_rb = None
    player_speed = 5

    async def start(self):
        self.player = Square(Point(0, -100), 50, 50, "blue", True, self.canvas).object()
        await self.canvas.spawn(self.player)
        await self.camera.add_ignorable(self.player)
        self.player_rb = Rigidbody(object=self.player, kinematic=True, mass=1)
        self.cube = Square(Point(0, -200), 10, 1000, "black", True, self.canvas).object()
        await self.canvas.spawn(self.cube)

    async def update(self):
        input = Input()
        world_position = self.player.world_position()
        direction = Vector2.zero()
        if input.get_key("W"): direction.y += 1
        if input.get_key("S"): direction.y -= 1
        if input.get_key("A"): direction.x -= 1
        if input.get_key("D"): direction.x += 1
        if input.get_key("X"): self.player_rb.kinematic = False
        else: self.player_rb.kinematic = True
        if direction != Vector2().zero():
            direction.normalize()
            direction.x *= self.player_speed
            direction.y *= self.player_speed
        new_position = Point(x=world_position.x + direction.x, y=world_position.y + direction.y)
        await self.player_rb.apply_force(new_position.vector2())
        await self.camera.follow(self.player)
        self.canvas.tupdate()
```

To run the engine:
```bash
python engine.py
```

---

## Project Structure

```
Turtle-Engine/
├── assets/           # User scripts and game logic (auto-loaded)
├── behaviours/       # Core behaviour base classes
├── components/       # Physics and collision components
├── general/          # Core engine systems (camera, canvas, input, shapes)
├── maths/            # Math utilities (Point, Vector2)
├── engine.py         # Engine entry point
├── requirements.txt  # Dependencies
└── README.md         # Documentation
```

---

## Architecture Overview

### Behaviours
- **CommonBehaviour**: Base class for all scripts. Implements async `start`, `update`, and `late_update` methods. All user scripts should inherit from this.

### Components
- **Rigidbody**: Adds physics and movement to objects. Supports kinematic and dynamic modes.
- **BoxCollider**: Handles axis-aligned bounding box collision detection.

### General Systems
- **Canvas**: Manages rendering, object spawning, and coordinate transforms.
- **Camera**: Handles world-to-screen mapping and camera following.
- **Input**: Singleton for keyboard input (using `pynput`).
- **Shapes**: Primitives for `Square` and `Circle` objects.
- **Object**: Base class for all renderable/movable entities.

### Maths
- **Point**: 2D point with utility methods.
- **Vector2**: 2D vector with normalization and conversion.

---

## API Reference

### Behaviours
```python
class CommonBehaviour:
    async def start(self): ...
    async def update(self): ...
    async def late_update(self): ...
    async def run(self): ...
```

### Components
```python
class Rigidbody:
    def __init__(self, object, mass=1, kinematic=True, gravity_force=Vector2(0, -9.8))
    async def apply_force(self, force: Vector2)

class BoxCollider:
    def __init__(self, object)
    def collided(self, ignorables=[]) -> bool
    def collided_with(self, object) -> bool
    def collisions(self, ignorables=[]) -> list
```

### General Systems
```python
class Canvas:
    def __init__(self, width=500, height=500, camera=None)
    async def spawn(self, object)
    async def destroy(self, object)
    async def move_world(self, object, world_position)
    def tupdate(self)

class Camera:
    def __init__(self, world_position, canvas, ignorable=[])
    async def follow(self, object)
    async def move(self, world_position)

class Input:
    def get_key(self, key: str) -> bool
    def get_key_down(self, key: str) -> bool
```

### Shapes
```python
class Square:
    def __init__(self, world_position, height, width, color, fill, canvas, name="Square")
    def object(self) -> Object

class Circle:
    def __init__(self, world_position, radius, color, fill, canvas, name="Circle")
    def object(self) -> Object
```

### Maths
```python
class Point:
    def __init__(self, x=0, y=0)
    @classmethod
    def zero(cls)
    def t_pos(self) -> list[float]
    def vector2(self) -> Vector2

class Vector2:
    def __init__(self, x=0, y=0)
    def normalize(self)
    @classmethod
    def zero(cls)
    def point(self) -> Point
```

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
