"""
Testing document for the compilation engine
"""
from pathlib import Path
import pytest

import xml.etree.ElementTree as element_tree
import xml.dom.minidom


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
    tree = element_tree.ElementTree(compilation.root)
    tree.write("output.xml", encoding="utf-8", xml_declaration=True)

    with open("output.xml", "r", encoding="utf-8") as f:
        content = f.read()
        pretty = xml.dom.minidom.parseString(content).toprettyxml(indent="  ")
        print("\n=== XML File Output ===")
        print(pretty)

    with open("output.xml", "w", encoding="utf-8") as f:
        f.write(pretty)


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


def test_compile_class_token_mode_on(setup_resources):
    """
    Test that when we turn on token mode, it produces an XML file.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class(token_mode=True)
    assert compilation.tokenizer.jack_file.exists()


class TestCompile:
    """
    Class that handles testing an entire compiler suite
    """
    def test_compile_class_token_mode_off(self, setup_resources, capsys):
        """
        Test that when we turn off token mode explicitly, it runs the normal cycle.
        """
        compilation = setup_resources["compilation"]
        compilation.compile_class(token_mode=False)
        captured = capsys.readouterr()

        assert "Token found: " in captured.out


    def test_write_token(self, setup_resources, capsys):
        """
        Test that the write_token helper method properly writes to the XML file.
        """
        compilation = setup_resources["compilation"]
        current_token_type = compilation.tokenizer.current_token_type = "legume"
        compilation.write_token(current_token_type)

