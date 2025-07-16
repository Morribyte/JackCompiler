"""
jack_analyzer.py
Opens and writes XML files for the compiler.
"""

from pathlib import Path
import sys
import xml.etree.ElementTree as element_tree

from src.tokenizer import Tokenizer
from src.compilation_engine import CompilationEngine


def check_args():
    if len(sys.argv) < 2:
        print("Usage: python jack_analyzer.py <input path>")
        sys.exit(1)
    path = Path(sys.argv[1])
    print(f"Current path: {path}")
    return path


def check_files(path) -> list[str]:
    if path.is_dir():
        print("Found directory:")
        files = [f for f in path.glob("*.jack")]
        print(files)
    elif path.is_file() and path.suffix == ".jack":
        print("Found file:")
        files = [path]
        print(files)
    else:
        raise ValueError("Invalid input: must be a .jack file or a directory containing .jack files.")

    return files


def main():
    """
    Handles the main compiler loop.
    """

    path = check_args()
    files = check_files(path)

    for jack_files in files:
        file_path = Path(jack_files)
        starting_path = fr"{file_path.parent.parent}"
        output_path = Path(fr"output\{file_path.parent.name}")
        print(starting_path)
        tokenizer = Tokenizer(jack_files)
        compiler = CompilationEngine(tokenizer)

        compiler.compile_class()

        tree = element_tree.ElementTree(compiler.root)
        element_tree.indent(tree)
        output_path.mkdir(parents=True, exist_ok=True)
        tree.write(fr"{output_path}\{file_path.stem}.xml", encoding="utf-8", short_empty_elements=False)
        xml_str = element_tree.tostring(compiler.root, encoding="unicode", method="html")

        print("XML file parsed and formatted.")

if __name__ == "__main__":
    main()
