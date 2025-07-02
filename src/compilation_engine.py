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


    def compile_class(self):
        """
        Compiles a class to XML code recursively.
        """
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            element_tree.SubElement(self.root, self.tokenizer.token_type()).text = self.tokenizer.current_token_value
        tree = element_tree.ElementTree(self.root)
        tree.write("output.xml", encoding="utf-8", xml_declaration=True)

        with open("output.xml", "r", encoding="utf-8") as f:
            content = f.read()
            pretty = xml.dom.minidom.parseString(content).toprettyxml(indent="  ")
            print("\n=== XML File Output ===")
            print(pretty)

        return True
