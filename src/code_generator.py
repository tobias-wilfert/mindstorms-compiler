from src.abstract_syntax_tree.abstract_syntax_tree import (
    AST,
    AddItemToListNode,
    ArithmeticalNode,
    ChangeVariableByNode,
    ListLiteralNode,
    LiteralNode,
    MotorGoToPositionNode,
    MotorPositionNode,
    MotorSpeedNode,
    Node,
    NumericalNode,
    RunMotorForDurationNode,
    SetMotorSpeedNode,
    SetVariableToNode,
    StartMotorNode,
    StopMotorNode,
    TurnDirection,
    VariableNode,
    WhenProgramStartsNode,
)


class CodeGenerator:
    def __init__(self):
        """The goal for the code generation is to translate the code as literal as possible.
        Furthermore the goal is to generate code as close as the boilerplate that is provided by LEGO.
        """

        # All the includes that LEGO deems necessary
        self.includes = """from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
from mindstorms.control import wait_for_seconds, wait_until, Timer
from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
import math
"""
        # Collection of all the objects that are added to self.objects_code
        self.objects = set()

        self.objects_code = ""
        self.program_code = ""

    def generate(self, ast: AST) -> str:
        # TODO: This will need to be changed later to support multiple block-states

        if len(ast.hat_nodes):  # Check if not empty
            self.visit(ast.hat_nodes[0])

        # Return the complete code
        return f"""{self.includes}
# Create your objects here.
{self.objects_code}
# Write your program here.
{self.program_code}
"""

    def visit(self, node: Node) -> str:
        """Visit the node in the AST, decide which type it is and call the appropriate method.

        :param node: The AST node that is being visited.
        :return: The code for the subtree rotted at node, if any (some sub-trees return trees, others don't)
        """

        if not node:
            return ""
        elif isinstance(node, WhenProgramStartsNode):
            return self.visit_when_program_starts_node(node)
        elif isinstance(node, RunMotorForDurationNode):
            return self.visit_run_motor_tor_duration_node(node)
        elif isinstance(node, NumericalNode):
            return self.visit_numerical_node(node)
        elif isinstance(node, ArithmeticalNode):
            return self.visit_arithmetical_node(node)
        elif isinstance(node, SetVariableToNode):
            return self.visit_set_variable_to_node(node)
        elif isinstance(node, VariableNode):
            return self.visit_variable_node(node)
        elif isinstance(node, MotorGoToPositionNode):
            return self.visit_motor_got_to_position_node(node)
        elif isinstance(node, StartMotorNode):
            return self.visit_start_motor_node(node)
        elif isinstance(node, StopMotorNode):
            return self.visit_stop_motor_node(node)
        elif isinstance(node, SetMotorSpeedNode):
            return self.visit_set_motor_speed_node(node)
        elif isinstance(node, MotorSpeedNode):
            return self.visit_motor_speed_node(node)
        elif isinstance(node, MotorPositionNode):
            return self.visit_motor_position_node(node)
        elif isinstance(node, ChangeVariableByNode):
            return self.visit_change_variable_by_node(node)
        elif isinstance(node, LiteralNode):
            return self.visit_literal_node(node)
        elif isinstance(node, AddItemToListNode):
            return self.visit_add_item_to_list_node(node)
        else:
            raise NotImplementedError(f"Currently no code can be generated for {node}")

    def generate_object(self, variable: str, object: str, ports: Node):
        """Generates the code for the object generation.

        :param variable: The variable that the object should be assigned to.
        :param object: The name of the constructor for the object.
        :param ports: A list or string of port identifier(s).
        """

        if variable not in self.objects:
            self.objects.add(variable)
            self.objects_code += f"{variable} = {object}({ports})\n"

    def visit_when_program_starts_node(self, node: WhenProgramStartsNode) -> str:
        self.visit(node.next)

    def visit_run_motor_tor_duration_node_fixed_ports(
        self, node: RunMotorForDurationNode
    ):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += "# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += "#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            # If the direction is counter wise negate the value
            value_code = self.visit(node.value)
            if node.direction == TurnDirection.COUNTERCLOCKWISE:
                value_code = f"-{value_code}"

            # Add the code and keep exploring
            if node.unit.code() == "degrees":
                self.program_code += f"{variable}.run_for_degrees(int({value_code}))  # Note: This methods expects an integer so wee need to convert the value.\n"
            else:
                self.program_code += (
                    f"{variable}.run_for_{node.unit.code()}({value_code})\n"
                )

        self.visit(node.next)

    def visit_run_motor_tor_duration_node_variable_ports(
        self, node: RunMotorForDurationNode
    ):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += """# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"for port in {node.ports.name}:\n"

        # If the direction is counter wise negate the value
        value_code = self.visit(node.value)
        if node.direction == TurnDirection.COUNTERCLOCKWISE:
            value_code = f"-{value_code}"

        if node.unit.code() == "degrees":
            self.program_code += f"\tMotor(port).run_for_degrees(int({value_code}))  # Note: This methods expects an integer so wee need to convert the value.\n"
        else:
            self.program_code += (
                f"\tMotor(port).run_for_{node.unit.code()}({value_code})\n"
            )
        self.visit(node.next)

    def visit_run_motor_tor_duration_node(self, node: RunMotorForDurationNode):
        if isinstance(node.ports, ListLiteralNode):
            self.visit_run_motor_tor_duration_node_fixed_ports(node)
        elif isinstance(node.ports, VariableNode):
            self.visit_run_motor_tor_duration_node_variable_ports(node)
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.ports}"
            )

    def visit_numerical_node(self, node: NumericalNode):
        return node.value

    def visit_arithmetical_node(self, node: ArithmeticalNode):
        return f"({self.visit(node.left_hand)} {node.op.code()} {self.visit(node.right_hand)})"

    def visit_set_variable_to_node(self, node: SetVariableToNode):
        self.program_code += f"{node.variable} = {self.visit(node.value)}\n"
        self.visit(node.next)

    def visit_variable_node(self, node: VariableNode):
        # TODO: Need to check how multiple variables are handled in a program. If that causes issue use the id here rather than the name (since the id is unique)
        # TODO: Might want to make the object here as well
        return node.name

    def visit_motor_got_to_position_node_fixed_ports(self, node: MotorGoToPositionNode):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += "# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += "#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            # If the direction is counter wise negate the value
            value_code = self.visit(node.value)
            if node.direction == TurnDirection.COUNTERCLOCKWISE:
                value_code = f"-{value_code}"  # TODO: Do some cashing for these.

            # Add the code and keep exploring
            self.program_code += f"{variable}.run_to_position(int({value_code}), '{node.direction.code()}')  # Note: This methods expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_motor_got_to_position_node_variable_ports(
        self, node: MotorGoToPositionNode
    ):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += """# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"for port in {node.ports.name}:\n"

        # If the direction is counter wise negate the value
        value_code = self.visit(node.value)
        if node.direction == TurnDirection.COUNTERCLOCKWISE:
            value_code = f"-{value_code}"

        # Add the code and keep exploring
        self.program_code += f"\tMotor(port).run_to_position(int({value_code}), '{node.direction.code()}')  # Note: This methods expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_motor_got_to_position_node(self, node: MotorGoToPositionNode):
        if isinstance(node.ports, ListLiteralNode):
            self.visit_motor_got_to_position_node_fixed_ports(node)
        elif isinstance(node.ports, VariableNode):
            self.visit_motor_got_to_position_node_variable_ports(node)
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.ports}"
            )

    def visit_start_motor_node_fixed_ports(self, node: StartMotorNode):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += "# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += "#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            if node.direction == TurnDirection.COUNTERCLOCKWISE:
                self.program_code += (
                    f"{variable}.start(-{variable}.get_default_speed())\n"
                )
            else:
                self.program_code += f"{variable}.start()\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_start_motor_node_variable_ports(self, node: StartMotorNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += """# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += "\tMotor(port).start()\n"
        self.visit(node.next)

    def visit_start_motor_node(self, node: StartMotorNode):
        if isinstance(node.ports, ListLiteralNode):
            self.visit_start_motor_node_fixed_ports(node)
        elif isinstance(node.ports, VariableNode):
            self.visit_start_motor_node_variable_ports(node)
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.ports}"
            )

    def visit_stop_motor_node_fixed_ports(self, node: StopMotorNode):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += "# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += "#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            self.program_code += f"{variable}.stop()\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_stop_motor_node_variable_ports(self, node: StopMotorNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += """# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += "\tMotor(port).stop()\n"
        self.visit(node.next)

    def visit_stop_motor_node(self, node: StopMotorNode):
        if isinstance(node.ports, ListLiteralNode):
            self.visit_stop_motor_node_fixed_ports(node)
        elif isinstance(node.ports, VariableNode):
            self.visit_stop_motor_node_variable_ports(node)
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.ports}"
            )

    def visit_motor_speed_node_fixed_ports(self, node: SetMotorSpeedNode):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += "# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += "#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            # TODO: Do some cashing here
            self.program_code += f"{variable}.set_default_speed(int({self.visit(node.value)}))  # Note: This methods expects an integer so wee need to convert the value.\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_motor_speed_node_variable_ports(self, node: SetMotorSpeedNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += """# Note: Since the content of the variable can't always be inferred at the time of the conversion
#   this code is needed. This will turn the motors after each other rather than at the same time.
#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += f"\tMotor(port).set_default_speed(int({self.visit(node.value)}))  # Note: This methods expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_set_motor_speed_node(self, node: SetMotorSpeedNode):
        if isinstance(node.ports, ListLiteralNode):
            self.visit_motor_speed_node_fixed_ports(node)
        elif isinstance(node.ports, VariableNode):
            self.visit_motor_speed_node_variable_ports(node)
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.ports}"
            )

    def visit_motor_speed_node(self, node: MotorSpeedNode):
        if not isinstance(node.port, ListLiteralNode) or len(node.port.value) != 1:
            raise NotImplementedError(
                f"An error occurred when trying to construct code for {node}, {node.port} can not be used here."
            )

        # Generate the object to call the method on
        variable = f"motor_{node.port.value[0].lower()}"
        self.generate_object(variable, "Motor", f"'{node.port.value[0]}'")

        return f"{variable}.get_speed()"

    def visit_motor_position_node(self, node: MotorPositionNode):
        if not isinstance(node.port, ListLiteralNode) or len(node.port.value) != 1:
            raise NotImplementedError(
                f"An error occurred when trying to construct code for {node}, {node.port} can not be used here."
            )

        # Generate the object to call the method on
        variable = f"motor_{node.port.value[0].lower()}"
        self.generate_object(variable, "Motor", f"'{node.port.value[0]}'")

        return f"{variable}.get_position()"

    def visit_change_variable_by_node(self, node: ChangeVariableByNode):
        self.program_code += f"{node.variable} += {self.visit(node.value)}\n"
        self.visit(node.next)

    def visit_literal_node(self, node: LiteralNode):
        return f"'{node.value}'"

    def visit_add_item_to_list_node(self, node: AddItemToListNode):
        variable = node.variable
        if variable not in self.objects:
            self.objects.add(variable)
            self.objects_code += f"{variable} = []\n"

        self.program_code += f"{variable}.append({self.visit(node.value)})\n"
        self.visit(node.next)
