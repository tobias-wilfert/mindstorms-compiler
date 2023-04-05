import typer

from src.code_generator import CodeGenerator
from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


# TODO: Also consider if having color in the output is worth it
# TODO: This is super basic for now add more functionality later via optional flags to allow for different behavior
def main(
    filename: str = typer.Argument(
        ..., help="The path to the file that should be converted."
    )
):
    # Extract the JSON from the input file
    concrete_syntax_tree = filter_json(extract_json(filename))
    # print(json.dumps(concrete_syntax_tree, indent=2)) # Print the interesting file content

    # Generate the AST
    visitor = Visitor()
    abstract_syntax_tree = visitor.visit(concrete_syntax_tree)
    # TODO: Add a flag for this to be outputted
    # print(abstract_syntax_tree.tree_representation())

    # Generate the code
    code_generator = CodeGenerator()
    # TODO: Write the code to the file or output it
    print(code_generator.generate(abstract_syntax_tree))


if __name__ == "__main__":
    typer.run(main)
