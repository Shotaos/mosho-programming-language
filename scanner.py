import string
import enum


class TokenType(enum.Enum):
    IF = "if"
    NEWLINE = "\n"
    INTEGER = enum.auto()
    FLOAT = enum.auto()
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    ASSIGNMENT = "="
    VARIABLE = enum.auto()
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    EOF = enum.auto()


class Token:
    def __init__(self, type, value=None):
        self.type = type if isinstance(type, TokenType) else TokenType(type)
        self.value = value

    def is_(self, type):
        return type == self.type

    def __repr__(self):
        result = str(self.type)
        if self.value:
            result += f" {self.value}"
        return result


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
            elif self.curr() in "()+-*/=\n":
                result.append(Token(self.advance()))
            elif self.curr() in string.ascii_lowercase:
                result.append(Token(TokenType.VARIABLE, value=self.advance()))
            elif self.curr().isspace():
                self.advance()
            else:
                raise ValueError(f"Invalid token: {self.curr()}")

        result.append(Token(TokenType.EOF))
        return result

    def number(self):
        digits = []
        while self.curr() and (self.curr().isdigit() or self.curr() == "."):
            digits.append(self.advance())
        return Token(TokenType.FLOAT, float("".join(digits)))
