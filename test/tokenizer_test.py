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


def test_advance_current_token(setup_resources):
    """
    Test that we can advance a token.
    """
    tokenizer = setup_resources["tokenizer"]
    current_token = tokenizer.advance()
    assert current_token == "{"
