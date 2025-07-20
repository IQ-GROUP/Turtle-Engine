import turtle as t
from general.objects import Object
from maths.transform import Point

class Canvas:
    def __init__(self, width=500, height=500, camera=None):
        self.camera = camera
        self.width = width
        self.height = height
        t.setup(width=width, height=height)
        t.bgcolor("white")
        t.tracer(0)
        t.hideturtle()
        self.objects = []

    def world_to_screen(self, world_pos: Point) -> Point:
        return Point(
            world_pos.x - self.camera.world_position().x,
            world_pos.y - self.camera.world_position().y
        )

    def screen_to_world(self, screen_pos: Point) -> Point:
        return Point(
            screen_pos.x + self.camera.world_position().x,
            screen_pos.y + self.camera.world_position().y
        )

    def generate_object_id(self):
        id = 0
        used_ids = [obj.get().get('id') for obj in self.objects]
        while id in used_ids:
            id += 1
        return id

    def add_object(self, object):
        if object not in self.objects:
            self.objects.append(object)
        return object

    def get_object_by_id(self, id):
        for obj in self.objects:
            if obj.get().get("id") == id:
                return obj
        return None

    def on_screen(self, object: Object) -> bool:
        position = object.position()
        size = object.size()
        width = size.get('width')
        height = size.get('height')
        if (
                position.x + width / 2 < -self.width / 2 or
                position.x - width / 2 > self.width / 2 or
                position.y + height / 2 < -self.height / 2 or
                position.y - height / 2 > self.height / 2
        ):
            return False
        return True

    async def spawn(self, object):
        turtle = object.get_t()
        turtle.clear()


        if (object not in self.objects):
            self.add_object(object)
        object.data["spawned"] = True

        if(not self.on_screen(object)):
            return object

        turtle.penup()
        turtle.goto(object.position().t_pos())
        turtle.pendown()
        turtle.color("black")
        object.instruction()(turtle)
        return object

    async def destroy(self, object):
        object.get_t().clear()

    async def despawn(self, object):
        self.destroy(object)
        self.objects.remove(object)
        object.data["spawned"] = False

    async def move_world(self, object, world_position):
        await object.move_world(world_position)

    async def move(self, object, position):
        await object.move(position)

    def tupdate(self):
        t.update()