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

        while self.tokenizer.has_more_tokens():
            print(f"Current token type: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")
            self.tokenizer.advance()
            self.write_token(self.root)
            element_tree.SubElement(self.tokens_root, self.tokenizer.token_type()).text = f" {self.tokenizer.current_token_value} "


        print(f"Token found: {self.tokenizer.current_token_value}")
        print(f"Token type found: {self.tokenizer.current_token_type}")



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

