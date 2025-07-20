#box_collider.py
from general.objects import Object
from general.shapes import Square
import asyncio
from maths.transform import Vector2

class BoxCollider:
    def __init__(self, object: Object = None):
        self.object = object

    def get_collider_cords(self, world_position, size):
        h_width = size.get("width") // 2
        h_height = size.get("height") // 2
        return {
            "x": Vector2(x=world_position.x - h_width, y=world_position.x + h_width),
            "y": Vector2(x=world_position.y - h_height, y=world_position.y + h_height)
        }


    def collided(self, ignorables: list[Object] = []) -> bool:
        if (self.collisions(ignorables) != []):
            return True
        return False

    def collided_with(self, object: Object) -> bool:
        if(object in self.collisions()):
            return True
        return False

    def overlaps(self, a_min, a_max, b_min, b_max):
        return a_min < b_max and a_max > b_min

    def collisions(self, ignorables: list[Object] = []) -> list:
        objects = self.object.canvas.objects
        world_position = self.object.world_position()
        size = self.object.size()

        cc = self.get_collider_cords(world_position, size)

        collisions = []

        for obj in objects:
            if obj == self.object or obj in ignorables:
                continue

            if(not obj.canvas.on_screen(obj)):
                continue

            obj_cc = self.get_collider_cords(obj.world_position(), obj.size())

            x_overlap = self.overlaps(cc["x"].x, cc["x"].y, obj_cc["x"].x, obj_cc["x"].y)
            y_overlap = self.overlaps(cc["y"].x, cc["y"].y, obj_cc["y"].x, obj_cc["y"].y)

            if x_overlap and y_overlap:
                collisions.append(obj)

        return collisions