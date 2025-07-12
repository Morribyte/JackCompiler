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




if __name__ == "__main__":
    main()
