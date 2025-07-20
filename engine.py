# engine.py
import os
import importlib
from behaviours.common import CommonBehaviour
import asyncio


def import_all_scripts():
    folder_path = os.path.join(os.path.dirname(__file__), "assets")

    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            full_module = f"assets.{module_name}"
            importlib.import_module(full_module)


async def main():
    import_all_scripts()

    # Create all behaviour instances
    instances = [cls() for cls in CommonBehaviour.__subclasses__()]

    # Start all behaviours
    tasks = []
    for instance in instances:
        if(instance.enabled):
            print(f"Starting {instance.__class__.__name__}")
            tasks.append(asyncio.create_task(instance.run()))

    # Run forever (or until all tasks complete)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())