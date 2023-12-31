from syntax_tree import (
    Root,
    Statement,
    Assignment,
    Expression,
    Factor,
    Term,
    Body,
    Grouping,
    Literal,
    If,
    While,
    Comparison,
    FunctionCall,
    FunctionDefinition,
)
from scanner import TokenType


# Grammar
#   ROOT -> EXPRESSION | STATEMENT
#   FUNCTION -> mosho (VARIABLE,) { EXPRESSION }
#   STATEMENT -> ASSIGNMENT | IF
#   ASSIGNMENT -> VARIABLE = EXPRESSION
#   IF -> if EXPRESSION BODY
#   WHILE -> while EXPRESSION BODY
#   BODY ->  { (EXPRESSION | ASSIGNMENT)* }
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

    def next_token_is_statement(self):
        return self.peek(1).is_(TokenType.ASSIGNMENT) or self.peek().is_(
            TokenType.IF, TokenType.WHILE, TokenType.MOSHO
        )

    def root(self):
        root = Root()

        while not self.peek().is_(TokenType.EOF):
            if self.next_token_is_statement():
                root.add(self.statement())
            else:
                root.add(self.expression())

        return root

    def statement(self):
        if self.peek(0).is_(TokenType.IF):
            return Statement(self.if_())
        elif self.peek().is_(TokenType.WHILE):
            return Statement(self.while_())
        elif self.peek().is_(TokenType.MOSHO):
            return Statement(self.function_definition())
        return Statement(self.assignment())

    def if_(self):
        assert self.advance().is_(TokenType.IF)
        condition = self.expression()
        body = self.body()
        return If(condition, body)

    def while_(self):
        assert self.advance().is_(TokenType.WHILE)
        condition = self.expression()
        body = self.body()
        return While(condition, body)

    def body(self):
        result = Body()
        assert self.advance().is_(TokenType.LEFT_CURLY_BRACE)
        while not self.peek().is_(TokenType.RIGHT_CURLY_BRACE):
            if self.next_token_is_statement():
                result.add(self.statement())
            else:
                result.add(self.expression())

        assert self.advance().is_(TokenType.RIGHT_CURLY_BRACE)
        return result

    def assignment(self):
        left = self.advance()
        assert self.advance().is_(TokenType.ASSIGNMENT)
        right = self.expression()
        return Assignment(left, right)

    def expression(self):
        return Expression(self.comparison())

    def comparison(self):
        result = self.term()

        while self.peek().is_(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
        ):
            operation = self.advance()
            right = self.term()
            result = Comparison(result, operation, right)

        return result

    def term(self):
        result = self.factor()

        while self.peek().is_(TokenType.PLUS, TokenType.MINUS):
            operation = self.advance()
            right = self.factor()
            result = Term(result, operation, right)

        return result

    def factor(self):
        result = self.grouping()

        while self.peek().is_(TokenType.MULTIPLY, TokenType.DIVIDE):
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
        if self.peek().is_(TokenType.VARIABLE) and self.peek(1).is_(
            TokenType.LEFT_PAREN
        ):
            return self.function_call()
        return Literal(self.advance())

    def function_call(self):
        name = self.advance()
        args = []
        assert self.advance().is_(TokenType.LEFT_PAREN)
        while not self.peek().is_(TokenType.RIGHT_PAREN):
            args.append(self.expression())

        assert self.advance().is_(TokenType.RIGHT_PAREN)

        return FunctionCall(name, args)

    def function_definition(self):
        args = []
        body = []
        assert self.advance().is_(TokenType.MOSHO)
        name = self.advance()
        assert self.advance().is_(TokenType.COLON)

        while not self.peek().is_(TokenType.LEFT_CURLY_BRACE):
            args.append(self.advance())

        assert self.advance().is_(TokenType.LEFT_CURLY_BRACE)
        while not self.peek().is_(TokenType.RIGHT_CURLY_BRACE):
            if self.next_token_is_statement():
                body.append(self.statement())
            else:
                body.append(self.expression())
        assert self.advance().is_(TokenType.RIGHT_CURLY_BRACE)

        return FunctionDefinition(name, args, body)
