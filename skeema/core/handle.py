from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from .handle_manager import HandleEntry, HandleManager


class Handle:
    """
    Handle
    """

    INVALID_INDEX = ~0x0
    ZEROTH_GENERATION = 0

    def __init__(self, index: int = INVALID_INDEX, generation: int = ZEROTH_GENERATION) -> None:
        self._index = index
        self._generation = generation

    @property
    def index(self) -> int:
        return self._index

    @property
    def generation(self) -> int:
        return self._generation

    def __eq__(self, other: Any) -> bool:
        return (
            self._index == other.index
            and self._generation == other.generation
        )


INVALID_HANDLE = Handle()


class HandleValidationException(Exception):
    def __init__(self, handle_manager: HandleManager, handle: Handle, msg: str = None):
        if msg is None:
            msg = f"A validation error occurred with handle {handle} used in manager {handle_manager}."
        super().__init__(msg)
        self._handle_manager: HandleManager = handle_manager
        self._handle: Handle = handle


class HandleInvalidException(HandleValidationException):
    def __init__(self, handle_manager: HandleManager, handle: Handle):
        super().__init__(
            handle_manager, handle,
            "Handle is invalid. Was this handle issued by a Handle Manager?"
        )


class HandleOutOfRangeException(HandleValidationException):
    def __init__(self, handle_manager: HandleManager, handle: Handle):
        super().__init__(
            handle_manager, handle,
            f"Handle index is out of range for this Handle Manager. Was it issued by another Handle Manager?"
            f"Handle index: {handle.index}, Manager range: {handle_manager.num_entries}."
        )


class HandleIsInactiveException(HandleValidationException):
    def __init__(self, handle_manager: HandleManager, handle: Handle):
        super().__init__(
            handle_manager, handle,
            "Handle must be active to get or remove it. Has this handle already been removed?"
        )


class HandleIsRetiredException(HandleValidationException):
    def __init__(self, handle_manager: HandleManager, handle: Handle, entry: HandleEntry):
        super().__init__(
            handle_manager, handle,
            "Handle no longer refers to a valid resource in this manager. Another resource is being managed here."
            f"Handle generation: {handle.generation}, Entry generation: {entry.generation}."
        )
