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

    print("XML file parsed and formatted.")

    return xml_str

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


def test_write_token(setup_resources):
    """
    Test that the write_token helper method properly writes to the XML file.
    This test does not have any assertions in it because I can visually check it.
    """
    compilation = setup_resources["compilation"]

    compilation.tokenizer.current_token_type = "keyword"
    compilation.tokenizer.current_token_value = "Main"
    compilation.compile_class(token_mode=False)

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
    <parameterList></parameterList>
    <symbol> ) </symbol>"""

    pretty = write_xml(setup_resources)

    assert "<parameterList>" in pretty
    assert code in pretty


def test_subroutine_body(setup_resources):
    """
    Test that when we call compile_class, it can run the subroutine body
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<subroutineBody>" in pretty
    assert "</subroutineBody>" in pretty


def test_var_dec(setup_resources):
    """
    Test that when we call compile_class, it runs through the variable declarations properly.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code="""      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier> SquareGame </identifier>
        <identifier> game </identifier>
        <symbol> ; </symbol>
      </varDec>"""

    pretty = write_xml(setup_resources)

    assert "<subroutineBody>" in pretty
    assert "</subroutineBody>" in pretty
    assert code in pretty


def test_statements_brackets(setup_resources):
    """
    Test that the compile statements brackets print properly
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<statements>" in pretty


def test_let_statements_brackets(setup_resources):
    """
    Test that the letStatement prints properly.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code="""      </varDec>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier> game </identifier>
"""

    pretty = write_xml(setup_resources)

    assert "<letStatement>" in pretty
    assert code in pretty


def test_compile_expression(setup_resources):
    """
    Test that when we run compile, an expression bracket is printed.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<expression>" in pretty
    assert "</expression>" in pretty


def test_compile_term(setup_resources):
    """
    Test that when we run compile, term is written properly
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<term>" in pretty


def test_compile_term_full(setup_resources):
    """
    Test that when we run compile, the full term and expression are written properly.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """              <expressionList></expressionList>
              <symbol> ) </symbol>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>"""

    pretty = write_xml(setup_resources)

    assert "<term>" in pretty
    assert code in pretty


def test_do_statement(setup_resources):
    """
    Test that when we run compile, the doStatement tag writes properly
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<doStatement>" in pretty


def test_full_do_statement(setup_resources):
    """
    Test that when we run compile, the doStatement fully compiles
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """        <doStatement>
          <keyword> do </keyword>
          <identifier> game </identifier>
          <symbol> . </symbol>
          <identifier> dispose </identifier>
          <symbol> ( </symbol>
          <expressionList></expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>"""

    pretty = write_xml(setup_resources)

    assert "<doStatement>" in pretty
    assert code in pretty


def test_while_statement(setup_resources):
    """
    Test that when we run compile, it prints the while statement brackets
    """
    jack_file: Path = Path(r"F:\Programming\Hack and ASM Projects\JackCompiler\input\ArrayTest\Main.jack")
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<whileStatement>" in pretty



def test_return_statement(setup_resources):
    """
    Test that when we run compile, it prints the <return> brackets
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<returnStatement>" in pretty


def test_full_return_statement(setup_resources):
    """
    Test that when we run compile, it compiles a full return statement
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>"""

    pretty = write_xml(setup_resources)

    assert "<returnStatement>" in pretty
    assert code in pretty


def test_full_function_subroutine_dec(setup_resources):
    """
    Test that our subroutine properly converts without any extra tokens.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList></parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier> SquareGame </identifier>
        <identifier> game </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier> game </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier> SquareGame </identifier>
              <symbol> . </symbol>
              <identifier> new </identifier>
              <symbol> ( </symbol>
              <expressionList></expressionList>
              <symbol> ) </symbol>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> game </identifier>
          <symbol> . </symbol>
          <identifier> run </identifier>
          <symbol> ( </symbol>
          <expressionList></expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> game </identifier>
          <symbol> . </symbol>
          <identifier> dispose </identifier>
          <symbol> ( </symbol>
          <expressionList></expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>"""
    pretty = write_xml(setup_resources)

    assert "<returnStatement>" in pretty
    assert code in pretty


def test_if_statement(setup_resources):
    """
    Test that when we compile, it properly handles the ifStatement.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<ifStatement>" in pretty


def test_full_if_statement(setup_resources):
    """
    Test that when we compile, it properly compiles a full ifStatement.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """      <statements>
        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <keyword> false </keyword>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> s </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <stringConstant> string constant </stringConstant>
                </term>
              </expression>"""

    pretty = write_xml(setup_resources)

    assert "<ifStatement>" in pretty
    assert code in pretty


def test_string_constant(setup_resources):
    """
    Test that when we compile, stringConstants are handled properly within term.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<stringConstant>" in pretty
    assert "string constant" in pretty


def test_full_string_constant(setup_resources):
    """
    Test that when we compile, the full string constants are printed at the right level.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """              <expression>
                <term>
                  <stringConstant> string constant </stringConstant>
                </term>
              </expression>
              <symbol> ; </symbol>"""

    pretty = write_xml(setup_resources)

    assert "<stringConstant>" in pretty
    assert "string constant" in pretty


def test_keyword_constant(setup_resources):
    """
    Test that when we compile, we see "null" print at the right level.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "null" in pretty


def test_full_keyword_constant(setup_resources):
    """
    Test that when we run the compiler, the keyword Constant part of the term compiles properly.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code = """              <expression>
                <term>
                  <keyword> null </keyword>
                </term>
              </expression>
              <symbol> ; </symbol>"""

    pretty = write_xml(setup_resources)

    assert "<keyword>" in pretty
    assert code in pretty


def test_integer_constant(setup_resources):
    """
    Test that when we compile, stringConstants are handled properly within term.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<integerConstant>" in pretty
    assert "2" in pretty


def test_symbols(setup_resources):
    """
    Test that when we compile, the symbols compile properly.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    pretty = write_xml(setup_resources)

    assert "<symbol>" in pretty

def test_full_if(setup_resources):
    """
    Test that when we compile, we compile the proper whole letStatement.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()

    code="""        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <keyword> false </keyword>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> s </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <stringConstant> string constant </stringConstant>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> s </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <keyword> null </keyword>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> a </identifier>
              <symbol> [ </symbol>
              <expression>
                <term>
                  <integerConstant> 1 </integerConstant>
                </term>
              </expression>
              <symbol> ] </symbol>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> a </identifier>
                  <symbol> [ </symbol>
                  <expression>
                    <term>
                      <integerConstant> 2 </integerConstant>
                    </term>
                  </expression>
                  <symbol> ] </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
          </statements>
          <symbol> } </symbol>
          <keyword> else </keyword>
          <symbol> { </symbol>
          <statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> i </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
                <symbol> * </symbol>
                <term>
                  <symbol> ( </symbol>
                  <expression>
                    <term>
                      <symbol> - </symbol>
                      <term>
                        <identifier> j </identifier>
                      </term>
                    </term>
                  </expression>
                  <symbol> ) </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> j </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> j </identifier>
                </term>
                <symbol> / </symbol>
                <term>
                  <symbol> ( </symbol>
                  <expression>
                    <term>
                      <symbol> - </symbol>
                      <term>
                        <integerConstant> 2 </integerConstant>
                      </term>
                    </term>
                  </expression>
                  <symbol> ) </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> i </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
                <symbol> | </symbol>
                <term>
                  <identifier> j </identifier>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
          </statements>
          <symbol> } </symbol>
        </ifStatement>"""

    pretty = write_xml(setup_resources)

    assert code in pretty


def test_full_compilation_square(setup_resources):
    """
    Tests that the full file Main.jack, our testing file, compiles fully.
    """
    compilation = setup_resources["compilation"]
    compilation.compile_class()


    code="""<class>
  <keyword> class </keyword>
  <identifier> Main </identifier>
  <symbol> { </symbol>
  <classVarDec>
    <keyword> static </keyword>
    <keyword> boolean </keyword>
    <identifier> test </identifier>
    <symbol> ; </symbol>
  </classVarDec>
  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> main </identifier>
    <symbol> ( </symbol>
    <parameterList></parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <identifier> SquareGame </identifier>
        <identifier> game </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <letStatement>
          <keyword> let </keyword>
          <identifier> game </identifier>
          <symbol> = </symbol>
          <expression>
            <term>
              <identifier> SquareGame </identifier>
              <symbol> . </symbol>
              <identifier> new </identifier>
              <symbol> ( </symbol>
              <expressionList></expressionList>
              <symbol> ) </symbol>
            </term>
          </expression>
          <symbol> ; </symbol>
        </letStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> game </identifier>
          <symbol> . </symbol>
          <identifier> run </identifier>
          <symbol> ( </symbol>
          <expressionList></expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <doStatement>
          <keyword> do </keyword>
          <identifier> game </identifier>
          <symbol> . </symbol>
          <identifier> dispose </identifier>
          <symbol> ( </symbol>
          <expressionList></expressionList>
          <symbol> ) </symbol>
          <symbol> ; </symbol>
        </doStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <subroutineDec>
    <keyword> function </keyword>
    <keyword> void </keyword>
    <identifier> more </identifier>
    <symbol> ( </symbol>
    <parameterList></parameterList>
    <symbol> ) </symbol>
    <subroutineBody>
      <symbol> { </symbol>
      <varDec>
        <keyword> var </keyword>
        <keyword> int </keyword>
        <identifier> i </identifier>
        <symbol> , </symbol>
        <identifier> j </identifier>
        <symbol> ; </symbol>
      </varDec>
      <varDec>
        <keyword> var </keyword>
        <identifier> String </identifier>
        <identifier> s </identifier>
        <symbol> ; </symbol>
      </varDec>
      <varDec>
        <keyword> var </keyword>
        <identifier> Array </identifier>
        <identifier> a </identifier>
        <symbol> ; </symbol>
      </varDec>
      <statements>
        <ifStatement>
          <keyword> if </keyword>
          <symbol> ( </symbol>
          <expression>
            <term>
              <keyword> false </keyword>
            </term>
          </expression>
          <symbol> ) </symbol>
          <symbol> { </symbol>
          <statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> s </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <stringConstant> string constant </stringConstant>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> s </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <keyword> null </keyword>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> a </identifier>
              <symbol> [ </symbol>
              <expression>
                <term>
                  <integerConstant> 1 </integerConstant>
                </term>
              </expression>
              <symbol> ] </symbol>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> a </identifier>
                  <symbol> [ </symbol>
                  <expression>
                    <term>
                      <integerConstant> 2 </integerConstant>
                    </term>
                  </expression>
                  <symbol> ] </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
          </statements>
          <symbol> } </symbol>
          <keyword> else </keyword>
          <symbol> { </symbol>
          <statements>
            <letStatement>
              <keyword> let </keyword>
              <identifier> i </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
                <symbol> * </symbol>
                <term>
                  <symbol> ( </symbol>
                  <expression>
                    <term>
                      <symbol> - </symbol>
                      <term>
                        <identifier> j </identifier>
                      </term>
                    </term>
                  </expression>
                  <symbol> ) </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> j </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> j </identifier>
                </term>
                <symbol> / </symbol>
                <term>
                  <symbol> ( </symbol>
                  <expression>
                    <term>
                      <symbol> - </symbol>
                      <term>
                        <integerConstant> 2 </integerConstant>
                      </term>
                    </term>
                  </expression>
                  <symbol> ) </symbol>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
            <letStatement>
              <keyword> let </keyword>
              <identifier> i </identifier>
              <symbol> = </symbol>
              <expression>
                <term>
                  <identifier> i </identifier>
                </term>
                <symbol> | </symbol>
                <term>
                  <identifier> j </identifier>
                </term>
              </expression>
              <symbol> ; </symbol>
            </letStatement>
          </statements>
          <symbol> } </symbol>
        </ifStatement>
        <returnStatement>
          <keyword> return </keyword>
          <symbol> ; </symbol>
        </returnStatement>
      </statements>
      <symbol> } </symbol>
    </subroutineBody>
  </subroutineDec>
  <symbol> } </symbol>
</class>"""

    pretty = write_xml(setup_resources)

    assert code in pretty
