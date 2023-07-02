from syntax_tree import (
    Root,
    Statement,
    Assignment,
    Expression,
    Factor,
    Term,
    Grouping,
    Literal,
)
from scanner import TokenType


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
            return Grouping(term)

        return self.literal()

    def literal(self):
        return Literal(self.advance())