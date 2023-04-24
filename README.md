# Mindstorms Compiler

[![Python application](https://github.com/tobias-wilfert/mindstorms-compiler/actions/workflows/python-app.yml/badge.svg)](https://github.com/tobias-wilfert/mindstorms-compiler/actions/workflows/python-app.yml)

 ## How to use:

**Note:** This currently assumes you have some knowledge of working with Python and [Python](https://www.python.org) as well as [Pip](https://pypi.org) installed.

1. Download this repository.  
2. Download the necessary requirements for this project by running `pip install -r requirements.txt` in the root of the project.
3. Run the compiler by executing the following command in the root of the project `python -m src INPUT_FILENAME` (where `INPUT_FILENAME` is the path to the file that should be compiled). Furthermore there are multiple optional flags that can be used, running `python -m src --help` gives you the following explanation for them:
```
Usage: python -m src [OPTIONS] INPUT_FILENAME

Arguments:
  INPUT_FILENAME  The path to the file that should be converted.  [required]

Options:
  --output-filename TEXT  The name of the file the code should be written to.
                          If none is provided the code will just be printed.
  --ast / --no-ast        Indicates if the AST representation should also be
                          outputted.  [default: no-ast]
  --ast-filename TEXT     Indicates where to write the AST representation to
                          if --ast is used. If none is provided the
                          representation will just be printed.
  --safe / --no-safe      Indicates if safer code should be outputted, the
                          code might be more verbose.  [default: no-safe]
  --help                  Show this message and exit.
```

## Description:

***Work in progress...***  

 A compiler from the [Scratch](https://scratch.mit.edu)-like programming language used by the [51515 Robot Inventor Lego set](https://www.lego.com/en-be/product/robot-inventor-51515) to Python.  
A great feature of the latest generation of Mindstorms is that they can be programmes using both a [Scratch](https://scratch.mit.edu)-like language (great for beginners) and [Python](https://www.python.org) (great for more experienced users). Sadly however making the switch from the Scratch-like language to Python can be a bit tricky as there is no way to generate the equivalent Python code for your past projects. This is where this program comes into play it takes as input your `project.lms` file and outputs the equivalent Python code.

 ### Structure:

 The root of the project contains a lot of uninteresting files which you can ignored unless you want to dive into the weeds how the project works.

 The source code can be found in `./src` this is a Python module which itself contains other Python modules the entry point is `./src/__main__.py` from which you should be able to follow the flow through all other files.

 The test can be found in `./tests` more precisely the input files for the tests are in `./tests/inputs` structured by the class of the blocks that are in the files. Each test input is a folder containing 3 files, the `FILE.lms` file with `FILE` the same name as the folder, the `project.json` this is the underlying json representation extracted from the the `FILE.lms` and `icon.scg` also extracted from the which in essence is a screenshot of the blocks that are in the project.  
 **Note:** If you save a file a `.lms` project file to `./tests/inputs` and run the `./format_input.sh` script on it it will automatically generate a folder with the same name as the file that will contain all 3 files discussed above.  
 The test themselves are written using [pytest](https://docs.pytest.org/en/7.2.x/) and are split into 3 categories, which test the JSON-extraction, AST-generation and Code-generation respectively. These can be run using `pipenv run pytest`.

 ### Already supported:

A set of the most used blocks is already supported (see the list below). On top of generating the equivalent Python code the compiler can also output the abstract syntax tree representation of a program. The representation is done using [Graphviz](https://graphviz.org) a simple example of such a AST visualization can be seen below together with the generated python code.

![example.svg](./example.png)

```python
my_variable = 10.0
motor_pair = MotorPair('A', 'B')
motor_pair.set_default_speed(50)  # Note: Needed since the default speed is 100, which is too fast.
motor_pair.set_default_speed(int(my_variable))  # Note: This methods expects an integer so wee need to convert the value.
motor_pair.move(10.0, 'cm')
```

## List of supported blocks

| Block        | # Configurations |
|--------------|------:|
| **Motors** |  |
| Run Motor for Duration | 11 |
| Motor Go to Position   | 8  |
| Start Motor   | 6  |
| Stop Motor   | 5  |
| Set Motor Speed   | 7  |
| Motor Position   | 3  |
| Motor Speed   | 3  |
| **Movement** |  |
| Move for Duration   | 9  |
| Move  with Steering | 7  |
| Start moving with Steering   | 2  |
| Stop moving   | 1  |
| Set Movement Speed   | 2  |
| Set Movement Motor   | 3  |
| Set Motor Rotation   | 3  |
| **Operators** |  |
| Plus   | 3 |
| Minus   | 3  |
| Multiply   | 3  |
| Divide   | 3  |
| **Variables** |  |
| Variable   | 2  |
| Set Variable To   | 2  |
| Change Variable By   | 2  |
| List   | 1  |
| Add Item to List   | 4  |
| **Events** |  |
| When Program Starts   | 1  |