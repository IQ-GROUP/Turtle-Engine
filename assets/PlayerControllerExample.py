#PlayerControllerExample.py

#Imports
from behaviours.common import CommonBehaviour
from components.rigidbody import Rigidbody
from general.camera import Camera
from general.canvas import Canvas
from general.shapes import Square
from general.inputs import Input
from maths.transform import Vector2, Point

class Test(CommonBehaviour):
    def __init__(self):
        self.tick = 0.0016 #Tick time in seconds for 60FPS
        self.enabled = True #Flag to enable the script to run


    #Initializing camera and canvas
    canvas = Canvas(640, 640)
    camera = Camera(Point.zero(), canvas)
    canvas.camera = camera

    #Player references
    player = None
    player_rb = None
    player_speed = 5

    # Behaviour method, called in the first frame
    async def start(self):

        #Initializing player
        self.player = Square(Point(0, -100), 50, 50, "blue", True, self.canvas).object()
        await self.canvas.spawn(self.player)
        await self.camera.add_ignorable(self.player)
        self.player_rb = Rigidbody(object=self.player, kinematic=True, mass=1)

        #Spawning wall
        self.cube = Square(Point(0, -200), 10, 1000, "black", True, self.canvas).object()
        await self.canvas.spawn(self.cube)


    #Behaviour method, being called each frame
    async def update(self):

        input = Input() #Initializing input

        world_position = self.player.world_position() #Getting current world position
        direction = Vector2.zero() #Initializing direction

        #Direction change depending on the input
        if(input.get_key("W")):
            direction.y += 1
        if (input.get_key("S")):
            direction.y -= 1
        if (input.get_key("A")):
            direction.x -= 1
        if (input.get_key("D")):
            direction.x += 1

        #Physics toogling
        if(input.get_key("X")):
            self.player_rb.kinematic = False
        else:
            self.player_rb.kinematic = True

        if(direction != Vector2().zero()):
            direction.normalize() #Avoiding faster speed when moving diagonaly

            #Multiplying by player speed
            direction.x *= self.player_speed
            direction.y *= self.player_speed

        #Initializing new position
        new_position = Point(x=world_position.x + direction.x,
                        y=world_position.y + direction.y)

        await self.player_rb.apply_force(new_position.vector2()) #Apply force to rigidbody
        await self.camera.follow(self.player) #Making camera follow player

        self.canvas.tupdate() #Updating the screen