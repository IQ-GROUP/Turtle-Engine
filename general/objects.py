import turtle

class Object:
    def __init__(self, canvas, data):
        self.canvas = canvas
        self.data = data
        turtle.tracer(0, 0)
        self.t = turtle.Turtle()
        self.t.speed(0)
        self.t.hideturtle()

    async def move_world(self, world_position):
        self.data["world_position"] = world_position
        screen_position = self.canvas.world_to_screen(world_position)
        self.data["position"] = screen_position
        await self.canvas.spawn(self)

    async def move_world_preview(self, world_position):
        preview_data = self.get().copy()
        preview_data["world_position"] = world_position
        screen_position = self.canvas.world_to_screen(world_position)
        preview_data["position"] = screen_position
        return Object(self.canvas, preview_data)

    async def move(self, position):
        world_position = self.canvas.screen_to_world(position)
        self.data["world_position"] = world_position
        self.data["position"] = position
        await self.canvas.spawn(self)

    def get(self):
        return self.data

    def name(self):
        return self.data.get("name")

    def position(self):  # screen position
        return self.data.get("position")

    def world_position(self): #world position
        return self.data.get("world_position")

    def instruction(self):
        return self.data.get("instruction")

    def size(self):
        return self.data.get("size")

    def spawned(self):
        return self.data.get("spawned")

    def get_t(self):
        return self.t
