import json

import typer

from extract_json import extract_json


# TODO: Also consider if having colour in the output is worth it
# TODO: This is super basic for now add more functionality later via optional flags to allow for different behaviour
def main(
    file_name: str = typer.Argument(
        ..., help="The path to the file that should be converted."
    )
):
    # Goal is to extract the json and then only work with the json from there such the file doesn't need to be in memory
    print(json.dumps(extract_json(file_name)["targets"][1], indent=2))

    # TODO: Extract only the necessary information (Front-end) (Parser -> AST)
    # Having the AST intermediate allows to generate graphs and optimize
    # The fun thing about this is that We don't neccesarrly have one starting block but could have multiple hence we need to deal with that slightly
    # differently
    # So the way scratch deals with that is by looking which one was created first and running that
    # FIXME: Not sure we are able to extract that sadly, so the next best thing we can do is go by which is higher, first big trade off
    print("TODO: Construct AST")

    # TODO: Do the conversion (Back-end) (AST -> Python code)
    print("TOOD: Generate the code from the AST")
    return ""


if __name__ == "__main__":
    typer.run(main)
