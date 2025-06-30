"""
The test suite for the Jack tokenizer
"""

import pytest

from src.tokenizer import Tokenizer

@pytest.fixture
def setup_resources():
    """
    Sets up the resources necessary for the tokenizer
    """
    tokenizer = Tokenizer()
    yield {
        "tokenizer": tokenizer,
    }


def test_object_creation(setup_resources):
    """
    Tests that the tokenizer object is created properly.
    """
    tokenizer = setup_resources["tokenizer"]
