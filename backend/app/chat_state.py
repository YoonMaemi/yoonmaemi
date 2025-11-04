"""In-memory chat history management."""

from threading import Lock
from typing import List

from .models import Message


class ChatState:
    """Thread-safe container for the single chat session history."""

    def __init__(self) -> None:
        self._history: List[Message] = []
        self._lock = Lock()

    def append(self, message: Message) -> None:
        """Persist a message to the in-memory history."""
        with self._lock:
            self._history.append(message)

    def snapshot(self) -> List[Message]:
        """Return a copy of the current history."""
        with self._lock:
            return list(self._history)

    def reset(self) -> None:
        """Clear the history."""
        with self._lock:
            self._history.clear()

