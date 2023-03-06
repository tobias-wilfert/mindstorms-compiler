from enum import Enum


class AST:
    """Abstract Syntax Tree that holds a list of hat nodes, which each represent a code stack."""

    # List of hat nodes, each can be interpreted as a sub tree, as such this is a forrest.
    # Needed since multiple code stacks can be present in a progam (i.e, function declarations)
    hat_nodes: list

    def __init__(self) -> None:
        self.hat_nodes = []

    def tree_representation(self, file_name: str = None) -> str:
        """Generates a dot representation of the AST and writes it to a file is file_name is provided.

        :param file_name: The name of the file to write the representation to, defaults to None.
        :type file_name: str, optional
        :return: The dot source code, or a string specifying where the code is written to.
        :rtype: str
        """
        nodes = []
        connections = []
        for hat_root in self.hat_nodes:
            hat_root.genereate_tree_representation(nodes, connections, -1, 0)

        full_representation = (
            'digraph {rankdir="TB"\n'
            + "\n".join(nodes)
            + "\n"
            + "\n".join(connections)
            + "}"
        )

        if file_name:
            with open(file_name + ".gv", "a") as file:
                file += full_representation
            return f"The representaion is written to {file_name}.gv"
        else:
            return full_representation


class Node:
    """Base class for all the nodes that can be found in the AST."""

    def __init__(self) -> None:
        pass

    def genereate_tree_representation(
        self, nodes: list, connections: list, parent_id: int, node_count: int
    ):
        """Generates the representation for this node

        :param nodes: Declerations of all the nodes.
        :type nodes: list
        :param connections: Connections between the nodes.
        :type connections: list
        :param parent_id: The id of the parent node.
        :type parent_id: int
        :param node_count: The count of the number of nodes that have already been visited (used to generate the UID for each node).
        :type node_count: int
        """
        raise NotImplementedError(
            "genereate_tree_representation() was called in the base class."
        )


class StackNode(Node):
    """The Base class for all Stack block, that are blocks which have a next pointer."""

    def __init__(self, next) -> None:
        super().__init__()
        self.next = next


class WhenProgramStartsNode(StackNode):
    """Class to represent the WhenProgramStarts block.
    Keeps track of the x and y position of the block for later code generation."""

    def __init__(self, x: int, y: int, next: Node) -> None:
        super().__init__(next)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "WhenProgramStartsNode"

    def genereate_tree_representation(
        self, nodes: list, connections: list, parent_id: int, node_count: int
    ):
        # Claim a node_id and update the node_counter
        node_id = node_count
        node_count += 1
        # Add the node representation to nodes, based on __str__
        nodes.append(f'{node_id} [label="{self}"]')
        # Generate the representation of the next node if there is one
        if self.next:
            self.next.genereate_tree_representation(
                nodes, connections, node_id, node_count
            )


class Direction(Enum):
    """Enum for the directions that can be used in the RunMotor blocks."""

    CLOCKWISE = 1
    COUNTERCLOCKWISE = 2


class Unit(Enum):
    """Enum for the units that can be used in the RunMotor blocks."""

    ROTATIONS = 1
    SECONDS = 2
    DEGREES = 3


class NumericalNode(Node):
    """Class to represent any numerical value, float or int."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # Could be both Float or Int

    def __str__(self) -> str:
        return f"NumericalNode({self.value})"

    def genereate_tree_representation(
        self, nodes: list, connections: list, parent_id: int, node_count: int
    ):
        node_id = node_count
        node_count += 1

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')


class RunMotorForDurationNode(StackNode):
    """Class to represent RunMotorForDuration blocks."""

    def __init__(
        self, ports: list, direction: Direction, value: Node, unit: Unit, next: Node
    ) -> None:
        super().__init__(next)
        self.ports = ports
        self.direction = direction
        self.value = value  # Could be both a NumericalNode or an expression or a Variable that evaluates to a numerical TODO: Add a test for that
        self.unit = unit

    def __str__(self) -> str:
        return f"RunMotorForDurationNode(ports:'{self.ports}', direction:'{self.direction}', unit:'{self.unit}',)"

    def genereate_tree_representation(
        self, nodes: list, connections: list, parent_id: int, node_count: int
    ):
        node_id = node_count
        node_count += 1

        connections.append(f"{parent_id} -> {node_id}")
        nodes.append(f'{node_id} [label="{self}"]')
        self.value.genereate_tree_representation(
            nodes, connections, node_id, node_count
        )

        if (
            self.next
        ):  # If there is a connection add it and epxlore further into the tree
            self.next.genereate_tree_representation(
                nodes, connections, node_id, node_count
            )
