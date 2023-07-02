from _parser import MoshoParser
from scanner import MoshoScanner


def repl():
    context = {}
    while True:
        source = input("-- mosho --> ")
        if source:
            tokens = MoshoScanner(source).scan()
            tree = MoshoParser(tokens).parse()
            for result in tree.eval(context):
                if result:
                    print(result)


if __name__ == "__main__":
    repl()
