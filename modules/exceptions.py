"""Exceptions"""

# ruff: noqa: D101,D107
# pylint: disable=missing-class-docstring

from modules.features import Pipe


class NoProjectError(Exception):
    def __init__(self) -> None:
        super().__init__("No project found")


class LayerTreeError(Exception):
    def __init__(self) -> None:
        super().__init__("Layer tree error")


class NewLayerInvalidError(Exception):
    def __init__(self, layer_name: str) -> None:
        super().__init__(f"{layer_name} is not a valid layer")


class PipeNotConnectedToMultipleBuildingsError(Exception):
    def __init__(self, pipe: Pipe) -> None:
        super().__init__(f"Pipe {pipe.id} is not connected to multiple buildings")
