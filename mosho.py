# Grammar
#   E -> T
#   T -> T + F | T - F
#   T -> F
#   F -> F * G | F / G
#   G -> ( E ) | N
#   N -> 0 1 2 3 4 5 6 7 8 9 


class MoshoScanner:
    def __init__(self, data):
        self.data = data
        self.i = 0
    
    def peek(self, forward=1):
        if len(self.data) > self.i + forward:
            return self.data[self.i + forward]
    
    def curr(self):
        return self.peek(0)

    def advance(self):
        res = self.data[self.i]
        self.i += 1
        return res

    def scan(self):
        result = []
        while self.curr() is not None:
            if self.curr().isdigit():
                result.append(self.number())
            elif self.curr() in "()+-*/":
                result.append(self.advance())
            elif self.curr().isspace():
                self.advance()
        
        return result

    def number(self):
        digits = []
        while self.curr() and (self.curr().isdigit() or self.curr() == "."):
            digits.append(self.advance())
        return float(''.join(digits))


class MoshoParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self, forward=0):
        if len(self.tokens) > self.i + forward:
            return self.tokens[self.i + forward]

    def advance(self):
        res = self.tokens[self.i]
        self.i += 1
        return res

    @staticmethod
    def create_node(type, value=None, op=None, children=list()):
        result = {"name": type}
        if children:
            result["children"] = [c for c in children if c is not None]
        
        if value is not None:
            result["value"] = value
        
        if op is not None:
            result["op"] = op

        return result

    def parse(self):
        return self.create_node("ROOT", children=[self.term()])
    
    def term(self):
        result = self.factor()

        while self.peek() in ("+", "-"):
            op = self.advance()
            result = self.create_node("Term", op=op, children=[result, self.factor()])

        return result
        

    def factor(self):
        result = self.grouping()

        while self.peek() in ("*", "/"):
            op = self.advance()
            result = self.create_node("Factor", op=op, children=[result, self.grouping()])

        return result
    
    def grouping(self):
        if self.peek() == '(':
            self.advance()
            term = self.term()
            if self.peek() != ')':
                raise ValueError("value error")

            self.advance()
            return term

        return self.literal()

    def literal(self):
        return self.create_node("Literal", value=float(self.advance()))


def evaluate(tree):
    if tree.get("value") is not None:
        return
    
    for c in tree["children"]:
        if c.get("value") is None:
            evaluate(c)
    
    if tree["name"] in ("Term", "Factor"):
        a, b = [n["value"] for n in tree["children"]]
        if tree["op"] == "+":
            tree["value"] = a + b
        elif tree["op"] == "-":
            tree["value"] = a - b
        elif tree["op"] == "*":
            tree["value"] = a * b
        elif tree["op"] == "/":
            tree["value"] = a / b

    elif tree["name"] == "ROOT":
        tree["value"] = tree["children"][0]["value"]

    return tree["value"]


if __name__ == '__main__':
    while True:
        tokens = MoshoScanner(input("-> ")).scan()
        tree = MoshoParser(tokens).parse()
        print("Result:", evaluate(tree))