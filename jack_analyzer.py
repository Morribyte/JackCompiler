"""
jack_analyzer.py
Opens and writes XML files for the compiler.
"""

import os
import sys

def main():
    """
    Handles the main compiler loop.
    """
    if len(sys.argv) < 2:
        print("Usage: python jack_analyzer.py <input path>")
        sys.exit(1)

    path = sys.argv[1]

    print(f"Current path: {path}")

    if os.path.isdir(path):
        print("Found directory:")
        files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jack")]
        print(files)
    elif path.endswith(".jack"):
        print("Found file.")
        files = [path]
        print(files)
    else:
        raise ValueError("Invalid input: must be .jack file or directory.")
if __name__ == "__main__":
    main()
