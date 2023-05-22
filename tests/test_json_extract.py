# Tests to check if the json is extracted correctly from the .lms input files.

import json

from src.json_parser import extract_json


def helper(filename: str, directory: str = "."):
    """Helper function that contains the logic to test if the json of a certain file is extracted correctly.

    :param filename: The name of the file that should be checked.
    :type filename: str
    :param directory: The folder that the file is in.
    :type directory: str
    """
    with open(f"tests/inputs/{directory}/{filename}/project.json", "r") as file:
        assert extract_json(
            f"tests/inputs/{directory}/{filename}/{filename}.lms"
        ) == json.load(file)


# ---------- Base ----------
def test_extract_json_empty():
    helper("empty")


# ---------- Events ----------
def test_extract_json_when_program_starts():
    helper("when_program_starts", "Events")


# ---------- Motors ----------
# - Run Motor for duration
def test_extract_json_run_motor_for_duration_base():
    helper("run_motor_for_duration_base", "Motors")


def test_extract_json_run_motor_for_duration_counterclockwise():
    helper("run_motor_for_duration_counterclockwise", "Motors")


def test_extract_json_run_motor_for_duration_degrees():
    helper("run_motor_for_duration_degrees", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors():
    helper("run_motor_for_duration_multiple_motors", "Motors")


def test_extract_json_run_motor_for_duration_multiple_motors3():
    helper("run_motor_for_duration_multiple_motors3", "Motors")


def test_extract_json_run_motor_for_duration_all_motors():
    helper("run_motor_for_duration_all_motors", "Motors")


def test_extract_json_run_motor_for_duration_seconds():
    helper("run_motor_for_duration_seconds", "Motors")


def test_extract_json_run_motor_for_duration_value_node():
    helper("run_motor_for_duration_value_node", "Motors")


def test_extract_json_run_motor_for_duration_port_list():
    helper("run_motor_for_duration_port_list", "Motors")


def test_extract_json_run_motor_for_duration_port_variable():
    helper("run_motor_for_duration_port_variable", "Motors")


def test_extract_json_run_motor_for_duration_value_variable():
    helper("run_motor_for_duration_value_variable", "Motors")


# - Motor Go to Position
def test_extract_json_motor_go_to_position_base():
    helper("motor_go_to_position_base", "Motors")


def test_extract_json_motor_go_to_position_clockwise():
    helper("motor_go_to_position_clockwise", "Motors")


def test_extract_json_motor_go_to_position_counterclockwise():
    helper("motor_go_to_position_counterclockwise", "Motors")


def test_extract_json_motor_go_to_position_multiple_motors():
    helper("motor_go_to_position_multiple_motors", "Motors")


def test_extract_json_motor_go_to_position_value_node():
    helper("motor_go_to_position_value_node", "Motors")


def test_extract_json_motor_go_to_position_port_list():
    helper("motor_go_to_position_port_list", "Motors")


def test_extract_json_motor_go_to_position_port_variable():
    helper("motor_go_to_position_port_variable", "Motors")


def test_extract_json_motor_go_to_position_value_variable():
    helper("motor_go_to_position_value_variable", "Motors")


# - Start Motor
def test_extract_json_start_motor_base():
    helper("start_motor_base", "Motors")


def test_extract_json_start_motor_all_motors():
    helper("start_motor_all_motors", "Motors")


def test_extract_json_start_motor_multiple_motors():
    helper("start_motor_multiple_motors", "Motors")


def test_extract_json_start_motor_counterclockwise():
    helper("start_motor_counterclockwise", "Motors")


def test_extract_json_start_motor_port_list():
    helper("start_motor_port_list", "Motors")


def test_extract_json_start_motor_port_variable():
    helper("start_motor_port_variable", "Motors")


# - Stop Motor
def test_extract_json_stop_motor_base():
    helper("stop_motor_base", "Motors")


def test_extract_json_stop_motor_all_motors():
    helper("stop_motor_all_motors", "Motors")


def test_extract_json_stop_motor_multiple_motors():
    helper("stop_motor_multiple_motors", "Motors")


def test_extract_json_stop_motor_port_list():
    helper("stop_motor_port_list", "Motors")


def test_extract_json_stop_motor_port_variable():
    helper("stop_motor_port_variable", "Motors")


# - Set Motor Speed
def test_extract_json_set_motor_speed_base():
    helper("set_motor_speed_base", "Motors")


def test_extract_json_set_motor_speed_all_motors():
    helper("set_motor_speed_all_motors", "Motors")


def test_extract_json_set_motor_speed_multiple_motors():
    helper("set_motor_speed_multiple_motors", "Motors")


def test_extract_json_set_motor_speed_value_node():
    helper("set_motor_speed_value_node", "Motors")


def test_extract_json_set_motor_speed_port_list():
    helper("set_motor_speed_port_list", "Motors")


def test_extract_json_set_motor_speed_port_variable():
    helper("set_motor_speed_port_variable", "Motors")


def test_extract_json_set_motor_speed_value_variable():
    helper("set_motor_speed_value_variable", "Motors")


# Motor Position
def test_extract_json_motor_position_base():
    helper("motor_position_base", "Motors")


def test_extract_json_motor_position_list():
    helper("motor_position_list", "Motors")


def test_extract_json_motor_position_variable():
    helper("motor_position_variable", "Motors")


# - Motor Speed
def test_extract_json_motor_speed_base():
    helper("motor_speed_base", "Motors")


def test_extract_json_motor_speed_list():
    helper("motor_speed_list", "Motors")


def test_extract_json_motor_speed_variable():
    helper("motor_speed_variable", "Motors")


# ---------- Movement ----------
# - Move for duration
def test_extract_json_move_for_duration_backwards():
    helper("move_for_duration_backwards", "Movement")


def test_extract_json_move_for_duration_base():
    helper("move_for_duration_base", "Movement")


def test_extract_json_move_for_duration_clockwise():
    helper("move_for_duration_clockwise", "Movement")


def test_extract_json_move_for_duration_counterclockwise():
    helper("move_for_duration_counterclockwise", "Movement")


def test_extract_json_move_for_duration_degrees():
    helper("move_for_duration_degrees", "Movement")


def test_extract_json_move_for_duration_inches():
    helper("move_for_duration_inches", "Movement")


def test_extract_json_move_for_duration_rotations():
    helper("move_for_duration_rotations", "Movement")


def test_extract_json_move_for_duration_seconds():
    helper("move_for_duration_seconds", "Movement")


def test_extract_json_move_for_duration_value_variable():
    helper("move_for_duration_value_variable", "Movement")


# - Move with Steering
def test_extract_json_move_with_steering_base():
    helper("move_with_steering_base", "Movement")


def test_extract_json_move_with_steering_degrees():
    helper("move_with_steering_degrees", "Movement")


def test_extract_json_move_with_steering_inches():
    helper("move_with_steering_inches", "Movement")


def test_extract_json_move_with_steering_rotations():
    helper("move_with_steering_rotations", "Movement")


def test_extract_json_move_with_steering_seconds():
    helper("move_with_steering_seconds", "Movement")


def test_extract_json_move_with_steering_steering_variable():
    helper("move_with_steering_steering_variable", "Movement")


def test_extract_json_move_with_steering_value_variable():
    helper("move_with_steering_value_variable", "Movement")


# - Start Moving with Steering
def test_extract_json_start_moving_with_steering_base():
    helper("start_moving_with_steering_base", "Movement")


def test_extract_json_start_moving_with_steering_variable():
    helper("start_moving_with_steering_variable", "Movement")


# - Stop Moving
def test_extract_json_stop_moving():
    helper("stop_moving", "Movement")


# - Set Movement Speed
def test_extract_json_set_movement_speed_base():
    helper("set_movement_speed_base", "Movement")


def test_extract_json_set_movement_speed_value_variable():
    helper("set_movement_speed_value_variable", "Movement")


# - Set Movement Motors
def test_extract_json_set_movement_motors_base():
    helper("set_movement_motors_base", "Movement")


def test_extract_json_set_movement_motors_list():
    helper("set_movement_motors_list", "Movement")


def test_extract_json_set_movement_motors_variable():
    helper("set_movement_motors_variable", "Movement")


# - Set Motor rotation
def test_extract_json_set_motor_rotation_base():
    helper("set_motor_rotation_base", "Movement")


def test_extract_json_set_motor_rotation_inches():
    helper("set_motor_rotation_inches", "Movement")


def test_extract_json_set_motor_rotation_value_variable():
    helper("set_motor_rotation_value_variable", "Movement")


# ---------- Light ----------
# - Start Animation
def test_extract_json_start_animation_base():
    helper("start_animation_base", "Light")


def test_extract_json_start_animation_custom():
    helper("start_animation_custom", "Light")


# - Play Animation until done
def test_extract_json_play_animation_until_done_base():
    helper("play_animation_until_done_base", "Light")


def test_extract_json_play_animation_until_done_custom():
    helper("play_animation_until_done_custom", "Light")


# - Turn on for duration
def test_extract_json_turn_on_for_duration_base():
    helper("turn_on_for_duration_base", "Light")


def test_extract_json_turn_on_for_duration_custom():
    helper("turn_on_for_duration_custom", "Light")


def test_extract_json_turn_on_for_duration_variable():
    helper("turn_on_for_duration_variable", "Light")


# - Turn on
def test_extract_json_turn_on_base():
    helper("turn_on_base", "Light")


def test_extract_json_turn_on_custom():
    helper("turn_on_custom", "Light")


# - Write
def test_extract_json_write_base():
    helper("write_base", "Light")


def test_extract_json_write_variable():
    helper("write_variable", "Light")


# - Turn off
def test_extract_json_turn_off_pixels():
    helper("turn_off_pixels", "Light")


# - Set pixel brightness
def test_extract_json_set_pixel_brightness_base():
    helper("set_pixel_brightness_base", "Light")


def test_extract_json_set_pixel_brightness_variable():
    helper("set_pixel_brightness_variable", "Light")


# - Set pixel
def test_extract_json_set_pixel_base():
    helper("set_pixel_base", "Light")


def test_extract_json_set_pixel_variable():
    helper("set_pixel_variable", "Light")


def test_extract_json_set_pixel_x_value_variable():
    helper("set_pixel_x_value_variable", "Light")


def test_extract_json_set_pixel_y_value_variable():
    helper("set_pixel_y_value_variable", "Light")


# - Rotate Orientation
def test_extract_json_rotate_orientation_clockwise():
    helper("rotate_orientation_clockwise", "Light")


def test_extract_json_rotate_orientation_counterclockwise():
    helper("rotate_orientation_counterclockwise", "Light")


# - Set Orientation
def test_extract_json_set_orientation_upright():
    helper("set_orientation_upright", "Light")


def test_extract_json_set_orientation_upsidedown():
    helper("set_orientation_upsidedown", "Light")


def test_extract_json_set_orientation_left():
    helper("set_orientation_left", "Light")


def test_extract_json_set_orientation_right():
    helper("set_orientation_right", "Light")


# - Set Center button
def test_extract_json_set_center_button_red():
    helper("set_center_button_red", "Light")


def test_extract_json_set_center_button_yellow():
    helper("set_center_button_yellow", "Light")


def test_extract_json_set_center_button_green():
    helper("set_center_button_green", "Light")


def test_extract_json_set_center_button_cyan():
    helper("set_center_button_cyan", "Light")


def test_extract_json_set_center_button_azure():
    helper("set_center_button_azure", "Light")


def test_extract_json_set_center_button_pink():
    helper("set_center_button_pink", "Light")


def test_extract_json_set_center_button_white():
    helper("set_center_button_white", "Light")


def test_extract_json_set_center_button_black():
    helper("set_center_button_black", "Light")


# -Light up distance sensor
def test_extract_json_light_up_distance_sensor_base():
    helper("light_up_distance_sensor_base", "Light")


def test_extract_json_light_up_distance_sensor_port_list():
    helper("light_up_distance_sensor_port_list", "Light")


def test_extract_json_light_up_distance_sensor_port_variable():
    helper("light_up_distance_sensor_port_variable", "Light")


# ---------- Sound ----------
# - Play sound until done base
def test_extract_json_play_sound_until_done_base():
    helper("play_sound_until_done_base", "Sound")


def test_extract_json_play_sound_until_done_custom():
    helper("play_sound_until_done_custom", "Sound")


# - Start sound
def test_extract_json_start_sound_base():
    helper("start_sound_base", "Sound")


def test_extract_json_start_sound_custom():
    helper("start_sound_custom", "Sound")


# - Play beep
def test_extract_json_play_beep_base():
    helper("play_beep_base", "Sound")


def test_extract_json_play_beep_variable():
    helper("play_beep_variable", "Sound")


# - Start beep
def test_extract_json_start_beep_base():
    helper("start_beep_base", "Sound")


def test_extract_json_start_beep_variable():
    helper("start_beep_variable", "Sound")


# - Stop beep
def test_extract_json_stop_beep():
    helper("stop_beep", "Sound")


# - Change Pitch
def test_extract_json_change_pitch_effect():
    helper("change_pitch_effect", "Sound")


# - Set Pitch
def test_extract_json_set_pitch_effect():
    helper("set_pitch_effect", "Sound")


# - Clear Sound Effects
def test_extract_json_clear_sound_effects():
    helper("clear_sound_effects", "Sound")


# - Change volume
def test_extract_json_change_volume_base():
    helper("change_volume_base", "Sound")


def test_extract_json_change_volume_variable():
    helper("change_volume_variable", "Sound")


# - Change volume
def test_extract_json_set_volume_base():
    helper("set_volume_base", "Sound")


def test_extract_json_set_volume_variable():
    helper("set_volume_variable", "Sound")


# - Volume
def test_extract_json_volume():
    helper("volume", "Sound")


# ---------- Control ----------
# - Wait for seconds
def test_extract_json_wait_for_seconds_base():
    helper("wait_for_seconds_base", "Control")


def test_extract_json_wait_for_seconds_variable():
    helper("wait_for_seconds_variable", "Control")


# - Wait until
def test_extract_json_wait_until():
    helper("wait_until", "Control")


# - Repeat loop
def test_extract_json_repeat_loop_base():
    helper("repeat_loop_base", "Control")


def test_extract_json_repeat_loop_variable():
    helper("repeat_loop_variable", "Control")


# - Forever loop
def test_extract_json_forever_loop():
    helper("forever_loop", "Control")


# - Repeat until loop
def test_extract_json_repeat_until_loop():
    helper("repeat_until_loop", "Control")


# - If then
def test_extract_json_if_then():
    helper("if_then", "Control")


# - If then else
def test_extract_json_if_then_else():
    helper("if_then_else", "Control")


# - Do this and this
def test_extract_json_do_this_and_this():
    helper("do_this_and_this", "Control")


# - Stop other stacks
def test_extract_json_stop_other_stacks():
    helper("stop_other_stacks", "Control")


# - Stop
def test_extract_json_stop_base():
    helper("stop_base", "Control")


def test_extract_json_stop_this_stack():
    helper("stop_this_stack", "Control")


def test_extract_json_stop_exit_program():
    helper("stop_exit_program", "Control")


# ---------- Sensors ----------
# - Is color
# black
def test_extract_json_is_color_black():
    helper("is_color_black", "Sensors")


# violet
def test_extract_json_is_color_violet():
    helper("is_color_violet", "Sensors")


# blue
def test_extract_json_is_color_blue():
    helper("is_color_blue", "Sensors")


# light blue
def test_extract_json_is_color_light_blue():
    helper("is_color_light_blue", "Sensors")


# green
def test_extract_json_is_color_green():
    helper("is_color_green", "Sensors")


# yellow
def test_extract_json_is_color_yellow():
    helper("is_color_yellow", "Sensors")


# red
def test_extract_json_is_color_red():
    helper("is_color_red", "Sensors")


# white
def test_extract_json_is_color_white():
    helper("is_color_white", "Sensors")


# no color
def test_extract_json_is_color_no_color():
    helper("is_color_no_color", "Sensors")


# - Color
def test_extract_json_color():
    helper("color", "Sensors")


# - Is reflected light
def test_extract_json_is_reflected_light_base():
    helper("is_reflected_light_base", "Sensors")


def test_extract_json_is_reflected_light_equal():
    helper("is_reflected_light_equal", "Sensors")


def test_extract_json_is_reflected_light_greater():
    helper("is_reflected_light_greater", "Sensors")


def test_extract_json_is_reflected_light_variable():
    helper("is_reflected_light_variable", "Sensors")


# - Reflected light
def test_extract_json_reflected_light():
    helper("reflected_light", "Sensors")


# - Is distance
def test_extract_json_is_distance_base():
    helper("is_distance_base", "Sensors")


def test_extract_json_is_distance_cm():
    helper("is_distance_cm", "Sensors")


def test_extract_json_is_distance_inches():
    helper("is_distance_inches", "Sensors")


def test_extract_json_is_distance_exactly_at():
    helper("is_distance_exactly_at", "Sensors")


def test_extract_json_is_distance_farther_than():
    helper("is_distance_farther_than", "Sensors")


# - Distance
def test_extract_json_distance_base():
    helper("distance_base", "Sensors")


def test_extract_json_distance_cm():
    helper("distance_cm", "Sensors")


def test_extract_json_distance_inches():
    helper("distance_inches", "Sensors")


# - Gesture
def test_extract_json_gesture():
    helper("gesture", "Sensors")


# - Is hub shaken
def test_extract_json_is_hub_shaken_base():
    helper("is_hub_shaken_base", "Sensors")


def test_extract_json_is_hub_shaken_falling():
    helper("is_hub_shaken_falling", "Sensors")


def test_extract_json_is_hub_shaken_tapped():
    helper("is_hub_shaken_tapped", "Sensors")


# - Is hub orientation
def test_extract_json_is_hub_orientation_base():
    helper("is_hub_orientation_base", "Sensors")


def test_extract_json_is_hub_orientation_back():
    helper("is_hub_orientation_back", "Sensors")


def test_extract_json_is_hub_orientation_bottom():
    helper("is_hub_orientation_bottom", "Sensors")


def test_extract_json_is_hub_orientation_left_side():
    helper("is_hub_orientation_left_side", "Sensors")


def test_extract_json_is_hub_orientation_right_side():
    helper("is_hub_orientation_right_side", "Sensors")


def test_extract_json_is_hub_orientation_top():
    helper("is_hub_orientation_top", "Sensors")


# - Hub orientation
def test_extract_json_hub_orientation():
    helper("hub_orientation", "Sensors")


# - Set yaw angle
def test_extract_json_set_yaw_angle():
    helper("set_yaw_angle", "Sensors")


# - Is button pressed
def test_extract_json_is_button_pressed_base():
    helper("is_button_pressed_base", "Sensors")


def test_extract_json_is_button_pressed_released():
    helper("is_button_pressed_released", "Sensors")


def test_extract_json_is_button_pressed_right():
    helper("is_button_pressed_right", "Sensors")


# - Hub angle
def test_extract_json_hub_angle_base():
    helper("hub_angle_base", "Sensors")


def test_extract_json_hub_angle_roll():
    helper("hub_angle_roll", "Sensors")


def test_extract_json_hub_angle_yaw():
    helper("hub_angle_yaw", "Sensors")


# - Timer
def test_extract_json_timer():
    helper("timer", "Sensors")


# - Reset timer
def test_extract_json_reset_timer():
    helper("reset_timer", "Sensors")


# - Key pressed
def test_extract_json_key_pressed():
    helper("key_pressed", "Sensors")


# ---------- Operators ----------
def test_extract_json_arithmetic():
    helper("arithmetic", "Operators")


def test_extract_json_divide():
    helper("divide", "Operators")


def test_extract_json_minus():
    helper("minus", "Operators")


def test_extract_json_multiply():
    helper("multiply", "Operators")


def test_extract_json_plus():
    helper("plus", "Operators")


def test_extract_json_arithmetic_variable():
    helper("arithmetic_variable", "Operators")


# - Pick random number
def test_extract_json_pick_random_number_base():
    helper("pick_random_number_base", "Operators")


def test_extract_json_pick_random_number_variable():
    helper("pick_random_number_variable", "Operators")


# - Less than
def test_extract_json_less_than_base():
    helper("less_than_base", "Operators")


def test_extract_json_less_than_variable():
    helper("less_than_variable", "Operators")


# - Equal
def test_extract_json_equal_base():
    helper("equal_base", "Operators")


def test_extract_json_equal_variable():
    helper("equal_variable", "Operators")


# - Greater than
def test_extract_json_greater_than_base():
    helper("greater_than_base", "Operators")


def test_extract_json_greater_than_variable():
    helper("greater_than_variable", "Operators")


# - And
def test_extract_json_and():
    helper("and", "Operators")


# - Or
def test_extract_json_or():
    helper("or", "Operators")


# - Not
def test_extract_json_not():
    helper("not", "Operators")


# - Is between
def test_extract_json_is_between_base():
    helper("is_between_base", "Operators")


def test_extract_json_is_between_variable():
    helper("is_between_variable", "Operators")


# Join strings
def test_extract_json_join_strings_base():
    helper("join_strings_base", "Operators")


def test_extract_json_join_strings_variable():
    helper("join_strings_variable", "Operators")


# - Letter of string
def test_extract_json_letter_of_string_base():
    helper("letter_of_string_base", "Operators")


def test_extract_json_letter_of_string_variable():
    helper("letter_of_string_variable", "Operators")


# - Length of string
def test_extract_json_length_of_string_base():
    helper("length_of_string_base", "Operators")


def test_extract_json_length_of_string_variable():
    helper("length_of_string_variable", "Operators")


# - String contains
def test_extract_json_string_contains_base():
    helper("string_contains_base", "Operators")


def test_extract_json_string_contains_variable():
    helper("string_contains_variable", "Operators")


# - Mod
def test_extract_json_mod_base():
    helper("mod_base", "Operators")


def test_extract_json_mod_variable():
    helper("mod_variable", "Operators")


# - Round
def test_extract_json_round_base():
    helper("round_base", "Operators")


def test_extract_json_round_variable():
    helper("round_variable", "Operators")


# - Math function
# 10
def test_extract_json_math_function_10():
    helper("math_function_10", "Operators")


# abs
def test_extract_json_math_function_abs():
    helper("math_function_abs", "Operators")


# acos
def test_extract_json_math_function_acos():
    helper("math_function_acos", "Operators")


# asin
def test_extract_json_math_function_asin():
    helper("math_function_asin", "Operators")


# atan
def test_extract_json_math_function_atan():
    helper("math_function_atan", "Operators")


# atan2
def test_extract_json_math_function_atan2():
    helper("math_function_atan2", "Operators")


# ceiling
def test_extract_json_math_function_ceiling():
    helper("math_function_ceiling", "Operators")


# copysign
def test_extract_json_math_function_copysign():
    helper("math_function_copysign", "Operators")


# cos
def test_extract_json_math_function_cos():
    helper("math_function_cos", "Operators")


# e
def test_extract_json_math_function_e():
    helper("math_function_e", "Operators")


# floor
def test_extract_json_math_function_floor():
    helper("math_function_floor", "Operators")


# hypot
def test_extract_json_math_function_hypot():
    helper("math_function_hypot", "Operators")


# ln
def test_extract_json_math_function_ln():
    helper("math_function_ln", "Operators")


# log
def test_extract_json_math_function_log():
    helper("math_function_log", "Operators")


# max
def test_extract_json_math_function_max():
    helper("math_function_max", "Operators")


# min
def test_extract_json_math_function_min():
    helper("math_function_min", "Operators")


# pow
def test_extract_json_math_function_pow():
    helper("math_function_pow", "Operators")


# sin
def test_extract_json_math_function_sin():
    helper("math_function_sin", "Operators")


# sqrt
def test_extract_json_math_function_sqrt():
    helper("math_function_sqrt", "Operators")


# tan
def test_extract_json_math_function_tan():
    helper("math_function_tan", "Operators")


# variable
def test_extract_json_math_function_variable():
    helper("math_function_variable", "Operators")


# ---------- Variables ----------
# - Change Variable by
def test_extract_json_change_variable_by():
    helper("change_variable_by", "Variables")


# - Variable
def test_extract_json_variable_num():
    helper("variable_num", "Variables")


def test_extract_json_variable_string():
    helper("variable_string", "Variables")


# - List
def test_extract_json_list():
    helper("list", "Variables")


# - Add item to list
def test_extract_json_add_item_to_list_base():
    helper("add_item_to_list_base", "Variables")


def test_extract_json_add_item_to_list_int():
    helper("add_item_to_list_int", "Variables")


def test_extract_json_add_item_to_list_list():
    helper("add_item_to_list_list", "Variables")


def test_extract_json_add_item_to_list_variable():
    helper("add_item_to_list_variable", "Variables")


# - Delete item in list
def test_extract_json_delete_item_in_list_base():
    helper("delete_item_in_list_base", "Variables")


def test_extract_json_delete_item_in_list_variable():
    helper("delete_item_in_list_variable", "Variables")


# - Delete all items in list
def test_extract_json_delete_all_items_in_list():
    helper("delete_all_items_in_list", "Variables")


# - Insert item at index
def test_extract_json_insert_item_at_index_base():
    helper("insert_item_at_index_base", "Variables")


def test_extract_json_insert_item_at_index_variable_index():
    helper("insert_item_at_index_variable_index", "Variables")


def test_extract_json_insert_item_at_index_variable_item():
    helper("insert_item_at_index_variable_item", "Variables")


# - Replace item at index
def test_extract_json_replace_item_at_index_base():
    helper("replace_item_at_index_base", "Variables")


def test_extract_json_replace_item_at_index_variable_index():
    helper("replace_item_at_index_variable_index", "Variables")


def test_extract_json_replace_item_at_index_variable_value():
    helper("replace_item_at_index_variable_value", "Variables")


# - Item at Index
def test_extract_json_item_at_index_base():
    helper("item_at_index_base", "Variables")


def test_extract_json_item_at_index_variable():
    helper("item_at_index_variable", "Variables")


# - Index of item
def test_extract_json_index_of_item_base():
    helper("index_of_item_base", "Variables")


def test_extract_json_index_of_item_variable():
    helper("index_of_item_variable", "Variables")


# - Length of list
def test_extract_json_length_of_list():
    helper("length_of_list", "Variables")


# - List contains
def test_extract_json_list_contains_base():
    helper("list_contains_base", "Variables")


def test_extract_json_list_contains_variable():
    helper("list_contains_variable", "Variables")
