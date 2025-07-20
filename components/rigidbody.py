#rigidbody.py
from components.box_collider import BoxCollider
from general.objects import Object
from maths.transform import Vector2

class Rigidbody():
    def __init__(self, object, mass: float =1, kinematic: bool =True, gravity_force: Vector2 = Vector2(0, -9.8)):
        self.object = object
        self.mass = mass
        self.kinematic = kinematic
        self.gravity_force= gravity_force

    async def apply_force(self, force: Vector2 = Vector2.zero()) -> Object:

        if(not self.kinematic):
            force = Vector2(
                force.x + self.mass * self.gravity_force.x,
                force.y + self.mass * self.gravity_force.y,
            )

        preview_object = await self.object.move_world_preview(force.point())

        if(not BoxCollider(preview_object).collided([self.object])):
            await self.object.move_world(force)
            return self.object

        return self.object