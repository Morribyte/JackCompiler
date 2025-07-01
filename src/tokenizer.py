"""
src/tokenizer.py
Handles tokenizing the input
"""
KEYWORD_LIST: list = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                      "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

SYMBOL_LIST: list = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]

class Tokenizer:
    def __init__(self, jack_file):
        self.jack_file = jack_file
        with open(self.jack_file, "r") as file:
            self.open_file = file.read()

        self.current_index = 0
        self.current_token_type = ""
        self.current_token_value = ""

    def has_more_tokens(self) -> bool:
        """
        Checks to see if there are more tokens.
        """
        i: int = self.current_index
        while i < len(self.open_file):
            peek: str = self.open_file[i:i+2]
            if self.open_file[i].isspace():
                i += 1
                continue
            elif peek == '//':
                i += 2
                while i < len(self.open_file) and self.open_file[i] != '\n':
                    i += 1
                i += 1
            elif peek == "/*":
                i += 2
                while i < len(self.open_file) - 1:
                    if self.open_file[i] == "*" and self.open_file[i+1] == "/":
                        i += 2
                        break
                    i += 1
            else:
                print(self.open_file[i])
                i += 1
                return True
        return False

    def advance(self):
        """
        After checking if we have more tokens, we advance and save the token.
        """
        ch = self.open_file[self.current_index]
        # Symbols

        if ch in SYMBOL_LIST:
            self.current_index += 1
            self.current_token_type = "symbol"
            self.current_token_value = ch
            return self.current_token_type, self.current_token_value

        # Keywords and Identifiers
        if ch.isalpha() or ch == "_":
            start = self.current_index
            while self.current_index < len(self.open_file) and self.open_file[self.current_index].isalnum() or self.open_file[self.current_index] == "_":
                print(self.open_file[self.current_index])
                self.current_index += 1
            self.current_token_value = self.open_file[start:self.current_index]
            self.current_token_type = "keyword" if self.current_token_value in KEYWORD_LIST else "identifier"
            return self.current_token_type, self.current_token_value

        return None





