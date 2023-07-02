import enum

class TokenType(enum.Enum):
	IF = "if"
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

class Token():
	def __init__(self, type, value=None):
		self.type = type if  isinstance(type, TokenType) else TokenType(type)
		self.value = value
	
	def is_(self, type):
		return type == self.type

	def __repr__(self):
		result = str(self.type)
		if self.value:
			result += f" {self.value}"
		return result
