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
        print(f"{self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")
        if token_mode:
            self._token_mode()
            return

        print("\n~*~*~ Compiling class ~*~*~\n")
        while self.tokenizer.has_more_tokens():
            print(f"Current token: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")

            if self.tokenizer.current_token_value in ("static", "field"):
                print("\n~*~*~ Found class variable declaration ~*~*~\n")
                self.compile_class_var_dec(self.root)
            self.tokenizer.advance()
            self.write_token(self.root)

        print(f"Token found: {self.tokenizer.current_token_value}")
        print(f"Token type found: {self.tokenizer.current_token_type}")

    def compile_class_var_dec(self, parent):
        """
        Compiles the variable declarations for a class.
        """
        class_var_dec_element = element_tree.SubElement(parent, "classVarDec")
        while True:
            if self.tokenizer.current_token_value == ";":
                self.write_token(class_var_dec_element)
                break
            self.write_token(class_var_dec_element)
            self.tokenizer.advance()

        print(f"Current token: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")

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
            print(f"Current token type: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")
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
