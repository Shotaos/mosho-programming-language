import string
from tree import Root, Statement, Assignment, Expression, Factor, Term, Literal
from _token import Token, TokenType

# Grammar
#   ROOT -> EXPRESSION | STATEMENT
#   STATEMENT -> ASSIGNMENT | IF
#   ASSIGNMENT -> VARIABLE = EXPRESSION
#   IF -> if EXPRESSION { EXPRESSION | ASSIGNMENT }
#   VARIABLE -> a-z
#   EXPRESSION -> TERM
#   TERM -> TERM + FACTOR | TERM - FACTOR
#   TERM -> FACTOR
#   FACTOR -> FACTOR * GROUP | FACTOR / GROUP
#   GROUP -> ( EXPRESSION ) | NUMBER | VARIABLE
#   NUMBER -> 0 1 2 3 4 5 6 7 8 9 


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
            elif self.curr() in "()+-*/=":
                result.append(Token(self.advance()))
            elif self.curr() in string.ascii_lowercase:
                result.append(Token(TokenType.VARIABLE, value=self.advance()))
            elif self.curr().isspace():
                self.advance()

        result.append(Token(TokenType.EOF)) 
        return result

    def number(self):
        digits = []
        while self.curr() and (self.curr().isdigit() or self.curr() == "."):
            digits.append(self.advance())
        return Token(TokenType.FLOAT, float(''.join(digits)))


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

    def parse(self):
        return self.root()
    
    def root(self):
        if self.peek(1).is_(TokenType.ASSIGNMENT):
            return Root(self.statement())

        return Root(self.expression())
    
    def statement(self):
        return Statement(self.assignment())

    def assignment(self):
        left = self.advance()

        if self.peek().is_(TokenType.ASSIGNMENT):
            self.advance()
        else:
            raise ValueError()
        
        right = self.expression()

        return Assignment(left, right)
    
    def expression(self):
        return Expression(self.term())

    def term(self):
        result = self.factor()

        while self.peek().is_(TokenType.PLUS) or self.peek().is_(TokenType.MINUS):
            operation = self.advance()
            right = self.factor()
            result = Term(result, operation, right)

        return result
        

    def factor(self):
        result = self.grouping()

        while self.peek().is_(TokenType.MULTIPLY) or self.peek().is_(TokenType.DIVIDE):
            operation = self.advance()
            right = self.grouping()
            result = Factor(result, operation, right)

        return result
    
    def grouping(self):
        if self.peek().is_(TokenType.LEFT_PAREN):
            self.advance()
            term = self.expression()
            if not self.peek().is_(TokenType.RIGHT_PAREN):
                raise ValueError("value error")

            self.advance()
            return term

        return self.literal()

    def literal(self):
        return Literal(self.advance())
    

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


if __name__ == '__main__':
    repl()