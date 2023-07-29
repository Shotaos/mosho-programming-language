from scanner import TokenType


class TreeNode:
    def eval(self, *args, **kwargs):
        raise NotImplementedError()


class Root(TreeNode):
    def __init__(self, child=None):
        self.children = [] if child is None else [child]

    def add(self, node):
        self.children.append(node)

    def eval(self, context):
        results = []
        for child in self.children:
            results.append(child.eval(context))
        return results


class If(TreeNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, context):
        if self.condition.eval(context):
            return self.body.eval(context)


class While(TreeNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def eval(self, context):
        while self.condition.eval(context):
            self.body.eval(context)


class Comparison(TreeNode):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def eval(self, context):
        left = self.left.eval(context)
        right = self.right.eval(context)

        if self.operation.is_(TokenType.GREATER):
            return left > right
        elif self.operation.is_(TokenType.GREATER_EQUAL):
            return left >= right
        elif self.operation.is_(TokenType.LESS):
            return left < right
        elif self.operation.is_(TokenType.LESS_EQUAL):
            return left <= right
        elif self.operation.is_(TokenType.EQUAL_EQUAL):
            return left == right

        raise ValueError("Invalid operation")


class Body(TreeNode):
    def __init__(self, children=None):
        self.children = children if children else list()

    def eval(self, context):
        results = []
        for child in self.children:
            results.append(child.eval(context))
        return results

    def add(self, node):
        self.children.append(node)


class Statement(TreeNode):
    def __init__(self, child):
        self.child = child

    def eval(self, context):
        return self.child.eval(context)


class Assignment(TreeNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self, context):
        context[self.left.value] = self.right.eval(context)


class Expression(TreeNode):
    def __init__(self, child):
        self.child = child

    def eval(self, context):
        return self.child.eval(context)


class Term(TreeNode):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def eval(self, context):
        left = self.left.eval(context)
        right = self.right.eval(context)

        if self.operation.is_(TokenType.PLUS):
            return left + right
        elif self.operation.is_(TokenType.MINUS):
            return left - right

        raise ValueError("Invalid operation")


class Factor(TreeNode):
    def __init__(self, left, operation, right):
        self.left = left
        self.operation = operation
        self.right = right

    def eval(self, context):
        left = self.left.eval(context)
        right = self.right.eval(context)

        if self.operation.is_(TokenType.MULTIPLY):
            return left * right
        elif self.operation.is_(TokenType.DIVIDE):
            return left / right

        raise ValueError("Invalid operation")


class Grouping(TreeNode):
    def __init__(self, child):
        self.child = child

    def eval(self, context):
        return self.child.eval(context)


class Literal(TreeNode):
    def __init__(self, child):
        self.child = child

    def eval(self, context):
        if self.child.is_(TokenType.FLOAT) or self.child.is_(TokenType.INTEGER):
            return self.child.value

        if self.child.is_(TokenType.VARIABLE):
            return context[self.child.value]


class FunctionCall(TreeNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def eval(self, context):
        if self.name.value != "print":
            raise ValueError("Invalid function call")

        for arg in self.args:
            print(arg.eval(context))
