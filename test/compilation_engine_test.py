"""
Testing document for the compilation engine
"""

import pytest

from src.compilation_engine import CompilationEngine

@pytest.fixture
def setup_resources():
    """
    Sets up the necessary resources for each test.
    """
    compilation = CompilationEngine()
    yield {
        "compilation": compilation,
    }


def test_object_creation(setup_resources):
    """
    Test object creation
    """
    compilation = setup_resources["compilation"]
    assert compilation is not None