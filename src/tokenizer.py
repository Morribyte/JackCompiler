"""
src/tokenizer.py
Handles tokenizing the input
"""

class Tokenizer:
    def __init__(self, jack_file):
        self.jack_file = jack_file
        with open(self.jack_file, "r") as file:
            self.open_file = file.read()

        self.current_index = 0
        self.current_token = ""

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
        if self.has_more_tokens():
            return "{"
        return "{"

