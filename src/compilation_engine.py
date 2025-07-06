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
        Compiles a class and starts the compilation process.
        Token_mode: if True, runs a basic parse in token mode so we can get a handle on the number of tokens.
        """
        if token_mode:
            self._token_mode()
            return

        self.tokenizer.advance()

        while self.tokenizer.has_more_tokens():
            match self.tokenizer.current_token_value:
                case "static" | "field":
                    self.compile_class_var_dec(self.root)
                case "function" | "method" | "constructor":
                    self.compile_subroutine(self.root)
                case _:
                    self.write_token(self.root)
                    self.tokenizer.advance()

    def compile_class_var_dec(self, parent):
        """
        Compiles the variable declarations for a class.
        """
        class_var_dec_element = element_tree.SubElement(parent, "classVarDec")

        while True:
            self.write_token(class_var_dec_element)
            if self.tokenizer.current_token_value == ";":
                self.tokenizer.advance()
                break
            self.tokenizer.advance()

    def compile_subroutine(self, parent):
        """
        Compiles the start of a subroutine.
        """
        subroutine_element = element_tree.SubElement(parent, "subroutineDec")
        while True:
            self.write_token(subroutine_element)
            if self.tokenizer.current_token_value == "(":
                self.tokenizer.advance()
                self.compile_parameter_list(subroutine_element)
                self.write_token(subroutine_element)
                break
            self.tokenizer.advance()
        self.compile_subroutine_body(subroutine_element)

    def compile_parameter_list(self, parent):
        """
        Compiles the parameter list of a subroutine.
        """
        parameter_list_element = element_tree.SubElement(parent, "parameterList")
        if self.tokenizer.current_token_value == ")":
            return

        while self.tokenizer.current_token_value != ")":

            self.tokenizer.advance()
            self.write_token(parameter_list_element)

    def compile_subroutine_body(self, parent):
        """
        Compiles the body of a subroutine.
        """
        subroutine_body_element = element_tree.SubElement(parent, "subroutineBody")

        while self.tokenizer.current_token_value != "}":
            self.tokenizer.advance()
            if self.tokenizer.current_token_value == "var":
                self.compile_var_dec(subroutine_body_element)

            if self.tokenizer.current_token_value in "let":
                self.compile_statements(subroutine_body_element)

            self.write_token(subroutine_body_element)

    def compile_statements(self, parent):
        """
        Compiles statements
        """
        statements_element = element_tree.SubElement(parent, "statements")

        match self.tokenizer.current_token_value:
            case "let":
                self.compile_let_statement(statements_element)
            case "do":
                pass
            case _:
                self.write_token(statements_element)
                self.tokenizer.advance()


    def compile_let_statement(self, parent):
        """
        Compiles a let statement.
        """
        let_statement_element = element_tree.SubElement(parent, "letStatement")

        while True:
            print(f"let statement token: {self.tokenizer.current_token_value}")
            if self.tokenizer.current_token_value == ";":
                self.write_token(let_statement_element)
                self.tokenizer.advance()
                break

            if self.tokenizer.current_token_value == "=":
                self.write_token(let_statement_element)
                self.tokenizer.advance()
                self.compile_expression(let_statement_element)
            self.write_token(let_statement_element)
            self.tokenizer.advance()

    def compile_expression(self, parent):
        """
        Compiles an expression.
        """
        expression_element = element_tree.SubElement(parent, "expression")
        self.compile_term(expression_element)

    def compile_term(self, parent):
        term_selement = element_tree.SubElement(parent, "term")


    def compile_expression_list(self, parent):
        """
        Compiles an expression list
        """
        expression_list_element = element_tree.SubElement(parent, "expressionList")

        if self.tokenizer.current_token_value == ")":
            return  # Empty list—bail early
        #
        # while self.tokenizer.current_token_value != ")":
        #
        #     self.compile_expression(expression_list_element)
        #
        #     if self.tokenizer.current_token_value == ",":
        #         self.write_token(expression_list_element)
        #         self.tokenizer.advance()
        #     self.tokenizer.advance()


    def compile_var_dec(self, parent):
        """
        Compiles the variable declaration of a subroutine.
        """
        subroutine_var_dec = element_tree.SubElement(parent, "varDec")

        while True:
            self.write_token(subroutine_var_dec)
            if self.tokenizer.current_token_value == ";":
                self.tokenizer.advance()
                break

            self.tokenizer.advance()

    def write_token(self, parent_name):
        """
        Writes a token to the XML.
        """
        token_tag = element_tree.SubElement(parent_name, self.tokenizer.current_token_type).text = f" {self.tokenizer.current_token_value} "


    def _token_mode(self):
        """
        Compiles to a basic XML for testing.
        """
        print(f"Writing in token mode")
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            self.write_token(self.root)
            element_tree.SubElement(self.tokens_root, self.tokenizer.token_type()).text = f" {self.tokenizer.current_token_value} "

        tree = element_tree.ElementTree(self.tokens_root)
        tree.write("output.xml", encoding="utf-8")

        with open("output.xml", "r", encoding="utf-8") as f:
            content = f.read()
            pretty = xml.dom.minidom.parseString(content).toprettyxml(indent="  ")
            print("\n=== XML File Output ===")
            print(pretty)
