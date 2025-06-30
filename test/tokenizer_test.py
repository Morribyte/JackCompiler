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
    assert tokenizer.open_file is not None
