from behaviours.common import CommonBehaviour
from pynput import keyboard
from typing import Set, Dict, Optional


class Input(CommonBehaviour):
    def __init__(self):
        self.enabled = True
        self.tick = 0.0016

    _instance: Optional['Input'] = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._current_frame_keys: Set[keyboard.KeyCode] = set()
            cls._instance._new_keys_this_frame: Set[keyboard.KeyCode] = set()
            cls._instance._listener: Optional[keyboard.Listener] = None
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        """Initialize the input system."""
        self._listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self._listener.daemon = True
        self._listener.start()

    def get_key(self, key: str) -> bool:
        """Returns True while the key is held down."""
        key_char = key.lower()
        return any(k == keyboard.KeyCode.from_char(key_char) for k in self._current_frame_keys)

    def get_key_down(self, key: str) -> bool:
        """Returns True only on the first frame the key is pressed."""
        key_char = key.lower()
        return any(k == keyboard.KeyCode.from_char(key_char) for k in self._new_keys_this_frame)

    async def late_update(self):
        """Must be called at the end of each frame."""
        self._new_keys_this_frame.clear()

    def _on_press(self, key):
        """Internal handler for key press events."""
        if key not in self._current_frame_keys:
            self._new_keys_this_frame.add(key)
        self._current_frame_keys.add(key)

    def _on_release(self, key):
        """Internal handler for key release events."""
        try:
            self._current_frame_keys.remove(key)
        except KeyError:
            pass