import sys
from _parser import MoshoParser
from scanner import MoshoScanner


def repl():
    context = {}
    while True:
        source = input("-- mosho --> ")
        if source:
            tokens = MoshoScanner(source).scan()
            tree = MoshoParser(tokens).parse()
            tree.eval(context)


def interpret_file(filename):
    context = {}
    source = open(filename, "r").read()
    tokens = MoshoScanner(source).scan()
    tree = MoshoParser(tokens).parse()
    tree.eval(context)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        interpret_file(sys.argv[1])
    else:
        repl()
