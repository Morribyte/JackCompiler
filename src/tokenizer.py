"""
src/tokenizer.py
Handles tokenizing the input
"""

class Tokenizer:
    def __init__(self, jack_file):
        self.jack_file = jack_file
        with open(self.jack_file, "r") as file:
            self.open_file = file.read()