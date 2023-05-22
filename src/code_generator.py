from src.abstract_syntax_tree import AST, CommentNode, LiteralNode, Node, NumericalNode
from src.abstract_syntax_tree.control import (
    ForeverLoopNode,
    IfElseNode,
    IfThenNode,
    RepeatLoopNode,
    RepeatUntilNode,
    WaitForSecondsNode,
    WaitUntilNode,
)
from src.abstract_syntax_tree.events import WhenProgramStartsNode
from src.abstract_syntax_tree.light import (
    LightUpDistanceSensorNode,
    SetCenterButtonNode,
    SetPixelBrightnessNode,
    SetPixelNode,
    TurnOffPixelsNode,
    TurnOnForDurationNode,
    TurnOnNode,
    WriteNode,
)
from src.abstract_syntax_tree.motors import (
    MotorGoToPositionNode,
    MotorPositionNode,
    MotorSpeedNode,
    RunMotorForDurationNode,
    SetMotorSpeedNode,
    StartMotorNode,
    StopMotorNode,
    TurnDirection,
)
from src.abstract_syntax_tree.movement import (
    MoveForDurationNode,
    MovementDirection,
    MoveWithSteeringNode,
    SetMotorRotationNode,
    SetMovementMotorsNode,
    SetMovementSpeedNode,
    StartMovingWithSteering,
    StopMovingNode,
)
from src.abstract_syntax_tree.operators import (
    ArithmeticalNode,
    BinaryMathFunctionNode,
    ComparisonNode,
    IsBetweenNode,
    JoinStringsNode,
    LengthOfStringNode,
    LetterOfStringNode,
    ModNode,
    NotNode,
    PickRandomNumberNode,
    RoundNode,
    StringContainsNode,
    UnaryMathFunctionNode,
)
from src.abstract_syntax_tree.sensors import (
    ColorNode,
    DistanceNode,
    GestureNode,
    HubAngleNode,
    HubInteractionNode,
    IsButtonPressedNode,
    IsColorNode,
    IsDistanceNode,
    IsKeyPressedNode,
    IsOrientationNode,
    IsReflectionNode,
    OrientationNode,
    ReflectedLightNode,
    ResetTimerNode,
    SetYawAngleNode,
    TimerNode,
)
from src.abstract_syntax_tree.sound import (
    ChangeVolumeNode,
    PlayBeepNode,
    PlaySoundUntilDoneNode,
    SetVolumeNode,
    StartBeepNode,
    StartSoundNode,
    StopBeepNode,
    VolumeNode,
)
from src.abstract_syntax_tree.variables import (
    AddItemToListNode,
    ChangeVariableByNode,
    DeleteAllItemsInListNode,
    DeleteItemInListNode,
    IndexOfItemNode,
    InsertItemAtIndexNode,
    ItemAtIndexNode,
    LengthOfListNode,
    ListContainsNode,
    ListLiteralNode,
    ReplaceItemAtIndexNode,
    SetVariableToNode,
    VariableNode,
)


class CodeGenerator:
    def __init__(self, safe=False):
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
        self.functions = set()

        self.objects_code = ""
        self.functions_code = ""
        self.program_code = ""

        self.indentation = ""

        # Indicates wether safe code should be generated which might be a bit more verbose
        self.safe_flag = safe

    def generate(self, ast: AST) -> str:
        # TODO: This will need to be changed later to support multiple block-states

        if len(ast.hat_nodes):  # Check if not empty
            self.visit(ast.hat_nodes[0])

        # Return the complete code
        if len(self.functions_code):
            return f"""{self.includes}
# Create your objects here.
{self.objects_code}
# Declare you functions here.
{self.functions_code}
# Write your program here.
{self.program_code}
"""
        else:
            return f"""{self.includes}
# Create your objects here.
{self.objects_code}
# Write your program here.
{self.program_code}
"""

    # flake8: noqa: C901
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
        elif isinstance(node, SetMovementMotorsNode):
            return self.visit_set_movement_motors_node(node)
        elif isinstance(node, MoveForDurationNode):
            return self.visit_move_for_duration_node(node)
        elif isinstance(node, MoveWithSteeringNode):
            return self.visit_move_with_steering_node(node)
        elif isinstance(node, StartMovingWithSteering):
            return self.visit_start_moving_with_steering_node(node)
        elif isinstance(node, StopMovingNode):
            return self.visit_stop_moving_node(node)
        elif isinstance(node, SetMovementSpeedNode):
            return self.visit_set_movement_speed_node(node)
        elif isinstance(node, SetMotorRotationNode):
            return self.visit_set_motor_rotation_node(node)
        elif isinstance(node, CommentNode):
            return self.visit_comment_node(node)
        elif isinstance(node, TurnOnForDurationNode):
            self.visit_turn_on_for_duration_node(node)
        elif isinstance(node, TurnOnNode):
            return self.visit_turn_on_node(node)
        elif isinstance(node, WriteNode):
            return self.visit_write_node(node)
        elif isinstance(node, TurnOffPixelsNode):
            return self.visit_turn_off_pixels_node(node)
        elif isinstance(node, SetPixelBrightnessNode):
            return self.visit_set_pixel_brightness_node(node)
        elif isinstance(node, SetPixelNode):
            return self.visit_set_pixel_node(node)
        elif isinstance(node, SetCenterButtonNode):
            return self.visit_set_center_button_node(node)
        elif isinstance(node, LightUpDistanceSensorNode):
            return self.visit_light_up_distance_sensor_node(node)
        elif isinstance(node, DeleteItemInListNode):
            return self.visit_delete_item_in_list_node(node)
        elif isinstance(node, DeleteAllItemsInListNode):
            return self.visit_delete_all_items_in_list_node(node)
        elif isinstance(node, LengthOfListNode):
            return self.visit_length_of_list_node(node)
        elif isinstance(node, InsertItemAtIndexNode):
            return self.visit_insert_item_at_index_node(node)
        elif isinstance(node, ItemAtIndexNode):
            return self.visit_item_at_index_node(node)
        elif isinstance(node, ReplaceItemAtIndexNode):
            return self.visit_replace_item_at_index_node(node)
        elif isinstance(node, IndexOfItemNode):
            return self.visit_index_of_item_node(node)
        elif isinstance(node, IfThenNode):
            return self.visit_if_then_node(node)
        elif isinstance(node, ListContainsNode):
            return self.visit_list_contains_node(node)
        elif isinstance(node, PickRandomNumberNode):
            return self.visit_pick_random_number_node(node)
        elif isinstance(node, ComparisonNode):
            return self.visit_comparison_node(node)
        elif isinstance(node, NotNode):
            return self.visit_not_node(node)
        elif isinstance(node, IsBetweenNode):
            return self.visit_is_between_node(node)
        elif isinstance(node, JoinStringsNode):
            return self.visit_join_strings_node(node)
        elif isinstance(node, LetterOfStringNode):
            return self.visit_letter_of_string_node(node)
        elif isinstance(node, LengthOfStringNode):
            return self.visit_length_of_string_node(node)
        elif isinstance(node, StringContainsNode):
            return self.visit_string_contains_node(node)
        elif isinstance(node, ModNode):
            return self.visit_mod_node(node)
        elif isinstance(node, RoundNode):
            return self.visit_round_node(node)
        elif isinstance(node, UnaryMathFunctionNode):
            return self.visit_unary_math_function_node(node)
        elif isinstance(node, BinaryMathFunctionNode):
            return self.visit_binary_math_function_node(node)
        elif isinstance(node, WaitForSecondsNode):
            return self.visit_wait_for_seconds_node(node)
        elif isinstance(node, WaitUntilNode):
            return self.visit_wait_until_node(node)
        elif isinstance(node, HubInteractionNode):
            return self.visit_hub_interaction_node(node)
        elif isinstance(node, RepeatLoopNode):
            return self.visit_repeat_loop_node(node)
        elif isinstance(node, ForeverLoopNode):
            return self.visit_forever_loop_node(node)
        elif isinstance(node, RepeatUntilNode):
            return self.visit_repeat_until_node(node)
        elif isinstance(node, IfElseNode):
            return self.visit_if_else_node(node)
        elif isinstance(node, IsColorNode):
            return self.visit_is_color_node(node)
        elif isinstance(node, ColorNode):
            return self.visit_color_node(node)
        elif isinstance(node, IsReflectionNode):
            return self.visit_is_reflection_node(node)
        elif isinstance(node, ReflectedLightNode):
            return self.visit_reflected_light_node(node)
        elif isinstance(node, IsDistanceNode):
            return self.visit_is_distance_node(node)
        elif isinstance(node, DistanceNode):
            return self.visit_distance_node(node)
        elif isinstance(node, GestureNode):
            return self.visit_gesture_node(node)
        elif isinstance(node, IsOrientationNode):
            return self.visit_is_orientation_node(node)
        elif isinstance(node, OrientationNode):
            return self.visit_orientation_node(node)
        elif isinstance(node, SetYawAngleNode):
            return self.visit_set_yaw_angle_node(node)
        elif isinstance(node, IsButtonPressedNode):
            return self.visit_is_button_pressed_node(node)
        elif isinstance(node, HubAngleNode):
            return self.visit_hub_angle_node(node)
        elif isinstance(node, TimerNode):
            return self.visit_timer_node(node)
        elif isinstance(node, ResetTimerNode):
            return self.visit_reset_timer_node(node)
        elif isinstance(node, IsKeyPressedNode):
            return self.visit_is_key_pressed_node(node)
        elif isinstance(node, PlaySoundUntilDoneNode):
            return self.visit_play_sound_until_done_node(node)
        elif isinstance(node, StartSoundNode):
            return self.visit_start_sound_node(node)
        elif isinstance(node, PlayBeepNode):
            return self.visit_play_beep_node(node)
        elif isinstance(node, StartBeepNode):
            return self.visit_start_beep_node(node)
        elif isinstance(node, StopBeepNode):
            return self.visit_stop_beep_node(node)
        elif isinstance(node, ChangeVolumeNode):
            return self.visit_change_volume_node(node)
        elif isinstance(node, SetVolumeNode):
            return self.visit_set_volume_node(node)
        elif isinstance(node, VolumeNode):
            return self.visit_volume_node(node)
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
            self.program_code += f"{self.indentation}# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += f"{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

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
                self.program_code += f"{self.indentation}{variable}.run_for_degrees(int({value_code}))  # Note: This method expects an integer so wee need to convert the value.\n"
            else:
                self.program_code += (
                    f"{variable}.run_for_{node.unit.code()}({value_code})\n"
                )

        self.visit(node.next)

    def visit_run_motor_tor_duration_node_variable_ports(
        self, node: RunMotorForDurationNode
    ):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += f"""{self.indentation}# Note: Since the content of the variable can't always be inferred at the time of the conversion
{self.indentation}#   this code is needed. This will turn the motors after each other rather than at the same time.
{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"{self.indentation}for port in {node.ports.name}:\n"

        # If the direction is counter wise negate the value
        value_code = self.visit(node.value)
        if node.direction == TurnDirection.COUNTERCLOCKWISE:
            value_code = f"-{value_code}"

        if node.unit.code() == "degrees":
            self.program_code += f"{self.indentation}\tMotor(port).run_for_degrees(int({value_code}))  # Note: This method expects an integer so wee need to convert the value.\n"
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
        self.program_code += (
            f"{self.indentation}{node.variable} = {self.visit(node.value)}\n"
        )
        self.visit(node.next)

    def visit_variable_node(self, node: VariableNode):
        # TODO: Need to check how multiple variables are handled in a program. If that causes issue use the id here rather than the name (since the id is unique)
        # TODO: Might want to make the object here as well
        return node.name

    def visit_motor_got_to_position_node_fixed_ports(self, node: MotorGoToPositionNode):
        # Print a note if there are multiple ports that should run.
        if len(node.ports.value) > 1:
            self.program_code += f"{self.indentation}# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += f"{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            # If the direction is counter wise negate the value
            value_code = self.visit(node.value)
            if node.direction == TurnDirection.COUNTERCLOCKWISE:
                value_code = f"-{value_code}"

            # Add the code and keep exploring
            self.program_code += f"{self.indentation}{variable}.run_to_position(int({value_code}), '{node.direction.code()}')  # Note: This method expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_motor_got_to_position_node_variable_ports(
        self, node: MotorGoToPositionNode
    ):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += f"""{self.indentation}# Note: Since the content of the variable can't always be inferred at the time of the conversion
{self.indentation}#   this code is needed. This will turn the motors after each other rather than at the same time.
{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"{self.indentation}for port in {node.ports.name}:\n"

        # If the direction is counter wise negate the value
        value_code = self.visit(node.value)
        if node.direction == TurnDirection.COUNTERCLOCKWISE:
            value_code = f"-{value_code}"

        # Add the code and keep exploring
        self.program_code += f"{self.indentation}\tMotor(port).run_to_position(int({value_code}), '{node.direction.code()}')  # Note: This method expects an integer so wee need to convert the value.\n"
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
            self.program_code += f"{self.indentation}# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += f"{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            if node.direction == TurnDirection.COUNTERCLOCKWISE:
                self.program_code += (
                    f"{variable}.start(-{variable}.get_default_speed())\n"
                )
            else:
                self.program_code += f"{self.indentation}{variable}.start()\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_start_motor_node_variable_ports(self, node: StartMotorNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += f"""{self.indentation}# Note: Since the content of the variable can't always be inferred at the time of the conversion
{self.indentation}#   this code is needed. This will turn the motors after each other rather than at the same time.
{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"{self.indentation}for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += f"{self.indentation}\tMotor(port).start()\n"
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
            self.program_code += f"{self.indentation}# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += f"{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            self.program_code += f"{self.indentation}{variable}.stop()\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_stop_motor_node_variable_ports(self, node: StopMotorNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += f"""{self.indentation}# Note: Since the content of the variable can't always be inferred at the time of the conversion
{self.indentation}#   this code is needed. This will turn the motors after each other rather than at the same time.
{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"{self.indentation}for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += f"{self.indentation}\tMotor(port).stop()\n"
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
            self.program_code += f"{self.indentation}# Note: This will turn the motors after each other rather than at the same time.\n"
            self.program_code += f"{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.\n"

        for port in node.ports.value:
            # Generate the object to call the method on
            variable = f"motor_{port.lower()}"
            self.generate_object(variable, "Motor", f"'{port}'")

            self.program_code += f"{self.indentation}{variable}.set_default_speed(int({self.visit(node.value)}))  # Note: This method expects an integer so wee need to convert the value.\n"
            self.visit(node.next)

        self.visit(node.next)

    def visit_motor_speed_node_variable_ports(self, node: SetMotorSpeedNode):
        # Print a note as to why this code is needed and what it is doing
        self.program_code += f"""{self.indentation}# Note: Since the content of the variable can't always be inferred at the time of the conversion
{self.indentation}#   this code is needed. This will turn the motors after each other rather than at the same time.
{self.indentation}#   This is because there is no way to turn multiple Motors at the same time in Python.
"""
        self.program_code += f"{self.indentation}for port in {node.ports.name}:\n"

        # Add the code and keep exploring
        self.program_code += f"{self.indentation}\tMotor(port).set_default_speed(int({self.visit(node.value)}))  # Note: This method expects an integer so wee need to convert the value.\n"
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
        if isinstance(node.port, ListLiteralNode):
            # Generate the object to call the method on
            variable = f"motor_{node.port.value[0].lower()}"
            self.generate_object(variable, "Motor", f"'{node.port.value[0]}'")
            return f"{variable}.get_speed()"
        elif isinstance(node.port, VariableNode):
            if self.safe_flag:
                return f"(Motor({node.port.name}[0].upper()).get_speed() if (len({node.port.name}) > 0 and {node.port.name}[0].lower() in 'abcdef') else  0)"
            else:
                return f"Motor({node.port.name}[0]).get_speed()"
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.port}"
            )

    def visit_motor_position_node(self, node: MotorPositionNode):
        if isinstance(node.port, ListLiteralNode):
            # Generate the object to call the method on
            variable = f"motor_{node.port.value[0].lower()}"
            self.generate_object(variable, "Motor", f"'{node.port.value[0]}'")
            return f"{variable}.get_position()"
        elif isinstance(node.port, VariableNode):
            if self.safe_flag:
                return f"(Motor({node.port.name}[0].upper()).get_position() if (len({node.port.name}) > 0 and {node.port.name}[0].lower() in 'abcdef') else  0)"
            else:
                return f"Motor({node.port.name}[0]).get_position()"
        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.port}"
            )

    def visit_change_variable_by_node(self, node: ChangeVariableByNode):
        self.program_code += (
            f"{self.indentation}{node.variable} += {self.visit(node.value)}\n"
        )
        self.visit(node.next)

    def visit_literal_node(self, node: LiteralNode):
        return f"'{node.value}'"

    def visit_add_item_to_list_node(self, node: AddItemToListNode):
        variable = node.variable
        if variable not in self.objects:
            self.objects.add(variable)
            self.objects_code += f"{variable} = []\n"

        self.program_code += (
            f"{self.indentation}{variable}.append({self.visit(node.value)})\n"
        )
        self.visit(node.next)

    def visit_set_movement_motors_node(self, node: SetMovementMotorsNode):
        if isinstance(node.ports, ListLiteralNode):
            self.program_code += f"{self.indentation}motor_pair = MotorPair('{node.ports.value[0]}', '{node.ports.value[1]}')\n"
        else:
            ports = self.visit(node.ports)
            self.program_code += f"{self.indentation}# Note: This will fail if the first two items in {ports} are not valid ports.\n"
            self.program_code += (
                f"{self.indentation}motor_pair = MotorPair({ports}[0], {ports}[1])\n"
            )

        self.program_code += f"{self.indentation}motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.\n"
        self.visit(node.next)

    def visit_move_for_duration_node(self, node: MoveForDurationNode):
        value = self.visit(node.value)
        if node.direction == MovementDirection.CLOCKWISE:
            self.program_code += (
                f"motor_pair.move({value}, '{node.unit.code()}', 100)\n"
            )
        elif node.direction == MovementDirection.COUNTERCLOCKWISE:
            self.program_code += (
                f"motor_pair.move({value}, '{node.unit.code()}', -100)\n"
            )
        else:
            if node.direction == MovementDirection.BACK:
                value = f"-{value}"
            self.program_code += (
                f"{self.indentation}motor_pair.move({value}, '{node.unit.code()}')\n"
            )

        self.visit(node.next)

    def visit_move_with_steering_node(self, node: MoveWithSteeringNode):
        self.program_code += f"{self.indentation}motor_pair.move({self.visit(node.value)}, '{node.unit.code()}', int({self.visit(node.steering)}))  # Note: This method expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_start_moving_with_steering_node(self, node: SetMotorSpeedNode):
        self.program_code += f"{self.indentation}motor_pair.start(int({self.visit(node.steering)}))  # Note: This method expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_stop_moving_node(self, node: StopMovingNode):
        self.program_code += f"{self.indentation}motor_pair.stop()\n"
        self.visit(node.next)

    def visit_set_movement_speed_node(self, node: SetMovementSpeedNode):
        self.program_code += f"{self.indentation}motor_pair.set_default_speed(int({self.visit(node.value)}))  # Note: This method expects an integer so wee need to convert the value.\n"
        self.visit(node.next)

    def visit_set_motor_rotation_node(self, node: SetMotorRotationNode):
        self.program_code += f"{self.indentation}motor_pair.set_motor_rotation({self.visit(node.value)}, '{node.unit.code()}')\n"
        self.visit(node.next)

    def visit_comment_node(self, node: CommentNode):
        self.program_code += f"{self.indentation}{node.value}\n"
        self.visit(node.next)

    def visit_set_center_button_node(self, node: SetCenterButtonNode):
        self.generate_object("hub", "MSHub", "")

        self.program_code += (
            f"{self.indentation}hub.status_light.on('{node.color.code()}')\n"
        )
        self.visit(node.next)

    def visit_light_up_distance_sensor_node(self, node: LightUpDistanceSensorNode):
        pattern = ", ".join(node.pattern.split(" "))

        if isinstance(node.port, ListLiteralNode):
            # Generate the object to call the method on
            variable = f"distance_sensor_{node.port.value[0].lower()}"
            self.generate_object(variable, "DistanceSensor", f"'{node.port.value[0]}'")
            self.program_code += f"{self.indentation}{variable}.light_up({pattern})\n"

        elif isinstance(node.port, VariableNode):
            port = self.visit(node.port)
            self.program_code += f"{self.indentation}# Note: This will fail if the first item in {port} is not valid port.\n"
            self.program_code += (
                f"DistanceSensor({node.port.name}[0].upper()).light_up({pattern})\n"
            )

        else:
            raise NotImplementedError(
                f"The following node is not currently supported in the port field: {node.port}"
            )
        self.visit(node.next)

    def visit_write_node(self, node: WriteNode):
        self.generate_object("hub", "MSHub", "")

        self.program_code += (
            f"{self.indentation}hub.light_matrix.write({self.visit(node.text)})\n"
        )
        self.visit(node.next)

    def visit_turn_off_pixels_node(self, node: TurnOffPixelsNode):
        self.generate_object("hub", "MSHub", "")

        self.program_code += f"{self.indentation}hub.light_matrix.off()\n"
        self.visit(node.next)

    def visit_set_pixel_node(self, node: SetPixelNode):
        self.generate_object("hub", "MSHub", "")

        self.program_code += f"{self.indentation}hub.light_matrix.set_pixel(int({self.visit(node.x)})-1, int({self.visit(node.y)})-1, int({self.visit(node.brightness)}))  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.\n"
        self.visit(node.next)

    def visit_set_pixel_brightness_node(self, node: SetPixelBrightnessNode):
        self.objects.add("_brightness")
        self.program_code += (
            f"{self.indentation}_brightness = {self.visit(node.brightness)}\n"
        )
        self.visit(node.next)

    def visit_turn_on_node(self, node: TurnOnNode):
        self.generate_object("hub", "MSHub", "")

        # If the function is not yet added add it
        if "_turn_on_pattern" not in self.functions:
            self.functions.add("_turn_on_pattern")
            self.functions_code += """# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))
"""

        if "_brightness" in self.objects:
            self.program_code += (
                f"{self.indentation}_turn_on_pattern('{node.image}', _brightness)\n"
            )
        else:
            self.program_code += f"{self.indentation}_turn_on_pattern('{node.image}')\n"

        self.visit(node.next)

    def visit_turn_on_for_duration_node(self, node: TurnOnForDurationNode):
        self.generate_object("hub", "MSHub", "")

        # If the function is not yet added add it
        if "_turn_on_pattern" not in self.functions:
            self.functions.add("_turn_on_pattern")
            self.functions_code += """# This is a helper function that is necessary to turn on patterns on the light matrix.
def _turn_on_pattern(pattern, brightness=100):
\tfor i in range(len(pattern)):
\t\thub.light_matrix.set_pixel(i%5, int(i/5), int(brightness * int(pattern[i])/9.0))
"""

        if "_brightness" in self.objects:
            self.program_code += (
                f"{self.indentation}_turn_on_pattern('{node.image}', _brightness)\n"
            )
        else:
            self.program_code += f"{self.indentation}_turn_on_pattern('{node.image}')\n"

        self.program_code += (
            f"{self.indentation}wait_for_seconds(int({self.visit(node.duration)}))\n"
        )
        self.program_code += f"{self.indentation}hub.light_matrix.off()\n"
        self.visit(node.next)

    def visit_delete_item_in_list_node(self, node: DeleteItemInListNode):
        self.program_code += f"{self.indentation}del {node.list}[int({self.visit(node.index)}) - 1]  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.\n"
        self.visit(node.next)

    def visit_delete_all_items_in_list_node(self, node: DeleteAllItemsInListNode):
        self.program_code += f"{self.indentation}{node.list}.clear()\n"
        self.visit(node.next)

    def visit_length_of_list_node(self, node: LengthOfListNode):
        return f"len({node.variable})"

    def visit_insert_item_at_index_node(self, node: InsertItemAtIndexNode):
        self.program_code += f"{self.indentation}{node.variable}.insert(int({self.visit(node.index)}) - 1, {self.visit(node.value)})  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.\n"
        self.visit(node.next)

    def visit_item_at_index_node(self, node: ItemAtIndexNode):
        return f"{node.variable}[int({self.visit(node.index)}) - 1]"

    def visit_replace_item_at_index_node(self, node: ReplaceItemAtIndexNode):
        self.program_code += f"{self.indentation}{node.variable}[int({self.visit(node.index)}) - 1] = {self.visit(node.value)}  # Note: This method expects integers so wee need to convert the value. Also starts with 0 not 1.\n"
        self.visit(node.next)

    def visit_index_of_item_node(self, node: IndexOfItemNode):
        return f"{node.variable}.index({self.visit(node.value)}) + 1"

    def visit_if_then_node(self, node: IfThenNode):
        self.program_code += f"{self.indentation}if {self.visit(node.condition)}:\n"
        self.indentation += "\t"
        self.visit(node.body)
        self.indentation[:-1]
        self.visit(node.next)

    def visit_list_contains_node(self, node: ListContainsNode):
        return f"{self.visit(node.value)} in {node.variable}"

    def visit_pick_random_number_node(self, node: PickRandomNumberNode):
        if not "from random import randint" in self.includes:
            self.includes += "from random import randint\n"
        return f"randint(int({self.visit(node.left_hand)}), int({self.visit(node.right_hand)}))"

    def visit_comparison_node(self, node: ComparisonNode):
        return f"({self.visit(node.left_hand)} {node.op.code()} {self.visit(node.right_hand)})"

    def visit_not_node(self, node: NotNode):
        return f"not {self.visit(node.left_hand)}"

    def visit_is_between_node(self, node: IsBetweenNode):
        return f"{self.visit(node.left_hand)} <= {self.visit(node.value)} <= {self.visit(node.right_hand)}"

    def visit_join_strings_node(self, node: JoinStringsNode):
        return f"{self.visit(node.left_hand)} + {self.visit(node.right_hand)}"

    def visit_letter_of_string_node(self, node: LetterOfStringNode):
        return f"{self.visit(node.right_hand)}[int({self.visit(node.left_hand)}) - 1]"

    def visit_length_of_string_node(self, node: LengthOfStringNode):
        return f"len({self.visit(node.left_hand)})"

    def visit_string_contains_node(self, node: StringContainsNode):
        return f"{self.visit(node.right_hand)} in {self.visit(node.left_hand)}"

    def visit_mod_node(self, node: ModNode):
        return f"{self.visit(node.left_hand)} % {self.visit(node.right_hand)}"

    def visit_round_node(self, node: RoundNode):
        return f"int({self.visit(node.left_hand)} + 0.5)"

    def visit_unary_math_function_node(self, node: UnaryMathFunctionNode):
        return f"{node.function.code()}{self.visit(node.left_hand)})"

    def visit_binary_math_function_node(self, node: BinaryMathFunctionNode):
        return f"{node.function.code()}({self.visit(node.left_hand)}, {self.visit(node.right_hand)})"

    def visit_wait_for_seconds_node(self, node: WaitForSecondsNode):
        self.program_code += (
            f"{self.indentation}wait_for_seconds({self.visit(node.seconds)})\n"
        )
        self.visit(node.next)

    def visit_wait_until_node(self, node: WaitUntilNode):
        self.program_code += (
            f"{self.indentation}wait_until(lambda: {self.visit(node.condition)})\n"
        )
        self.visit(node.next)

    def visit_hub_interaction_node(self, node: HubInteractionNode):
        self.generate_object("hub", "MSHub", "")
        return f"hub.motion_sensor.get_gesture() == '{node.interaction.code()}'"

    def visit_repeat_loop_node(self, node: RepeatLoopNode):
        self.program_code += (
            f"{self.indentation}for _ in range({self.visit(node.times)}):\n"
        )
        self.indentation += "\t"
        self.visit(node.body)
        self.indentation = self.indentation[:-1]
        self.visit(node.next)

    def visit_forever_loop_node(self, node: ForeverLoopNode):
        self.program_code += f"{self.indentation}while True:\n"
        self.indentation += "\t"
        self.visit(node.body)
        self.indentation = self.indentation[:-1]
        self.visit(node.next)

    def visit_repeat_until_node(self, node: RepeatUntilNode):
        self.program_code += (
            f"{self.indentation}while not ({self.visit(node.condition)}):\n"
        )
        self.indentation += "\t"
        self.visit(node.body)
        self.indentation = self.indentation[:-1]
        self.visit(node.next)

    def visit_if_else_node(self, node: IfElseNode):
        self.program_code += f"{self.indentation}if {self.visit(node.condition)}:\n"
        self.indentation += "\t"
        self.visit(node.body)
        self.indentation = self.indentation[:-1]
        self.program_code += f"{self.indentation}else:\n"
        self.indentation += "\t"
        self.visit(node.else_body)
        self.indentation = self.indentation[:-1]
        self.visit(node.next)

    def visit_is_color_node(self, node: IsColorNode):
        variable = f"color_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "ColorSensor", f"'{node.port.value[0]}'")
        return f"{variable}.get_color() == {node.color.code()}"

    def visit_color_node(self, node: ColorNode):
        variable = f"color_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "ColorSensor", f"'{node.port.value[0]}'")
        mapping = "{None:-1, 'black':0, 'violet':1, 'blue':3, 'cyan':4, 'green':5, 'yellow': 7, 'red':9, 'white':10}"
        return f"{mapping}[{variable}.get_color()]"

    def visit_is_reflection_node(self, node: IsReflectionNode):
        variable = f"color_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "ColorSensor", f"'{node.port.value[0]}'")
        return f"{variable}.get_reflected_light() {node.comparator.value} {self.visit(node.reflection)}"

    def visit_reflected_light_node(self, node: ReflectedLightNode):
        variable = f"color_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "ColorSensor", f"'{node.port.value[0]}'")
        return f"{variable}.get_reflected_light()"

    def visit_is_distance_node(self, node: IsDistanceNode):
        variable = f"distance_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "DistanceSensor", f"'{node.port.value[0]}'")
        return f"{variable}.get_distance_{node.unit.code()}() {node.comparator.value} {self.visit(node.distance)}"

    def visit_distance_node(self, node: DistanceNode):
        variable = f"distance_sensor_{node.port.value[0].lower()}"
        self.generate_object(variable, "DistanceSensor", f"'{node.port.value[0]}'")
        return f"{variable}.get_distance_{node.unit.code()}()"

    def visit_gesture_node(self, node: GestureNode):
        self.generate_object("hub", "MSHub", "")
        return "{None:-1, 'shaken':0, 'tapped':1, 'falling':3}[hub.motion_sensor.get_gesture()]"

    def visit_is_orientation_node(self, node: IsOrientationNode):
        self.generate_object("hub", "MSHub", "")
        return f"hub.motion_sensor.get_orientation() == '{node.orientation.value}'"

    def visit_orientation_node(self, node: OrientationNode):
        self.generate_object("hub", "MSHub", "")
        return "{'front':0, 'back':1, 'up':2, 'down':3, 'leftside':4, 'rightside':5}[hub.motion_sensor.get_orientation()]"

    def visit_set_yaw_angle_node(self, node: SetYawAngleNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += f"{self.indentation}hub.motion_sensor.reset_yaw_angle()\n"
        self.visit(node.next)

    def visit_is_button_pressed_node(self, node: IsButtonPressedNode):
        self.generate_object("hub", "MSHub", "")
        return f"hub.{node.button.value}_button.is_{node.action.value}()"

    def visit_hub_angle_node(self, node: HubAngleNode):
        self.generate_object("hub", "MSHub", "")
        return f"hub.motion_sensor.get_{node.unit.value}_angle()"

    def visit_timer_node(self, node: TimerNode):
        self.generate_object("timer", "Timer", "")
        return "timer.now()"

    def visit_reset_timer_node(self, node: ResetTimerNode):
        self.generate_object("timer", "Timer", "")
        self.program_code += f"{self.indentation}timer.reset()\n"
        self.visit(node.next)

    def visit_is_key_pressed_node(self, node: IsKeyPressedNode):
        raise DeprecationWarning(
            "Note that key pressed is not currently supported by MINDSTORMS itself."
        )

    def visit_play_sound_until_done_node(self, node: PlaySoundUntilDoneNode):
        self.generate_object("app", "App", "")
        self.program_code += f"{self.indentation}app.play_sound('{node.sound}')\n"
        self.visit(node.next)

    def visit_start_sound_node(self, node: StartSoundNode):
        self.generate_object("app", "App", "")
        self.program_code += f"{self.indentation}app.start_sound('{node.sound}')\n"
        self.visit(node.next)

    def visit_play_beep_node(self, node: PlayBeepNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += f"{self.indentation}hub.speaker.beep({self.visit(node.pitch)}, {self.visit(node.duration)})\n"
        self.visit(node.next)

    def visit_start_beep_node(self, node: StartBeepNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += (
            f"{self.indentation}hub.speaker.start_beep({self.visit(node.pitch)})\n"
        )
        self.visit(node.next)

    def visit_stop_beep_node(self, node: StopBeepNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += f"{self.indentation}hub.speaker.stop()\n"
        self.visit(node.next)

    def visit_change_volume_node(self, node: ChangeVolumeNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += f"{self.indentation}hub.speaker.set_volume(hub.speaker.get_volume() - {self.visit(node.volume)})\n"
        self.visit(node.next)

    def visit_set_volume_node(self, node: SetVolumeNode):
        self.generate_object("hub", "MSHub", "")
        self.program_code += (
            f"{self.indentation}hub.speaker.set_volume({self.visit(node.volume)})\n"
        )
        self.visit(node.next)

    def visit_volume_node(self, node: VolumeNode):
        self.generate_object("hub", "MSHub", "")
        return "hub.speaker.get_volume()"
