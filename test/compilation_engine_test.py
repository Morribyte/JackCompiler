"""
Testing document for the compilation engine
"""
from pathlib import Path
import pytest
# import xml.dom.minidom


from src.compilation_engine import CompilationEngine
from src.tokenizer import Tokenizer

@pytest.fixture(scope="class")
def setup_resources():
    """
    Sets up the necessary resources for each test.
    """
    jack_file: Path = Path("F:\Programming\Hack and ASM Projects\JackCompiler\input\ArrayTest\Main.jack")
    tokenizer = Tokenizer(jack_file)
    compilation = CompilationEngine(tokenizer)
    yield {
        "compilation": compilation,
    }

def test_object_creation(setup_resources):
    """
    Test object creation
    """
    compilation = setup_resources["compilation"]
    assert compilation is not None


def test_tokenizer_variable(setup_resources):
    """
    Test that when initializer happens, the tokenizer properly loads, and we can access its internal attributes.
    """
    compilation = setup_resources["compilation"]
    print(compilation.tokenizer.jack_file)
    assert str(compilation.tokenizer.jack_file) == "F:\Programming\Hack and ASM Projects\JackCompiler\input\ArrayTest\Main.jack"


def test_compile_class_token_mode_on(setup_resources, tmp_path):
    """
    Test that when we turn on token mode, it produces an XML file.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class(token_mode=True)
    assert compilation.tokenizer.jack_file.exists()
