"""
src/compilation_engine.py
Handles turning the tokens into XML output and writes them to file.

Jack Language Reference:
'xxx': An item around quotes means it appears like this literally within the statements.
xxx: represents names of terminal and non-terminal elements
(): represents grouping
x | y: either x or y
x y: x is followed by y
x?: x appears 0-1 times
x*: x appears 0 or more times
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
        Grammar:
        'class' className '{' classVarDec* subroutineDec* '}'
        """

        if token_mode:
            self._token_mode()
            return

        # Advance tokenizer and assert first token is in fact class
        self.tokenizer.advance()  # Starts the token advancing
        assert self.tokenizer.current_token_value == "class"

        while self.tokenizer.has_more_tokens():
            match self.tokenizer.current_token_value:
                case "static" | "field":
                    self.compile_class_var_dec(self.root)
                case "function" | "method" | "constructor":
                    self.compile_subroutine(self.root)
                case _:
                    self.write_token(self.root)
                    self.tokenizer.advance()

        # Final token write
        self.write_token(self.root)

    def compile_class_var_dec(self, parent):
        """
        Compiles the variable declarations for a class.
        ('static'|'field') type varName (',' varName)* ';'
        """
        class_var_dec_element = element_tree.SubElement(parent, "classVarDec")
        assert self.tokenizer.current_token_value in ["static", "field"]

        while self.tokenizer.current_token_value != ";":
            self.write_token(class_var_dec_element)
            self.tokenizer.advance()
        self.write_token(class_var_dec_element)
        self.tokenizer.advance()

    def compile_subroutine(self, parent):
        """
        Compiles the start of a subroutine.
        ('constructor'|'method'|'function') ('void'|type) subroutineName '('parameterList')' subroutineBody
        """
        subroutine_element = element_tree.SubElement(parent, "subroutineDec")
        assert self.tokenizer.current_token_value in ["function", "method", "constructor"]

        while self.tokenizer.current_token_value != ")":
            if self.tokenizer.current_token_value == "(":
                self.write_token(subroutine_element)  # Writes (
                self.compile_parameter_list(subroutine_element)
                self.write_token(subroutine_element)  # Writes ) once parameters are dealt with
                break
            self.write_token(subroutine_element)
            self.tokenizer.advance()
        self.compile_subroutine_body(subroutine_element)

    def compile_parameter_list(self, parent):
        """
        Compiles the parameter list of a subroutine.
        ((type varName) (',' type varName)*)?
        """
        parameter_list_element = element_tree.SubElement(parent, "parameterList")
        # Writes the token after the (. If it'
        self.tokenizer.advance()

        if self.tokenizer.current_token_value == ")":
            return  # Parent method will handle writing the closing ")"

        while self.tokenizer.current_token_value != ")":
            self.tokenizer.advance()
            self.write_token(parameter_list_element)
        self.tokenizer.advance()

    def compile_subroutine_body(self, parent):
        """
        Compiles the body of a subroutine.
        '{'varDec* statements '}'
        """
        subroutine_body_element = element_tree.SubElement(parent, "subroutineBody")
        self.tokenizer.advance()
        self.write_token(subroutine_body_element)

        while self.tokenizer.current_token_value != "}":
            self.tokenizer.advance()

            if self.tokenizer.current_token_value == "var":
                self.compile_var_dec(subroutine_body_element)

            if self.tokenizer.current_token_value in ["let", "do", "if", "while", "return"]:
                self.compile_statements(subroutine_body_element)

        self.write_token(subroutine_body_element)
        self.tokenizer.advance()

    def compile_var_dec(self, parent):
        """
        Compiles the variable declaration of a subroutine.
        'var' type varName (',' varName)* ';'
        """
        subroutine_var_dec = element_tree.SubElement(parent, "varDec")

        while self.tokenizer.current_token_value != ";":
            self.write_token(subroutine_var_dec)
            self.tokenizer.advance()
        self.write_token(subroutine_var_dec)

    def compile_statements(self, parent):
        """
        Compiles statements
        statement*
        """
        if self.tokenizer.current_token_value in ["let", "do", "if", "while", "return"]:
            statements_element = element_tree.SubElement(parent, "statements")

            while self.tokenizer.current_token_value in ["let", "do", "if", "while", "return"]:
                print(f"CURRENT TOKEN: {self.tokenizer.current_token_value}")
                match self.tokenizer.current_token_value:
                    case "let":
                        self.compile_let_statement(statements_element)
                    case "do":
                        self.compile_do_statement(statements_element)
                    case "if":
                        self.compile_if_statement(statements_element)
                    case "while":
                        self.compile_while_statement(statements_element)
                    case "return":
                        self.compile_return_statement(statements_element)

    def compile_let_statement(self, parent):
        """
        Compiles a let statement.
        'let' varName ('['expression']')? '=' expression ';'
        """
        let_statement_element = element_tree.SubElement(parent, "letStatement")

        while self.tokenizer.current_token_value != ";":
            if self.tokenizer.current_token_value == "[":
                self.write_token(let_statement_element)
                self.tokenizer.advance()
                self.compile_expression(let_statement_element)

            elif self.tokenizer.current_token_value == "=":
                self.write_token(let_statement_element)
                self.tokenizer.advance()
                self.compile_expression(let_statement_element)
            elif self.tokenizer.current_token_value == ";":
                self.write_token(let_statement_element)
                break
            else:
                self.write_token(let_statement_element)
                self.tokenizer.advance()
        self.write_token(let_statement_element)  # Writes the ';'
        self.tokenizer.advance()

    def compile_do_statement(self, parent):
        """
        Compiles a do statement.
        'do' subroutineCall ';'

        subroutineCall -> subroutineName '('expressionList')' | (className|varName)'.'subroutineName'('expressionList')'
        """
        do_statement_element = element_tree.SubElement(parent, "doStatement")

        while self.tokenizer.current_token_value != ";":
            if self.tokenizer.current_token_value == "(":
                self.write_token(do_statement_element)
                self.compile_expression_list(do_statement_element)
                self.tokenizer.advance()
            else:
                self.write_token(do_statement_element)
                self.tokenizer.advance()
        self.write_token(do_statement_element)  # Writes the ';'
        self.tokenizer.advance()


    def compile_if_statement(self, parent):
        """
        Compiles an if statement.
        'if' '('expression')' '{'statements'}' ('else' '{'statements'}')?
        """
        if_statement_element = element_tree.SubElement(parent, "ifStatement")

        while self.tokenizer.current_token_value != "}":
            if self.tokenizer.current_token_value == "(":
                self.write_token(if_statement_element)
                self.tokenizer.advance()
                self.compile_expression(if_statement_element)
            self.write_token(if_statement_element)
            self.tokenizer.advance()
            self.compile_statements(if_statement_element)

        self.write_token(if_statement_element)
        self.tokenizer.advance()

        if self.tokenizer.current_token_value == "else":
            while self.tokenizer.current_token_value != "}":
                self.write_token(if_statement_element)
                self.tokenizer.advance()
                self.compile_statements(if_statement_element)

            self.write_token(if_statement_element)
            self.tokenizer.advance()

    def compile_while_statement(self, parent):
        """
        Compiles a while statement
        'while' '('expression')' '{'statements'}'
        """

        while_statement_element = element_tree.SubElement(parent, "whileStatement")

        while self.tokenizer.current_token_value != "}":
            if self.tokenizer.current_token_value == "(":
                self.write_token(while_statement_element)
                self.tokenizer.advance()
                self.compile_expression(while_statement_element)
            if self.tokenizer.current_token_value == "{":
                self.write_token(while_statement_element)  # '{'
                self.tokenizer.advance()
                self.compile_statements(while_statement_element)
                self.write_token(while_statement_element)  # '}'
                self.tokenizer.advance()
            self.write_token(while_statement_element)
            self.tokenizer.advance()


    def compile_return_statement(self, parent):
        """
        Compiles a return statement.
        'return' expression?';'
        """
        return_statement_element = element_tree.SubElement(parent, "returnStatement")

        while self.tokenizer.current_token_value != ";":
            self.write_token(return_statement_element)
            self.tokenizer.advance()
        self.write_token(return_statement_element)

    def compile_expression(self, parent):
        """
        Compiles an expression.
        term (op term)*
        op -> '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='

        """
        expression_element = element_tree.SubElement(parent, "expression")
        self.compile_term(expression_element)

        while self.tokenizer.current_token_value in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self.write_token(expression_element)
            self.tokenizer.advance()

            self.compile_term(expression_element)

    def compile_term(self, parent):
        """
        Compiles a set of terms inside expressions to the specified values.
        integerConstant | stringConstant | keywordConstant | varName | varName'['expression']' | '('expression')'|(unaryOpTerm)|subroutineCall

        subroutineCall -> subroutineName '('expressionList')' | (className|varName)'.'subroutineName'('expressionList')'
        unaryOpTerm -> '-' | '~'

        keywordConstant -> 'true' | 'false' | 'null' | 'this'
        """
        term_element = element_tree.SubElement(parent, "term")

        match self.tokenizer.current_token_type:
            case "identifier":
                print(f"Current token: {self.tokenizer.current_token_value}")
                next_token_value = self.tokenizer.open_file[
                                   self.tokenizer.current_index:self.tokenizer.current_index + 1]
                print(f"Looking ahead. Next token value is: {next_token_value}")

                match next_token_value:
                    case ".":
                        print("Subroutine Call.")
                        while self.tokenizer.current_token_value != ";":
                            self.write_token(term_element)
                            self.tokenizer.advance()
                            if self.tokenizer.current_token_value == "(":
                                self.write_token(term_element)
                                self.tokenizer.advance()
                                self.compile_expression_list(term_element)

                                if self.tokenizer.current_token_value == ")":
                                    self.write_token(term_element)
                                    self.tokenizer.advance()
                                    break
                    case "[":
                        print("varName expression")
                        while self.tokenizer.current_token_value != ";":
                            self.write_token(term_element)
                            self.tokenizer.advance()
                            if self.tokenizer.current_token_value == "[":
                                self.write_token(term_element)
                                self.tokenizer.advance()
                                self.compile_expression(term_element)
                    case _:
                        print("plain varname")
                        self.write_token(term_element)
                        self.tokenizer.advance()

            case "stringConstant":
                self.write_token(term_element)
                self.tokenizer.advance()
            case "keyword":
                if self.tokenizer.current_token_value in ["true", "false", "null", "this"]:
                    self.write_token(term_element)
                    self.tokenizer.advance()
            case "integerConstant":
                self.write_token(term_element)
                self.tokenizer.advance()
            case "symbol":
                if self.tokenizer.current_token_value == "(":
                    self.write_token(term_element)  # write (
                    self.tokenizer.advance()
                    self.compile_expression(term_element)
                    self.write_token(term_element)  # write )
                    self.tokenizer.advance()
                elif self.tokenizer.current_token_value in ["-", "~"]:
                    self.write_token(term_element)  # Write the unary symbol
                    self.tokenizer.advance()
                    self.compile_term(term_element)  # Nest the next term inside

    def compile_expression_list(self, parent) -> int:
        """
        Compiles an expression list
        (expression(',' expression)*)?
        """
        expression_list_element = element_tree.SubElement(parent, "expressionList")
        count = 0
        print(f"EXPR LIST ENTRY TOKEN: {self.tokenizer.current_token_value}")
        self.tokenizer.advance()
        if self.tokenizer.current_token_value in [")", "]"]:
            return count

        return count

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
