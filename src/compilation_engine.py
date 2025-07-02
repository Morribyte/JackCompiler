"""
src/compilation_engine.py
Handles turning the tokens into XML output and writes them to file.
"""

import xml.etree.ElementTree as element_tree

from src.tokenizer import Tokenizer

class CompilationEngine:
    """
    Represents a compilation engine object.
    """
    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
