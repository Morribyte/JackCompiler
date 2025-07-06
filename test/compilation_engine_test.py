"""
Testing document for the compilation engine
"""
from pathlib import Path
import pytest

import xml.etree.ElementTree as element_tree


from src.compilation_engine import CompilationEngine
from src.tokenizer import Tokenizer

@pytest.fixture
def setup_resources():
    """
    Sets up the necessary resources for each test.
    """
    jack_file: Path = Path(r"F:\Programming\Hack and ASM Projects\JackCompiler\input\10\Square\Main.jack")
    tokenizer = Tokenizer(jack_file)
    compilation = CompilationEngine(tokenizer)


    yield {
        "compilation": compilation,
    }

def write_xml(setup_resources):
    compilation = setup_resources["compilation"]
    tree = element_tree.ElementTree(compilation.root)
    element_tree.indent(tree)
    tree.write("output.xml", encoding="utf-8", short_empty_elements=False)
    xml_str = element_tree.tostring(compilation.root, encoding="unicode", method="html")

    print(xml_str)


    # with open("output.xml", "w", encoding="utf-8") as f:
    #     f.write(xml_str)

    # with open("output.xml", "r", encoding="utf-8") as f:
    #     content = f.read()
    #     # print("\n=== XML File Output ===")
    #     print(content)

    print("XML file parsed and formatted.")

   # return pretty

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
    assert str(compilation.tokenizer.jack_file) == r"F:\Programming\Hack and ASM Projects\JackCompiler\input\10\Square\Main.jack"


def test_compile_class_token_mode_on(setup_resources):
    """
    Test that when we turn on token mode, it produces an XML file.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class(token_mode=True)
    assert compilation.tokenizer.jack_file.exists()


def test_compile_class_token_mode_off(setup_resources, capsys):
    """
    Test that when we turn off token mode explicitly, it runs the normal cycle.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class(token_mode=False)
    captured = capsys.readouterr()

    assert "Compiling class" in captured.out


def test_write_token(setup_resources):
    """
    Test that the write_token helper method properly writes to the XML file.
    This test does not have any assertions in it because I can visually check it.
    """
    compilation = setup_resources["compilation"]

    compilation.tokenizer.current_token_type = "keyword"
    compilation.tokenizer.current_token_value = "Main"
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<class>" in pretty


# Tests for compilation
def test_compile_class(setup_resources):
    """
    Test that when we call compile_class, it properly handles the class keyword with its first token.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<class>" in pretty


def test_compile_first_keyword(setup_resources):
    """
    Test that when we call compile_class, it properly handles everything up to the first keyword.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>"""
    pretty = write_xml(setup_resources)

    assert code in pretty


def test_compile_class_var_dec(setup_resources):
    """
    Test that when we call compile_class, it handles class var dec.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """  <classVarDec>
    <keyword> static </keyword>
    <keyword> boolean </keyword>
    <identifier> test </identifier>
    <symbol> ; </symbol>
  </classVarDec>"""
    pretty = write_xml(setup_resources)

    assert "<classVarDec>" in pretty
    assert code in pretty


def test_subroutine_dec(setup_resources):
    """
    Test that when we call compile_class, it handles subroutine declarations.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """  </classVarDec>
  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>"""
    pretty = write_xml(setup_resources)

    assert "<subroutineDec>" in pretty
    assert code in pretty


def test_compile_parameter_list(setup_resources):
    """
    Test that when we call compile_class, it handles the parameter list.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code="""  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList>
    </parameterList>
    <symbol> ) </symbol>"""

    pretty = write_xml(setup_resources)

    assert "<parameterList>" in pretty
    assert code in pretty