from json import loads

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
    CenterButtonColor,
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
    GoDirection,
    MotorGoToPositionNode,
    MotorPositionNode,
    MotorSpeedNode,
    RunMotorForDurationNode,
    SetMotorSpeedNode,
    StartMotorNode,
    StopMotorNode,
    TurnDirection,
    Unit,
)
from src.abstract_syntax_tree.movement import (
    MoveForDurationNode,
    MovementDirection,
    MovementUnit,
    MoveWithSteeringNode,
    RotationUnit,
    SetMotorRotationNode,
    SetMovementMotorsNode,
    SetMovementSpeedNode,
    StartMovingWithSteering,
    StopMovingNode,
)
from src.abstract_syntax_tree.operators import (
    ArithmeticalNode,
    BinaryFunction,
    BinaryMathFunctionNode,
    ComparisonNode,
    ComparisonOperator,
    IsBetweenNode,
    JoinStringsNode,
    LengthOfStringNode,
    LetterOfStringNode,
    ModNode,
    NotNode,
    Operation,
    PickRandomNumberNode,
    RoundNode,
    StringContainsNode,
    UnaryFunction,
    UnaryMathFunctionNode,
)
from src.abstract_syntax_tree.sensors import (
    AngleUnit,
    ButtonAction,
    ButtonType,
    ColorNode,
    DistanceComparator,
    DistanceNode,
    DistanceUnit,
    GestureNode,
    HubAngleNode,
    HubInteraction,
    HubInteractionNode,
    HubOrientation,
    IsButtonPressedNode,
    IsColorNode,
    IsDistanceNode,
    IsKeyPressedNode,
    IsOrientationNode,
    IsReflectionNode,
    OrientationNode,
    ReflectedLightNode,
    ReflectionComparator,
    ResetTimerNode,
    SensorColor,
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


class Visitor:
    """This visits CST and generates the AST while doing so."""

    ast: AST  # The AST that is being constructed
    cst: dict

    best_effort: bool  # If true then the visitor will try to continue even if it encounters a block it can't translate.
    # A comment will be added to the AST to indicate that this has happened.

    def __init__(self, best_effort) -> None:
        self.best_effort = best_effort

    def visit(self, cst: dict) -> AST:
        # TODO: Need to do something with the variables, list, broadcast and extensions
        self.ast = AST()
        self.cst = cst["blocks"]

        # Parse all the subtrees that are present in the CST
        for node in self.find_root_nodes():
            self.ast.hat_nodes.append(self.visit_node(node))

        return self.ast

    def find_root_nodes(self) -> list:
        """Find all the root notes of the subtrees present in the CST. These are the first blocks of block stacks.
        :return: List of all the root nodes.
        :rtype: list
        """
        # TODO: This will need to be more sophisticated but this works for now
        if self.cst:
            return [next(iter(self.cst))]
        else:
            return []

    # flake8: noqa: C901
    def visit_node(self, node: dict) -> Node:
        """Checks the type of the node and calls the appropriate visit function.
        :param node: The identifier of the current node (the key for the CST dict) or None
        :type node: dict
        :raises NotImplementedError: If the node is not yet supported raise an error
        :return: The AST representation of the node
        :rtype: Node
        """
        if not node:  # There is no node return None
            return None
        node = self.cst[node]

        opcode = node["opcode"]
        if opcode == "flipperevents_whenProgramStarts":
            return self.visit_when_program_starts(node)
        elif opcode == "flippermotor_motorTurnForDirection":
            return self.visit_run_motor_for_duration(node)
        elif opcode == "flippermotor_motorGoDirectionToPosition":
            return self.visit_motor_go_to_position(node)
        elif opcode == "flippermotor_custom-angle":
            return self.visit_motor_custom_angle(node)
        elif opcode == "flippermotor_motorStartDirection":
            return self.visit_start_motor(node)
        elif opcode == "flippermotor_motorStop":
            return self.visit_stop_motor(node)
        elif opcode == "flippermotor_motorSetSpeed":
            return self.visit_set_motor_speed(node)
        elif opcode == "flippermotor_absolutePosition":
            return self.visit_motor_position(node)
        elif opcode == "flippermotor_speed":
            return self.visit_motor_speed(node)
        elif opcode == "flippermove_setMovementPair":
            return self.visit_set_movement_motors(node)
        elif opcode == "flippermove_move":
            return self.visit_move_for_duration(node)
        elif opcode == "flippermove_steer":
            return self.visit_move_with_steering(node)
        elif opcode == "flippermove_rotation-wheel":
            return self.visit_move_rotation_wheel(node)
        elif opcode == "flippermove_startSteer":
            return self.visit_start_moving_with_steering(node)
        elif opcode == "flippermove_stopMove":
            return self.visit_stop_moving(node)
        elif opcode == "flippermove_movementSpeed":
            return self.visit_set_movement_speed(node)
        elif opcode == "flippermove_setDistance":
            return self.visit_set_motor_rotation(node)
        elif opcode == "flipperdisplay_ledAnimation":
            return self.visit_start_animation(node)
        elif opcode == "flipperdisplay_ledAnimationUntilDone":
            return self.visit_play_animation_until_done(node)
        elif opcode == "flipperdisplay_ledImageFor":
            return self.visit_turn_on_for_duration(node)
        elif opcode == "flipperdisplay_ledImage":
            return self.visit_turn_on(node)
        elif opcode == "flipperdisplay_ledText":
            return self.visit_write(node)
        elif opcode == "flipperdisplay_displayOff":
            return self.visit_turn_off_pixels(node)
        elif opcode == "flipperdisplay_ledSetBrightness":
            return self.visit_set_pixel_brightness(node)
        elif opcode == "flipperdisplay_ledOn":
            return self.visit_set_pixel(node)
        elif opcode == "flipperdisplay_menu_ledMatrixIndex":
            return self.visit_set_pixel_matrix_index(node)
        elif opcode == "flipperdisplay_ledRotateDirection":
            return self.visit_rotate_orientation(node)
        elif opcode == "flipperdisplay_ledRotateOrientation":
            return self.visit_set_orientation(node)
        elif opcode == "flipperdisplay_centerButtonLight":
            return self.visit_set_center_button(node)
        elif opcode == "flipperdisplay_ultrasonicLightUp":
            return self.visit_light_up_distance_sensor(node)
        elif opcode == "data_setvariableto":
            return self.visit_set_variable_to(node)
        elif opcode == "data_changevariableby":
            return self.visits_change_variable_by(node)
        elif opcode == "data_addtolist":
            return self.visit_add_to_list(node)
        elif opcode == "data_deleteoflist":
            return self.visit_delete_item_in_list(node)
        elif opcode == "data_deletealloflist":
            return self.visit_delete_all_items_in_list(node)
        elif opcode == "data_lengthoflist":
            return self.visit_length_of_list(node)
        elif opcode == "data_insertatlist":
            return self.visit_insert_at_index(node)
        elif opcode == "data_itemoflist":
            return self.visit_item_at_index(node)
        elif opcode == "data_replaceitemoflist":
            return self.visit_replace_item_at_index(node)
        elif opcode == "data_itemnumoflist":
            return self.visit_index_of_item(node)
        elif opcode == "data_listcontainsitem":
            return self.visit_list_contains_item(node)
        elif opcode == "control_if":
            return self.visit_if_then(node)
        elif opcode == "control_wait":
            return self.visit_for_seconds(node)
        elif opcode == "control_wait_until":
            return self.visit_wait_until(node)
        elif opcode == "control_repeat":
            return self.visit_repeat_loop(node)
        elif opcode == "control_forever":
            return self.visit_forever_loop(node)
        elif opcode == "control_if_else":
            return self.visit_if_else(node)
        elif opcode == "control_repeat_until":
            return self.visit_repeat_until(node)
        elif opcode == "flippercontrol_fork":
            return self.visit_do_this_and_this(node)
        elif opcode == "flippercontrol_stopOtherStacks":
            return self.visit_stop_other_stacks(node)
        elif opcode == "flippercontrol_stop":
            return self.visit_stop(node)
        elif opcode == "flippersensors_color":
            return self.visit_color(node)
        elif opcode == "flippersensors_isColor":
            return self.visit_is_color(node)
        elif opcode == "flippersensors_isReflectivity":
            return self.visit_is_reflectivity(node)
        elif opcode == "flippersensors_reflectivity":
            return self.visit_reflectivity(node)
        elif opcode == "flippersensors_isDistance":
            return self.visit_is_distance(node)
        elif opcode == "flippersensors_distance":
            return self.visit_distance(node)
        elif opcode == "flippersensors_motion":
            return self.visit_gesture(node)
        elif opcode == "flippersensors_isorientation":
            return self.visit_is_orientation(node)
        elif opcode == "flippersensors_orientation":
            return self.visit_orientation(node)
        elif opcode == "flippersensors_resetYaw":
            return self.visit_reset_yaw(node)
        elif opcode == "flippersensors_buttonIsPressed":
            return self.visit_is_button_pressed(node)
        elif opcode == "flippersensors_orientationAxis":
            return self.visit_hub_angle(node)
        elif opcode == "flippersensors_timer":
            return self.visit_hub_timer(node)
        elif opcode == "flippersensors_resetTimer":
            return self.visit_hub_reset_timer(node)
        elif opcode == "sensing_keypressed":
            return self.visit_key_pressed(node)
        elif opcode == "flippersensors_ismotion":
            return self.visit_hub_is_shaken(node)
        elif opcode == "operator_add":
            return self.visit_operator(Operation.PLUS, node)
        elif opcode == "operator_subtract":
            return self.visit_operator(Operation.MINUS, node)
        elif opcode == "operator_divide":
            return self.visit_operator(Operation.DIVIDE, node)
        elif opcode == "operator_multiply":
            return self.visit_operator(Operation.MULTIPLY, node)
        elif opcode == "operator_random":
            return self.visit_pick_random(node)
        elif opcode == "operator_lt":
            return self.visit_comparison(node, ComparisonOperator.LESS)
        elif opcode == "operator_equals":
            return self.visit_comparison(node, ComparisonOperator.EQUAL)
        elif opcode == "operator_gt":
            return self.visit_comparison(node, ComparisonOperator.GREATER)
        elif opcode == "operator_and":
            return self.visit_comparison(node, ComparisonOperator.AND)
        elif opcode == "operator_or":
            return self.visit_comparison(node, ComparisonOperator.OR)
        elif opcode == "operator_contains":
            return self.visit_string_contains(node)
        elif opcode == "operator_not":
            return self.visit_not_node(node)
        elif opcode == "flipperoperator_isInBetween":
            return self.visit_is_between(node)
        elif opcode == "operator_join":
            return self.visit_join_strings(node)
        elif opcode == "operator_letter_of":
            return self.visit_letter_of_string(node)
        elif opcode == "operator_length":
            return self.visit_length_of_string(node)
        elif opcode == "operator_mod":
            return self.visit_mod(node)
        elif opcode == "operator_round":
            return self.visit_round(node)
        elif opcode == "operator_mathop":
            return self.visit_unary_math_function(node)
        elif opcode == "flipperoperator_mathFunc2Params":
            return self.visit_binary_math_function(node)
        elif opcode == "flippersound_playSoundUntilDone":
            return self.visit_play_sound(node)
        elif opcode == "flippersound_playSound":
            return self.visit_start_sound(node)
        elif opcode == "flippersound_beepForTime":
            return self.visit_play_beep(node)
        elif opcode == "flippersound_custom-piano":
            return self.visit_piano_node(node)
        elif opcode == "flippersound_beep":
            return self.visit_start_beep(node)
        elif opcode == "flippersound_stopSound":
            return self.visit_stop_sound(node)
        elif opcode == "sound_setvolumeto":
            return self.visit_set_volume(node)
        elif opcode == "sound_changevolumeby":
            return self.visit_change_volume(node)
        elif opcode == "sound_volume":
            return self.visit_volume(node)
        elif opcode == "sound_changeeffectby":
            return self.visit_change_effect(node)
        elif opcode == "sound_seteffectto":
            return self.visit_set_effect(node)
        elif opcode == "sound_cleareffects":
            return self.visit_clear_effects(node)
        else:
            raise NotImplementedError(opcode)

    def visit_when_program_starts(self, node: dict) -> WhenProgramStartsNode:
        """Constructs the AST representation of the WhenProgramStarts node.
        :param node: The Node representation.
        """
        next_node = self.visit_node(node["next"])
        return WhenProgramStartsNode(node["x"], node["y"], next_node)

    def visit_run_motor_for_duration(self, node: dict) -> RunMotorForDurationNode:
        """Constructs the AST representation of the RunMotorForDuration node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_run_motor_for_duration_direction(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_run_motor_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return RunMotorForDurationNode(ports, direction, value, unit, next_node)

    def visit_run_motor_for_duration_port(self, node: dict) -> list:
        """Parses the ports that are being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: List of all the port names (single characters).
        """
        port_specifier = node["inputs"]["PORT"][1]
        if isinstance(port_specifier, list):
            return VariableNode(port_specifier[1], port_specifier[2])
        else:
            ports = self.cst[port_specifier]["fields"][
                "field_" + self.cst[port_specifier]["opcode"]
            ][0]
            return ListLiteralNode(list(ports))

    def visit_run_motor_for_duration_direction(self, node: dict) -> TurnDirection:
        """Parses the direction that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = self.cst[node["inputs"]["DIRECTION"][1]]["fields"][
            "field_flippermotor_custom-icon-direction"
        ][0]
        return TurnDirection[direction.upper()]

    def visit_run_motor_for_duration_unit(self, node: dict) -> Unit:
        """Parses the unit that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The unit that is being used.
        """
        unit = node["fields"]["UNIT"][0]
        return Unit[unit.upper()]

    def visit_input(self, val) -> Node:
        """Visits the input field of a node.
        Val can be 2 things, if it is a list, than the 2 items is a string representation of a float or an int.
        **NOTE**: If the list has 3 items it is actually a variable.
        If it is a string it is the identifier of a another node that needs to be parsed.

        :param val: Input representation.
        :type val: str or list
        :return: AST representation of the input.
        """
        if isinstance(val, list):
            if len(val) == 3:
                return VariableNode(val[1], val[2])
            else:
                try:
                    return NumericalNode(float(val[1]))
                except ValueError:
                    return LiteralNode(val[1])
        else:
            return self.visit_node(val)

    def visit_run_motor_for_duration_value(self, node: dict) -> Node:
        """Parses the value that is being used by the RunMotorForDurationNode.
        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        return self.visit_input(node["inputs"]["VALUE"][1])

    def visit_operator(self, op: Operation, node: dict) -> ArithmeticalNode:
        """Constructs the AST representation of the Arithmetics node.
        :param op: The operation of the arithmetic block
        :param node: The Node representation.
        :return: The AST representation.
        """
        left_hand = self.visit_input(node["inputs"]["NUM1"][1])
        right_hand = self.visit_input(node["inputs"]["NUM2"][1])
        return ArithmeticalNode(op, left_hand, right_hand)

    def visit_motor_go_to_position(self, node: dict) -> MotorGoToPositionNode:
        """Constructs the AST representation of the MotorGoToPosition node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_motor_go_to_position_direction(node)
        value = self.visit_motor_go_to_position_value(node)
        next_node = self.visit_node(node["next"])
        return MotorGoToPositionNode(ports, direction, value, next_node)

    def visit_motor_go_to_position_direction(self, node: dict) -> GoDirection:
        """Parse the direction used by the MotorGoToPositionNode.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = node["fields"]["DIRECTION"][0]
        return GoDirection[direction.upper()]

    def visit_motor_go_to_position_value(self, node: dict) -> Node:
        """Parse the value used by the MotorGoToPositionNode.
        :param node: The Node representation.
        :return: The value that is being used.
        """
        if len(node["inputs"]["POSITION"][1]) == 3:
            return VariableNode(
                node["inputs"]["POSITION"][1][1], node["inputs"]["POSITION"][1][2]
            )
        return self.visit_node(node["inputs"]["POSITION"][1])

    def visit_motor_custom_angle(self, node: dict) -> NumericalNode:
        """Parse the MotorCustomAngleNode.
        :param node: The Node representation.
        :return: The AST representation.
        """
        return NumericalNode(
            float(node["fields"]["field_flippermotor_custom-angle"][0])
        )

    def visit_start_motor(self, node: dict) -> StartMotorNode:
        """Constructs the AST representation of the StartMotor node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        direction = self.visit_run_motor_for_duration_direction(node)
        next_node = self.visit_node(node["next"])
        return StartMotorNode(ports, direction, next_node)

    def visit_stop_motor(self, node: dict) -> StopMotorNode:
        """Constructs the AST representation of the StopMotor node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return StopMotorNode(ports, next_node)

    def visit_set_motor_speed(self, node) -> SetMotorSpeedNode:
        """Constructs the AST representation of the SetMotorSpeed node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_run_motor_for_duration_port(node)
        value = self.visit_set_motor_speed_value(node)
        next_node = self.visit_node(node["next"])
        return SetMotorSpeedNode(ports, value, next_node)

    def visit_set_motor_speed_value(self, node: dict) -> Node:
        """Parse the value used by the SetMotorSpeedNode.
        :param node: The Node representation.
        :return: The value that is being used.
        """
        return self.visit_input(node["inputs"]["SPEED"][1])

    def visit_set_variable_to(self, node: dict) -> SetVariableToNode:
        """Constructs the AST representation of the SetVariableTo node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        # TODO: This needs to be fixed to also keep track of the variable ID and NAME
        variable = node["fields"]["VARIABLE"][0]
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return SetVariableToNode(variable, value, next_node)

    def visits_change_variable_by(self, node) -> ChangeVariableByNode:
        """Constructs the AST representation of the ChangeVariable node.
        :param node: The Node representation.
        :return: The AST representation.
        """
        # TODO: This needs to be fixed to also keep track of the variable ID and NAME
        variable = node["fields"]["VARIABLE"][0]
        value = self.visit_run_motor_for_duration_value(node)
        next_node = self.visit_node(node["next"])
        return ChangeVariableByNode(variable, value, next_node)

    def visit_add_to_list_value(self, node) -> Node:
        """Parses the value that is being used by the AddItemToList node.

        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        if len(node["inputs"]["ITEM"][1]) == 3:
            return VariableNode(
                node["inputs"]["ITEM"][1][1], node["inputs"]["ITEM"][1][2]
            )
        else:
            if isinstance(node["inputs"]["ITEM"][1], list):
                return LiteralNode(node["inputs"]["ITEM"][1][1])
            else:
                return self.visit_node(node["inputs"]["ITEM"][1])

    def visit_add_to_list(self, node) -> AddItemToListNode:
        """Constructs the AST representation of the AddItemToList node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        variable = node["fields"]["LIST"][0]
        value = self.visit_add_to_list_value(node)
        next_node = self.visit_node(node["next"])
        return AddItemToListNode(variable, value, next_node)

    def visit_motor_position(self, node) -> MotorPositionNode:
        """Constructs the AST representation of the MotorPosition node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return MotorPositionNode(port, next_node)

    def visit_motor_speed(self, node) -> MotorSpeedNode:
        """Constructs the AST representation of the MotorSpeed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        next_node = self.visit_node(node["next"])
        return MotorSpeedNode(port, next_node)

    def visit_movement_ports(self, node: dict) -> Node:
        """Parses the ports that are being used by the SetMovementMotorsNode.
        :param node: The Node representation.
        :return: List of all the port names (single characters).
        """
        port_specifier = node["inputs"]["PAIR"][1]
        if isinstance(port_specifier, list):
            return VariableNode(port_specifier[1], port_specifier[2])
        else:
            ports = self.cst[port_specifier]["fields"][
                "field_" + self.cst[port_specifier]["opcode"]
            ][0]
            return ListLiteralNode(list(ports))

    def visit_set_movement_motors(self, node) -> SetMovementMotorsNode:
        """Constructs the AST representation of the SetMovementMotors node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        ports = self.visit_movement_ports(node)
        next_node = self.visit_node(node["next"])
        return SetMovementMotorsNode(ports, next_node)

    def visit_move_for_duration_unit(self, node: dict) -> MovementUnit:
        """Parses the unit that is being used by the MoveForDuration.
        :param node: The Node representation.
        :return: The unit that is being used.
        """
        unit = node["fields"]["UNIT"][0]
        return MovementUnit[unit.upper()]

    def visit_move_for_duration_direction(self, node: dict) -> MovementDirection:
        """Parses the direction that is being used by the MoveForDuration.
        :param node: The Node representation.
        :return: The direction that is being used.
        """
        direction = self.cst[node["inputs"]["DIRECTION"][1]]["fields"][
            "field_flippermove_custom-icon-direction"
        ][0]
        return MovementDirection[direction.upper()]

    def visit_move_for_duration(self, node) -> MoveForDurationNode:
        """Constructs the AST representation of the MoveForDuration node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        direction = self.visit_move_for_duration_direction(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_move_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return MoveForDurationNode(direction, value, unit, next_node)

    def visit_move_with_steering_steering(self, node: dict) -> Node:
        """Parses the value that is being used by the MoveWithSteeringNode.
        :param node: The Node representation.
        :return: The node that that specifies the value that should be used. (Could be an entire subtree, in the case of an equation).
        """
        return self.visit_input(node["inputs"]["STEERING"][1])

    def visit_move_rotation_wheel(self, node: dict) -> Node:
        """Parses the steering that is being used by the MoveWithSteeringNode.
        :param node: The Node representation.
        :return: A NumericalNode with the value of the steering.
        """
        return NumericalNode(
            float(node["fields"]["field_flippermove_rotation-wheel"][0])
        )

    def visit_move_with_steering(self, node) -> MoveWithSteeringNode:
        """Constructs the AST representation of the MoveWithSteering node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        steering = self.visit_move_with_steering_steering(node)
        value = self.visit_run_motor_for_duration_value(node)
        unit = self.visit_move_for_duration_unit(node)
        next_node = self.visit_node(node["next"])
        return MoveWithSteeringNode(steering, value, unit, next_node)

    def visit_start_moving_with_steering(self, node) -> StartMovingWithSteering:
        """Constructs the AST representation of the StartMovingWithSteering node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        steering = self.visit_move_with_steering_steering(node)
        next_node = self.visit_node(node["next"])
        return StartMovingWithSteering(steering, next_node)

    def visit_stop_moving(self, node) -> StopMovingNode:
        """Constructs the AST representation of the StopMoving node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return StopMovingNode(next_node)

    def visit_set_movement_speed(self, node) -> SetMovementSpeedNode:
        """Constructs the AST representation of the SetMovementSpeed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        value = self.visit_input(node["inputs"]["SPEED"][1])
        next_node = self.visit_node(node["next"])
        return SetMovementSpeedNode(value, next_node)

    def visit_set_motor_rotation(self, node) -> SetMotorRotationNode:
        """Constructs the AST representation of the SetMotorRotation node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        value = self.visit_input(node["inputs"]["DISTANCE"][1])
        unit = RotationUnit[node["fields"]["UNIT"][0].upper()]
        next_node = self.visit_node(node["next"])
        return SetMotorRotationNode(value, unit, next_node)

    def visit_start_animation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that animations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Animations are not supported yet, use the best_effort flag to generate code without animations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the START ANIMATION block. Note: that animations are not supported in Python at the moment.",
            next_node,
        )

    def visit_play_animation_until_done(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that animations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Animations are not supported yet, use the best_effort flag to generate code without animations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the PLAY ANIMATION block. Note: that animations are not supported in Python at the moment.",
            next_node,
        )

    def visit_turn_on_for_duration(self, node) -> TurnOnForDurationNode:
        """Constructs the AST representation of the TurnOnForDuration node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        image = self.cst[node["inputs"]["MATRIX"][1]]["fields"][
            "field_flipperdisplay_custom-matrix"
        ][0]
        duration = self.visit_input(node["inputs"]["VALUE"][1])
        next_node = self.visit_node(node["next"])
        return TurnOnForDurationNode(image, duration, next_node)

    def visit_turn_on(self, node) -> TurnOnNode:
        """Constructs the AST representation of the TurnOn node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        image = self.cst[node["inputs"]["MATRIX"][1]]["fields"][
            "field_flipperdisplay_custom-matrix"
        ][0]
        next_node = self.visit_node(node["next"])
        return TurnOnNode(image, next_node)

    def visit_write(self, node) -> WriteNode:
        """Constructs the AST representation of the Write node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        text = self.visit_input(node["inputs"]["TEXT"][1])
        next_node = self.visit_node(node["next"])
        return WriteNode(text, next_node)

    def visit_turn_off_pixels(self, node) -> TurnOffPixelsNode:
        """Constructs the AST representation of the TurnOffPixels node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return TurnOffPixelsNode(next_node)

    def visit_set_pixel_brightness(self, node) -> SetPixelBrightnessNode:
        """Constructs the AST representation of the SetPixelBrightness node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        brightness = self.visit_input(node["inputs"]["BRIGHTNESS"][1])
        next_node = self.visit_node(node["next"])
        return SetPixelBrightnessNode(brightness, next_node)

    def visit_set_pixel_matrix_index(self, node) -> NumericalNode:
        return NumericalNode(float(node["fields"]["ledMatrixIndex"][0]))

    def visit_set_pixel(self, node) -> SetPixelNode:
        """Constructs the AST representation of the SetPixel node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        x = self.visit_input(node["inputs"]["X"][1])
        y = self.visit_input(node["inputs"]["Y"][1])
        brightness = self.visit_input(node["inputs"]["BRIGHTNESS"][1])
        next_node = self.visit_node(node["next"])
        return SetPixelNode(x, y, brightness, next_node)

    def visit_rotate_orientation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that rotations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Rotations are not supported yet, use the best_effort flag to generate code without rotations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the ROTATE ORIENTATION block. Note: that rotations are not supported in Python at the moment.",
            next_node,
        )

    def visit_set_orientation(self, node) -> CommentNode:
        """If the best effort flag is true constructs a comment node that acts as a place holder and explains that rotations are not supported yet.
        Else raise an NotImplementedError.
        :param node: The Node representation.
        :return: The AST representation.
        """
        if not self.best_effort:
            raise NotImplementedError(
                "Rotations are not supported yet, use the best_effort flag to generate code without rotations."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the SET ORIENTATION block. Note: that rotations are not supported in Python at the moment.",
            next_node,
        )

    def visit_set_center_button(self, node) -> SetCenterButtonNode:
        """Constructs the AST representation of the SetCenterButton node.

        :param node: The Node representation.
        :return: The AST representation.
        """

        color_index = int(
            self.cst[node["inputs"]["COLOR"][1]]["fields"][
                "field_flipperdisplay_color-selector-vertical"
            ][0]
        )
        color = CenterButtonColor.at(color_index)
        next_node = self.visit_node(node["next"])
        return SetCenterButtonNode(color, next_node)

    def visit_light_up_distance_sensor(self, node) -> LightUpDistanceSensorNode:
        """Constructs the AST representation of the LightUpDistanceSensor node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        pattern = self.cst[node["inputs"]["VALUE"][1]]["fields"][
            "field_flipperdisplay_led-selector"
        ][0]
        next_node = self.visit_node(node["next"])
        return LightUpDistanceSensorNode(port, pattern, next_node)

    def visit_delete_item_in_list(self, node) -> DeleteItemInListNode:
        """Constructs the AST representation of the DeleteItemInList node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        # TODO: This needs to be fixed to also keep track of the variable ID and NAME
        list = node["fields"]["LIST"][0]
        index = self.visit_input(node["inputs"]["INDEX"][1])
        next_node = self.visit_node(node["next"])
        return DeleteItemInListNode(list, index, next_node)

    def visit_delete_all_items_in_list(self, node) -> DeleteAllItemsInListNode:
        """Constructs the AST representation of the DeleteAllItemsInList node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        next_node = self.visit_node(node["next"])
        return DeleteAllItemsInListNode(list, next_node)

    def visit_length_of_list(self, node) -> LengthOfListNode:
        """Constructs the AST representation of the LengthOfList node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        return LengthOfListNode(list)

    def visit_item_at_index(self, node) -> ItemAtIndexNode:
        """Constructs the AST representation of the ItemAtIndex node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        index = self.visit_input(node["inputs"]["INDEX"][1])
        return ItemAtIndexNode(list, index)

    def visit_insert_at_index(self, node) -> InsertItemAtIndexNode:
        """Constructs the AST representation of the InsertItemAtIndex node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        item = self.visit_input(node["inputs"]["ITEM"][1])
        index = self.visit_input(node["inputs"]["INDEX"][1])
        next_node = self.visit_node(node["next"])
        return InsertItemAtIndexNode(list, item, index, next_node)

    def visit_replace_item_at_index(self, node) -> ReplaceItemAtIndexNode:
        """Constructs the AST representation of the ReplaceItemAtIndex node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        index = self.visit_input(node["inputs"]["INDEX"][1])
        item = self.visit_input(node["inputs"]["ITEM"][1])
        next_node = self.visit_node(node["next"])
        return ReplaceItemAtIndexNode(list, index, item, next_node)

    def visit_index_of_item(self, node) -> IndexOfItemNode:
        """Constructs the AST representation of the IndexOfItem node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        item = self.visit_input(node["inputs"]["ITEM"][1])
        return IndexOfItemNode(list, item)

    def visit_if_then(self, node) -> IfThenNode:
        """Constructs the AST representation of the IfThen node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        condition = self.visit_input(node["inputs"]["CONDITION"][1])
        body = self.visit_node(node["inputs"]["SUBSTACK"][1])
        next_node = self.visit_node(node["next"])
        return IfThenNode(condition, body, next_node)

    def visit_list_contains_item(self, node) -> ListContainsNode:
        """Constructs the AST representation of the ListContainsItem node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        list = node["fields"]["LIST"][0]
        item = self.visit_input(node["inputs"]["ITEM"][1])
        return ListContainsNode(list, item)

    def visit_pick_random(self, node) -> PickRandomNumberNode:
        """Constructs the AST representation of the PickRandom node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        low = self.visit_input(node["inputs"]["FROM"][1])
        high = self.visit_input(node["inputs"]["TO"][1])
        return PickRandomNumberNode(low, high)

    def visit_comparison(self, node, operator) -> ComparisonNode:
        """Constructs the AST representation of the Comparison node.

        :param node: The Node representation.
        :param operator: The operator of the comparison.
        :return: The AST representation.
        """
        left = self.visit_input(node["inputs"]["OPERAND1"][1])
        right = self.visit_input(node["inputs"]["OPERAND2"][1])
        return ComparisonNode(operator, left, right)

    def visit_not_node(self, node) -> NotNode:
        """Constructs the AST representation of the Not node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        operand = self.visit_input(node["inputs"]["OPERAND"][1])
        return NotNode(operand)

    def visit_is_between(self, node) -> IsBetweenNode:
        """Constructs the AST representation of the IsBetween node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        value = self.visit_input(node["inputs"]["VALUE"][1])
        low = self.visit_input(node["inputs"]["LOW"][1])
        high = self.visit_input(node["inputs"]["HIGH"][1])
        return IsBetweenNode(value, low, high)

    def visit_join_strings(self, node) -> JoinStringsNode:
        """Constructs the AST representation of the JoinStrings node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        string1 = self.visit_input(node["inputs"]["STRING1"][1])
        string2 = self.visit_input(node["inputs"]["STRING2"][1])
        return JoinStringsNode(string1, string2)

    def visit_letter_of_string(self, node) -> LetterOfStringNode:
        """Constructs the AST representation of the LetterOfString node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        index = self.visit_input(node["inputs"]["LETTER"][1])
        string = self.visit_input(node["inputs"]["STRING"][1])
        return LetterOfStringNode(index, string)

    def visit_length_of_string(self, node) -> LengthOfStringNode:
        """Constructs the AST representation of the LengthOfString node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        string = self.visit_input(node["inputs"]["STRING"][1])
        return LengthOfStringNode(string)

    def visit_string_contains(self, node) -> StringContainsNode:
        """Constructs the AST representation of the StringContains node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        string1 = self.visit_input(node["inputs"]["STRING1"][1])
        string2 = self.visit_input(node["inputs"]["STRING2"][1])
        return StringContainsNode(string1, string2)

    def visit_mod(self, node) -> ModNode:
        """Constructs the AST representation of the Mod node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        dividend = self.visit_input(node["inputs"]["NUM1"][1])
        divisor = self.visit_input(node["inputs"]["NUM2"][1])
        return ModNode(dividend, divisor)

    def visit_round(self, node) -> RoundNode:
        """Constructs the AST representation of the Round node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        num = self.visit_input(node["inputs"]["NUM"][1])
        return RoundNode(num)

    def visit_unary_math_function(self, node) -> UnaryMathFunctionNode:
        """Constructs the AST representation of the MathFunction node.

        :param node: The Node representation.
        :param function: The function of the UnaryMathFunction.
        :return: The AST representation.
        """
        function = UnaryFunction.parse(node["fields"]["OPERATOR"][0])
        num = self.visit_input(node["inputs"]["NUM"][1])
        return UnaryMathFunctionNode(function, num)

    def visit_binary_math_function(self, node) -> BinaryMathFunctionNode:
        """Constructs the AST representation of the MathFunction node.

        :param node: The Node representation.
        :param function: The function of the BinaryMathFunction.
        :return: The AST representation.
        """
        function = BinaryFunction.parse(node["fields"]["TYPE"][0])
        num1 = self.visit_input(node["inputs"]["ARG1"][1])
        num2 = self.visit_input(node["inputs"]["ARG2"][1])
        return BinaryMathFunctionNode(function, num1, num2)

    def visit_for_seconds(self, node) -> WaitForSecondsNode:
        """Constructs the AST representation of the WaitForSeconds node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        seconds = self.visit_input(node["inputs"]["DURATION"][1])
        next_node = self.visit_node(node["next"])
        return WaitForSecondsNode(seconds, next_node)

    def visit_wait_until(self, node) -> WaitUntilNode:
        """Constructs the AST representation of the WaitUntil node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        condition = self.visit_input(node["inputs"]["CONDITION"][1])
        next_node = self.visit_node(node["next"])
        return WaitUntilNode(condition, next_node)

    def visit_repeat_loop(self, node) -> RepeatLoopNode:
        """Constructs the AST representation of the RepeatLoop node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        times = self.visit_input(node["inputs"]["TIMES"][1])
        body = self.visit_node(node["inputs"]["SUBSTACK"][1])
        next_node = self.visit_node(node["next"])
        return RepeatLoopNode(times, body, next_node)

    def visit_forever_loop(self, node) -> ForeverLoopNode:
        """Constructs the AST representation of the ForeverLoop node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        body = self.visit_node(node["inputs"]["SUBSTACK"][1])
        next_node = self.visit_node(node["next"])
        return ForeverLoopNode(body, next_node)

    def visit_if_else(self, node) -> IfElseNode:
        """Constructs the AST representation of the IfElse node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        condition = self.visit_input(node["inputs"]["CONDITION"][1])
        body = self.visit_node(node["inputs"]["SUBSTACK"][1])
        else_body = self.visit_node(node["inputs"]["SUBSTACK2"][1])
        next_node = self.visit_node(node["next"])
        return IfElseNode(condition, body, else_body, next_node)

    def visit_repeat_until(self, node) -> RepeatUntilNode:
        """Constructs the AST representation of the RepeatUntil node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        condition = self.visit_input(node["inputs"]["CONDITION"][1])
        body = self.visit_node(node["inputs"]["SUBSTACK"][1])
        next_node = self.visit_node(node["next"])
        return RepeatUntilNode(condition, body, next_node)

    def visit_do_this_and_this(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Parallelism is not supported, use the best_effort flag to generate code without rotations."
            )
        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the DO THIS AND THIS block. Note: that parallelism is not supported in Python at the moment.",
            next_node,
        )

    def visit_stop_other_stacks(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Parallelism is not supported, use the best_effort flag to generate code without rotations."
            )
        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the STOP OTHER STACKS block. Note: that parallelism is not supported in Python at the moment.",
            next_node,
        )

    def visit_stop(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Parallelism is not supported, use the best_effort flag to generate code without rotations."
            )
        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the STOP block. Note: that parallelism is not supported in Python at the moment.",
            next_node,
        )

    def visit_hub_is_shaken(self, node) -> HubInteractionNode:
        """Constructs the AST representation of the HubInteraction node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        interaction = HubInteraction[node["fields"]["MOTION"][0].upper()]
        return HubInteractionNode(interaction)

    def visit_is_color(self, node) -> IsColorNode:
        """Constructs the AST representation of the IsColor node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        color_index = int(
            self.cst[node["inputs"]["VALUE"][1]]["fields"][
                "field_flippersensors_color-selector"
            ][0]
        )
        color = SensorColor.at(color_index)
        return IsColorNode(port, color)

    def visit_color(self, node) -> ColorNode:
        """Constructs the AST representation of the Color node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        return ColorNode(port)

    def visit_is_reflectivity(self, node) -> IsReflectionNode:
        """Constructs the AST representation of the IsReflection node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        comparator = ReflectionComparator.parse(node["fields"]["COMPARATOR"][0])
        value = self.visit_input(node["inputs"]["VALUE"][1])
        return IsReflectionNode(port, comparator, value)

    def visit_reflectivity(self, node) -> ReflectedLightNode:
        """Constructs the AST representation of the ReflectedLight node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        return ReflectedLightNode(port)

    def visit_is_distance(self, node) -> IsDistanceNode:
        """Constructs the AST representation of the IsDistance node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        comparator = DistanceComparator.parse(node["fields"]["COMPARATOR"][0])
        value = self.visit_input(node["inputs"]["VALUE"][1])
        unit = DistanceUnit.parse(node["fields"]["UNIT"][0])
        return IsDistanceNode(port, comparator, value, unit)

    def visit_distance(self, node) -> DistanceNode:
        """Constructs the AST representation of the Distance node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        port = self.visit_run_motor_for_duration_port(node)
        unit = DistanceUnit.parse(node["fields"]["UNIT"][0])
        return DistanceNode(port, unit)

    def visit_gesture(self, node) -> GestureNode:
        """Constructs the AST representation of the Gesture node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        return GestureNode()

    def visit_is_orientation(self, node) -> IsOrientationNode:
        """Constructs the AST representation of the IsOrientation node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        comparator = HubOrientation[node["fields"]["ORIENTATION"][0].upper()]
        return IsOrientationNode(comparator)

    def visit_orientation(self, node) -> OrientationNode:
        """Constructs the AST representation of the Orientation node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        return OrientationNode()

    def visit_reset_yaw(self, node) -> SetYawAngleNode:
        """Constructs the AST representation of the ResetYaw node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return SetYawAngleNode(next_node)

    def visit_is_button_pressed(self, node) -> IsButtonPressedNode:
        """Constructs the AST representation of the IsButtonPressed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        button = ButtonType[node["fields"]["BUTTON"][0].upper()]
        action = ButtonAction[node["fields"]["EVENT"][0].upper()]
        return IsButtonPressedNode(button, action)

    def visit_hub_angle(self, node) -> HubAngleNode:
        """Constructs the AST representation of the HubAngle node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        unit = AngleUnit[node["fields"]["AXIS"][0].upper()]
        return HubAngleNode(unit)

    def visit_hub_timer(self, node) -> TimerNode:
        """Constructs the AST representation of the HubTimer node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        return TimerNode()

    def visit_hub_reset_timer(self, node) -> ResetTimerNode:
        """Constructs the AST representation of the HubResetTimer node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return ResetTimerNode(next_node)

    def visit_key_pressed(self, node) -> IsKeyPressedNode:
        """Constructs the AST representation of the IsKeyPressed node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        key = self.cst[node["inputs"]["KEY_OPTION"][1]]["fields"]["KEY_OPTION"][0]
        return IsKeyPressedNode(key)

    def visit_play_sound(self, node) -> PlaySoundUntilDoneNode:
        """Constructs the AST representation of the PlaySound node.

        :param node: The Node representation.
        :return: The AST representation.
        """

        sound_json = self.cst[node["inputs"]["SOUND"][1]]["fields"][
            "field_flippersound_sound-selector"
        ][0]
        sound_name = loads(sound_json)["name"]
        next_node = self.visit_node(node["next"])
        return PlaySoundUntilDoneNode(sound_name, next_node)

    def visit_start_sound(self, node) -> StartSoundNode:
        """Constructs the AST representation of the StartSound node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        sound_json = self.cst[node["inputs"]["SOUND"][1]]["fields"][
            "field_flippersound_sound-selector"
        ][0]
        sound_name = loads(sound_json)["name"]
        next_node = self.visit_node(node["next"])
        return StartSoundNode(sound_name, next_node)

    def visit_piano_node(self, node) -> NumericalNode:
        """Constructs the AST representation of the Piano node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        return NumericalNode(
            float(node["fields"]["field_flippersound_custom-piano"][0])
        )

    def visit_play_beep(self, node) -> PlayBeepNode:
        """Constructs the AST representation of the PlayBeep node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        pitch = self.visit_input(node["inputs"]["NOTE"][1])
        duration = self.visit_input(node["inputs"]["DURATION"][1])
        next_node = self.visit_node(node["next"])
        return PlayBeepNode(pitch, duration, next_node)

    def visit_start_beep(self, node) -> StartBeepNode:
        """Constructs the AST representation of the StartBeep node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        pitch = self.visit_input(node["inputs"]["NOTE"][1])
        next_node = self.visit_node(node["next"])
        return StartBeepNode(pitch, next_node)

    def visit_stop_sound(self, node) -> StopBeepNode:
        """Constructs the AST representation of the StopSound node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        next_node = self.visit_node(node["next"])
        return StopBeepNode(next_node)

    def visit_set_volume(self, node) -> SetVolumeNode:
        """Constructs the AST representation of the SetVolume node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        volume = self.visit_input(node["inputs"]["VOLUME"][1])
        next_node = self.visit_node(node["next"])
        return SetVolumeNode(volume, next_node)

    def visit_change_volume(self, node) -> ChangeVolumeNode:
        """Constructs the AST representation of the ChangeVolume node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        volume = self.visit_input(node["inputs"]["VOLUME"][1])
        next_node = self.visit_node(node["next"])
        return ChangeVolumeNode(volume, next_node)

    def visit_volume(self, node) -> VolumeNode:
        """Constructs the AST representation of the Volume node.

        :param node: The Node representation.
        :return: The AST representation.
        """
        return VolumeNode()

    def visit_change_effect(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Pitch effects are not supported, use the best_effort flag to generate code without pitch effects."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the CHANGE PITCH block. Note: that pitch effects are not supported in Python at the moment.",
            next_node,
        )

    def visit_set_effect(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Pitch effects are not supported, use the best_effort flag to generate code without pitch effects."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the SET PITCH block. Note: that pitch effects are not supported in Python at the moment.",
            next_node,
        )

    def visit_clear_effects(self, node) -> CommentNode:
        if not self.best_effort:
            raise NotImplementedError(
                "Pitch effects are not supported, use the best_effort flag to generate code without pitch effects."
            )

        next_node = self.visit_node(node["next"])
        return CommentNode(
            "# Placeholder for the CLEAR PITCH block. Note: that pitch effects are not supported in Python at the moment.",
            next_node,
        )
