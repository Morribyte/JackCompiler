"""
src/compilation_engine.py
Handles turning the tokens into XML output and writes them to file.
"""
from pathlib import Path
import xml.etree.ElementTree as element_tree
import xml.dom.minidom

from src.tokenizer import Tokenizer

class CompilationEngine:
    """
    Represents a compilation engine object.
    """
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.tokens_root = element_tree.Element("tokens")
        self.root = element_tree.Element("class")

    def compile_class(self, token_mode=False):
        """
        Compiles a class to XML code recursively.
        """
        if token_mode:
            self._token_mode()
        else:
            while self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                print(f"Token found: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")
                #
                match self.tokenizer.current_token_value:
                    case "static" | "field":
                        self.compile_class_var_dec(self.root)
                    case "constructor" | "function" | "method":
                        self.compile_subroutine(self.root)
                    case _:
                        self.write_token(self.root)


    def compile_class_var_dec(self, parent):
        """
        Compiles a class's variable declaration.
        """
        class_var_dec_element = element_tree.SubElement(parent, "classVarDec")
        while True:
            self.write_token(class_var_dec_element)
            if self.tokenizer.current_token_value == ";":
                break
            self.tokenizer.advance()

    def compile_subroutine(self, parent):
        """
        Compiles a method.
        """
        subroutine_element = element_tree.SubElement(parent, "subroutineDec")
        while True:
            self.write_token(subroutine_element)
            if self.tokenizer.current_token_value == "(":
                break
            self.tokenizer.advance()
        self.tokenizer.advance()

        self.compile_parameter_list(subroutine_element)
        self.write_token(subroutine_element)
        self.tokenizer.advance()

        self.compile_subroutine_body(subroutine_element)
        self.compile_statements(subroutine_element)

    def compile_parameter_list(self, parent):
        """
        Compile's a method's parameter list.
        """
        parameter_list_element = element_tree.SubElement(parent, "parameterList")
        while self.tokenizer.current_token_value != ")":
            self.write_token(parameter_list_element)
            self.tokenizer.advance()

    def compile_subroutine_body(self, parent):
        """
        Compile a method's subroutine body.
        """
        subroutine_body_element = element_tree.SubElement(parent, "subroutineBody")
        while True:
            if self.tokenizer.current_token_value == "var":
                self.compile_var_dec(subroutine_body_element)
            else:
                self.write_token(subroutine_body_element)
            if self.tokenizer.current_token_value == "}":
                break
            self.tokenizer.advance()


    def compile_var_dec(self, parent):
        """
        Compile a method's variable declaration.
        """
        var_dec_element = element_tree.SubElement(parent, "varDec")
        while True:
            self.write_token(var_dec_element)
            if self.tokenizer.current_token_value == ";":
                break
            self.tokenizer.advance()

    def compile_statements(self, parent):
        """
        Compile any statement.
        """
        statements_element = element_tree.SubElement(parent, "statements")
        print(f"Current statement: ({self.tokenizer.current_token_value} | {self.tokenizer.current_token_type})")
        match self.tokenizer.current_token_value:
            case "let":
                self.compile_let_statement(statements_element)
            case "if":
                pass
            case "while":
                pass
            case "do":
                pass
            case "return":
                pass
            case _:
                print(f"Unknown keyword pair: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_type}")
                return

    def compile_let_statement(self, parent):
        """
        Compiles a let statement.
        """
        let_statement_element = element_tree.SubElement(parent, "letStatement")
        while True:
            self.write_token(let_statement_element)
            if self.tokenizer.current_token_value == ";":
                break
            self.tokenizer.advance()

    def write_token(self, parent_name):
        """
        Writes a token to the XML.
        """
        element_tree.SubElement(parent_name, self.tokenizer.current_token_type).text = f"{self.tokenizer.current_token_value}"

    def _token_mode(self):
        """
        Compiles to a basic XML for testing.
        """
        while self.tokenizer.has_more_tokens():
            print(f"Has more tokens: {self.tokenizer.has_more_tokens()}")
            self.tokenizer.advance()
            element_tree.SubElement(self.tokens_root, self.tokenizer.token_type()).text = f" {self.tokenizer.current_token_value} "

        tree = element_tree.ElementTree(self.tokens_root)
        tree.write("output.xml", encoding="utf-8", xml_declaration=True)

        with open("output.xml", "r", encoding="utf-8") as f:
            content = f.read()
            pretty = xml.dom.minidom.parseString(content).toprettyxml(indent="  ")
            print("\n=== XML File Output ===")
            print(pretty)

