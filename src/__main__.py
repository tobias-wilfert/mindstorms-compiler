import typer

from src.code_generator import CodeGenerator
from src.json_parser import extract_json, filter_json
from src.visitor import Visitor


def main(
    input_filename: str = typer.Argument(
        ..., help="The path to the file that should be converted."
    ),
    output_filename: str = typer.Option(
        "",
        help="The name of the file the code should be written to. If none is provided the code will just be printed.",
    ),
    ast: bool = typer.Option(
        False, help="Indicates if the AST representation should also be outputted."
    ),
    ast_filename: str = typer.Option(
        "",
        help="Indicates where to write the AST representation to if --ast is used. If none is provided the representation will just be printed.",
    ),
    safe: bool = typer.Option(
        False,
        help="Indicates if safer code should be outputted, the code might be more verbose.",
    ),
    best_effort: bool = typer.Option(
        True,
        help="Indicates if the code should be generated even if it contains blocks that are not translatable (will be skipped).",
    ),
):
    # Extract the JSON from the input file
    concrete_syntax_tree = filter_json(extract_json(input_filename))
    # print(json.dumps(concrete_syntax_tree, indent=2)) # Print the interesting file content

    # Generate the AST
    visitor = Visitor(best_effort)
    abstract_syntax_tree = visitor.visit(concrete_syntax_tree)

    # Output the AST
    if ast:
        if ast_filename == "":
            print(f"{'-'*10} Begin: AST Representation {'-'*10}")
            print(abstract_syntax_tree.tree_representation())
            print(f"{'-'*10} End: AST Representation {'-'*10}")
        else:
            f = open(ast_filename, "x")
            f.write(abstract_syntax_tree.tree_representation())
            f.close()

    # Generate the code
    code_generator = CodeGenerator(safe)

    # Output the Code
    if output_filename == "":
        print(f"{'-'*10} Begin: Code {'-'*10}")
        print(code_generator.generate(abstract_syntax_tree))
        print(f"{'-'*10} End: Code {'-'*10}")
    else:
        f = open(output_filename, "x")
        f.write(code_generator.generate(abstract_syntax_tree))
        f.close()


if __name__ == "__main__":
    typer.run(main)
