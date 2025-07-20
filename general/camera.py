#camera.py
from general.canvas import Canvas
from maths.transform import Point, Vector2


class Camera:
    def __init__(self, world_position: Point, canvas: Canvas, ignorable: list = []):
        self.data = {
            "world_position": world_position
        } #world position
        self.canvas = canvas
        self.ignorable = ignorable


    async def add_ignorable(self, object):
        if(object not in self.ignorable):
            self.ignorable.append(object)

    async def remove_ignorable(self, object):
        self.ignorable.remove(object)

    async def move(self, world_position):
        data = self.data
        dx = world_position.x - data.get("world_position").x
        dy = world_position.y - data.get("world_position").y

        for obj in self.canvas.objects:
            if(obj in self.ignorable):
                continue
            obj_pos = obj.position()
            await obj.move(Point(x=obj_pos.x - dx, y=obj_pos.y - dy))

        self.data["world_position"] = world_position #world position

    async def follow(self, object=None):
        if(object not in self.ignorable):
            await self.add_ignorable(object)
        await self.move(object.world_position())
        await object.move(Point.zero())
        await self.remove_ignorable(object)

    def world_position(self):
        return self.data["world_position"] #world position