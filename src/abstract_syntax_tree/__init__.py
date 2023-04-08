class UIDGenerator:
    """Simple UID generator."""

    def __init__(self) -> None:
        self.count = -1

    def get_uid(self) -> int:
        self.count += 1
        return self.count


class AST:
    """Abstract Syntax Tree that holds a list of hat nodes, which each represent a code stack."""

    # List of hat nodes, each can be interpreted as a sub tree, as such this is a forrest.
    # Needed since multiple code stacks can be present in a program (i.e, function declarations)
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
        uid_generator = UIDGenerator()
        for hat_root in self.hat_nodes:
            hat_root.generate_tree_representation(nodes, connections, -1, uid_generator)

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
            return f"The representation is written to {file_name}.gv"
        else:
            return full_representation


class Node:
    """Base class for all the nodes that can be found in the AST."""

    def __init__(self) -> None:
        pass

    def custom_representation(self, nodes, connections, node_id, uid_generator):
        # Should be called if there is any custom representation logic that needs to be done
        pass

    def generate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        """Generates the representation for this node

        :param nodes: Decelerations of all the nodes.
        :type nodes: list
        :param connections: Connections between the nodes.
        :type connections: list
        :param parent_id: The id of the parent node.
        :type parent_id: int
        :param uid_generator: UID-generator so that every node can generates its own uid.
        :type uid_generator: UIDGenerator
        """
        # Claim a node_id and update the node_counter
        node_id = uid_generator.get_uid()
        # Add the node representation to nodes, based on __str__
        nodes.append(f'{node_id} [label="{self}"]')
        # Connect to parent, unless it is the first node
        if parent_id != -1:
            connections.append(f"{parent_id} -> {node_id}")
        # Do any custom logic if necessary
        self.custom_representation(nodes, connections, node_id, uid_generator)


class StackNode(Node):
    """The Base class for all Stack block, that are blocks which have a next pointer."""

    def __init__(self, next) -> None:
        super().__init__()
        self.next = next

    def generate_tree_representation(
        self,
        nodes: list,
        connections: list,
        parent_id: int,
        uid_generator: UIDGenerator,
    ):
        # Claim a node_id and update the node_counter
        node_id = uid_generator.get_uid()
        # Add the node representation to nodes, based on __str__
        nodes.append(f'{node_id} [label="{self}"]')
        # Connect to parent, unless it is the first node
        if parent_id != -1:
            connections.append(f"{parent_id} -> {node_id}")
        # Do any custom logic if necessary
        self.custom_representation(nodes, connections, node_id, uid_generator)
        # If there is a next node also generate the representation for it
        if self.next:
            self.next.generate_tree_representation(
                nodes, connections, node_id, uid_generator
            )


class NumericalNode(Node):
    """Class to represent any numerical value, float or int."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # Could be both Float or Int

    def __str__(self) -> str:
        return f"NumericalNode({self.value})"


class LiteralNode(Node):
    """Class to represent any string literal."""

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value  # String

    def __str__(self) -> str:
        return f"LiteralNode('{self.value}')"
