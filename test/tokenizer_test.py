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


def test_has_more_tokens(setup_resources):
    """
    Test that we're able to check that there's more tokens.
    """
    tokenizer = setup_resources["tokenzier"]
    more_tokens: bool = tokenizer.has_more_tokens()
    assert more_tokens is True
