"""
This file contains the logic to extract the relevant json from the *.lms input file.
The json will than server as the Concrete Syntax tree that is visited to generate the Abstract Syntaxt tree.
"""
import io
import json
import zipfile


def extract_json(filename: str) -> dict:
    """Extracts the json out of a Mindstorms .lms file
    TODO: This puts the enitre inner zip file into memory which might not be ideal, so decide if unzipping it somewhere on disk is better
    See reference: https://stackoverflow.com/q/11930515/8076979
    :param filename: The path to the lms file
    :type filename: str
    :return: Returns a dictionary representation of the json
    :rtype: dict
    """
    # TODO: Check if this only works now becuase I link it from the correct position?
    with zipfile.ZipFile(filename, "r") as outer_zip:
        with outer_zip.open("scratch.sb3") as inner_zip:
            file_data = io.BytesIO(inner_zip.read())
            with zipfile.ZipFile(file_data) as nested_zip:
                return json.load(nested_zip.open("project.json"))


def filter_json(json: dict) -> dict:
    """Filter the uncessesary json code that is not relevant for the code generation.
    More precisly only the variables, lists, broadcast, blocks and extention settings are relevant for the code generation.
    :param json: The json in dict format.
    :type json: dict
    :return: The json that is relevant for the code generation.
    :rtype: dict
    """
    return {
        "variables": json["targets"][1]["variables"],
        "lists": json["targets"][1]["lists"],
        "broadcasts": json["targets"][1]["broadcasts"],
        "blocks": json["targets"][1]["blocks"],
        "extensions": json["extensions"],
    }
