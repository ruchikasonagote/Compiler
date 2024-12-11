import sys
import ply.yacc as yacc
import drd_parser
import scanner
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker
from WatGenerator import *

if __name__ == '__main__':
    filename = input("Enter the source file path: ")
    try:
        with open(filename, "r") as file:
            text = file.read()
    except IOError:
        print(f"Cannot open {filename} file")
        sys.exit(0)

    lexer = scanner.lexer
    ast = drd_parser.parser.parse(text, lexer=scanner.lexer)

    # if ast:
    #     print("Abstract Syntax Tree:")
    #     ast.printTree()  

    # Type check
    typeChecker = TypeChecker()
    typeChecker.visit(ast)  
    if not typeChecker.valid:
        raise Exception('Program invalid (types)')

    if ast:
        wat_generator = WatGenerator()
        wat_filename = f"{filename.split('.')[0]}.wat"
        wat_generator.generate_wat(ast, wat_filename)
        print(f"Generated {wat_filename} with WebAssembly text.")

