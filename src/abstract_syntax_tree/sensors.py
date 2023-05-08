from enum import Enum

from src.abstract_syntax_tree import BooleanNode


class HubInteraction(Enum):
    SHAKE = "shaken"
    TAPPED = "tapped"
    FALLING = "falling"

    def code(self) -> str:
        return self.value


class HubInteractionNode(BooleanNode):
    """Class to represent the HubInteraction block."""

    def __init__(self, interaction: HubInteraction) -> None:
        super().__init__()
        self.interaction = interaction

    def __str__(self) -> str:
        return f"HubInteractionNode(interaction: '{self.interaction}')"
