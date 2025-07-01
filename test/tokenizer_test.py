"""
The test suite for the Jack tokenizer
"""
from pathlib import Path
import pytest

from src.tokenizer import Tokenizer

@pytest.fixture
def setup_resources():
    """
    Sets up the resources necessary for the tokenizer
    """
    jack_file: Path = Path("F:\Programming\Hack and ASM Projects\JackCompiler\input\ArrayTest\Main.jack")
    tokenizer = Tokenizer(jack_file)
    yield {
        "tokenizer": tokenizer,
    }


def test_object_creation(setup_resources):
    """
    Tests that the tokenizer object is created properly.
    """
    tokenizer = setup_resources["tokenizer"]


def test_open_file(setup_resources):
    """
    Test that we can open our file when an object is instantiated
    """
    tokenizer = setup_resources["tokenizer"]
    print(tokenizer.open_file)
    assert tokenizer.open_file is not None


def test_has_more_tokens_space(setup_resources):
    """
    Test that we're able to check whitespaces in has_more_tokens
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "Here is some text"
    more_tokens: bool = tokenizer.has_more_tokens()
    assert more_tokens is True


def test_has_more_tokens_inline_comments(setup_resources):
    """
    Test that we're able to check in line comments in has_more_tokens
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "//Here is a comment And some more\nNon Comment"
    more_tokens: bool = tokenizer.has_more_tokens()
    assert more_tokens is True


def test_has_more_tokens_blocked_comments(setup_resources):
    """
    Test that we're able to check blocked comments in has_more_tokens
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "/* Here is a comment And some more */\n And some more text"
    more_tokens: bool = tokenizer.has_more_tokens()
    assert more_tokens is True


def test_has_more_tokens_blocked_two_asterisk_comments(setup_resources):
    """
    Test that we're able to check blocked comments in has_more_tokens
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "/** Here is a comment And some more */\n Non comment"
    more_tokens: bool = tokenizer.has_more_tokens()
    assert more_tokens is True


def test_advance_keyword(setup_resources):
    """
    Test that advance can parse a keyword.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "class Paddle {}"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)

    assert current_token == ("keyword", "class")

@pytest.mark.parametrize("keyword_list", ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
                      "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"])
def test_all_keywords(setup_resources, keyword_list):
    """
    Test that advance can read all keywords
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = f"{keyword_list} Paddle"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)

    assert current_token == ("keyword" or "identifier", keyword_list)


def test_advance_identifier(setup_resources):
    """
    Test that when we get an identifier, it works and returns it properly
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "Paddle\n"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)
    assert current_token == ("identifier", "Paddle")


def test_advance_current_token(setup_resources):
    """
    Test that we can advance a token and it's a symbol.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "{item}"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)
    assert current_token == ("symbol", "{")


@pytest.mark.parametrize("symbol_list", ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"])
def test_full_symbol_list(setup_resources, symbol_list):
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = f"{symbol_list}"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)
    assert current_token == ("symbol", f"{symbol_list}")


def test_advance_integer_constant(setup_resources):
    """
    Test that the tokenizer can detect integer constants.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "38512"
    current_token = tokenizer.advance()
    print(tokenizer.current_token_value)
    assert current_token == ("integerConstant", "38512")


def test_advance_handles_spaces(setup_resources):
    """
    Test that we're able to check whitespaces in has_more_tokens
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = " Here is some text"
    dealing_with_whitespace = tokenizer.advance()
    print(dealing_with_whitespace)
    assert dealing_with_whitespace == ("identifier", "Here")


def test_advance_string_constants(setup_resources):
    """
    Test the tokenizer's ability to parse string constants.
    They should be returned without any quotes.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = '"Here is some text"'
    string_constant: str = tokenizer.advance()
    print(string_constant)
    assert string_constant == ("stringConstant", "Here is some text")


def test_token_type_return(setup_resources):
    """
    Test that our token type is returned properly.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = '"Here is some text"'
    string_constant: str = tokenizer.advance()
    print(string_constant)
    current_token: str = tokenizer.token_type()
    assert current_token == "stringConstant"


def test_keyword_return(setup_resources):
    """
    Test that keyword returns the proper keyword.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "class Paddle"
    string_constant: str = tokenizer.advance()
    print(string_constant)
    current_token: str = tokenizer.keyword()
    assert current_token == "class"


def test_keyword_not_a_keyword(setup_resources):
    """
    Test that keyword errors when not using the proper keyword
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "34182"
    not_a_string_constant: str = tokenizer.advance()
    print(not_a_string_constant)
    with pytest.raises(ValueError):
        tokenizer.keyword()


def test_symbol_return(setup_resources):
    """
    Test that symbol returns the proper symbol.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "{an item}"
    string_constant: str = tokenizer.advance()
    print(string_constant)
    current_token: str = tokenizer.symbol()
    assert current_token == "{"


def test_symbol_not_a_symbol(setup_resources):
    """
    Test that symbol errors when not using the proper symbol
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "34182"
    not_a_symbol: str = tokenizer.advance()
    print(not_a_symbol)
    with pytest.raises(ValueError):
        tokenizer.symbol()


def test_identifier_return(setup_resources):
    """
    Test that identifier returns the proper identifier.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "Paddle "
    identifier: str = tokenizer.advance()
    print(identifier)
    current_token: str = tokenizer.identifier()
    assert current_token == "Paddle"


def test_identifier_not_a_identifier(setup_resources):
    """
    Test that identifier errors when not using the proper identifier
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "34182"
    not_an_identifier: str = tokenizer.advance()
    print(not_an_identifier)
    with pytest.raises(ValueError):
        tokenizer.identifier()


def test_int_val_return(setup_resources):
    """
    Test that int_val returns the proper int_val.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "31435"
    int_val: str = tokenizer.advance()
    print(int_val)
    current_token: int = tokenizer.int_val()
    assert current_token == int("31435")



def test_int_val_not_int_val(setup_resources):
    """
    Test that int_val errors when not using the proper int_val
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "babouche "
    not_an_int_val: str = tokenizer.advance()
    print(not_an_int_val)
    with pytest.raises(ValueError):
        tokenizer.int_val()


def test_string_constant_return(setup_resources):
    """
    Test that string_constant returns the proper string_constant.
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = '"Babouche"'
    string_constant: str = tokenizer.advance()
    print(string_constant)
    current_token: str = tokenizer.string_constant()
    assert current_token == "Babouche"


def test_string_constant_not_string_constant(setup_resources):
    """
    Test that string_constant errors when not using the proper string_constant
    """
    tokenizer = setup_resources["tokenizer"]
    tokenizer.open_file = "babouche "
    not_a_string_constant: str = tokenizer.advance()
    print(not_a_string_constant)
    with pytest.raises(ValueError):
        tokenizer.string_constant()
