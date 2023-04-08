from src.abstract_syntax_tree import Node, StackNode


class WhenProgramStartsNode(StackNode):
    """Class to represent the WhenProgramStarts block.
    Keeps track of the x and y position of the block for later code generation."""

    # TODO: This probably also needs to keep track of the variables that are being used in this stack
    def __init__(self, x: int, y: int, next: Node) -> None:
        super().__init__(next)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "WhenProgramStartsNode"
