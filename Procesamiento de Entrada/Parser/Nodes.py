class ASTNode:
    def get_children(self):
        return iter([])

class EcuationDeclaration(ASTNode):
    def __init__(self, Left, Right):
        self.Left = Left
        self.Right = Right
    
    def get_children(self):
        return iter([self.value])

class BinaryExpressionNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def get_children(self):
        return iter([self.left, self.right])

class UnaryExpressionNode(ASTNode):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def get_children(self):
        return iter([self.expression])

class FunctionNode(ASTNode):
    def __init__(self, name, body):
        self.name = name
        self.body = body
    
    def get_children(self):
        return iter([self.body])

class GroupingNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

    def get_children(self):
        return iter([self.expression])

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class VariableNode(ASTNode):
    def __init__(self, name):
        self.name = name

