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
        self.root = element_tree.Element("tokens")


    def compile_class(self, token_mode=False):
        """
        Compiles a class to XML code recursively.
        """
        if token_mode:
            self._token_mode()
        else:
            if self.tokenizer.has_more_tokens():
                print(f"Token found: {self.tokenizer.current_token_type} | {self.tokenizer.current_token_value}")
                self.tokenizer.advance()
            return True

    def _token_mode(self):
        """
        Compiles to a basic XML for testing.
        """
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            element_tree.SubElement(self.root, self.tokenizer.token_type()).text = f" {self.tokenizer.current_token_value} "
            print(f"{repr(self.tokenizer.current_token_value)}")

        tree = element_tree.ElementTree(self.root)
        tree.write("output.xml", encoding="utf-8", xml_declaration=True)

        with open("output.xml", "r", encoding="utf-8") as f:
            content = f.read()
            pretty = xml.dom.minidom.parseString(content).toprettyxml(indent="  ")
            print("\n=== XML File Output ===")
            print(pretty)
