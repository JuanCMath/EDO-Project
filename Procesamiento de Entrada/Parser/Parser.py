import Nodes

class Parse:
    def __init__(self, tokens):
        self.currentIndex = 0
        self.tokens = tokens
        self.defaultprecedence = {
            'Plus': 3,
            'Sub': 3,
            'ParenL': 5,
            'BraceL': 5,
            'BracketL': 5,
            'Multiplie': 4,
            'Div': 4,
            'Pow': 5,
            'Rem': 4,
            'sen': 5,
            'cos': 5,
            'tan': 5,
            'log': 5,
            'exp': 5,
            'sqrt': 5,
            'abs': 5,
        }

    def Parse(self):
        return self.ParseEcuation()


    def ParseEquation(self, precedence=0):
        Left = self.ParseExpression(precedence)
        self.currentIndex += 1
        Right = self.ParseExpression(precedence)

        return Nodes.EquationDeclaration(Left, Right)

    def ParseExpression(self, precedence=0):
        return self.ParseBinaryExpression(precedence)

    def ParseBinaryExpression(self, minPrecedence):
        left = self.ParseUnaryExpression()

        while True:
            op = self.tokens[self.currentIndex]
            opType = op.type

            if opType not in self.defaultprecedence or self.defaultprecedence[opType] < minPrecedence or opType == 'Equal':
                return left

            else:
                self.currentIndex += 1
                right = self.ParseExpression(self.defaultprecedence[opType] + 1)
                left = Nodes.BinaryExpressionNode(left, op, right)


    def ParseUnaryExpression(self):
        if self.tokens[self.currentIndex + 1].type == 'MinusOne':
            exp = self.ParsePrimaryExpression()
            op = self.Expect('MinusOne')
            return Nodes.UnaryExpressionNode(op, exp)
        else:
            return self.ParsePrimaryExpression()

    def ParsePrimaryExpression(self):
        if self.Match('Number'):
            return Nodes.NumberNode(self.ExpectNumber())
        
        elif self.Match('ParenL'):
            self.Expect('ParenL')
            exp = self.ParseExpression()
            self.Expect('ParenR')
            return Nodes.GroupingNode(exp)
        
        elif self.ExpectFunction():
            op = self.Peek()

            self.Expect('ParenL')
            body = self.ParseExpression(0)
            self.Expect('ParenR')

            return Nodes.FunctionNode(op.lexeme, body)
        
        elif self.Match('Var'):
            identifier = self.Expect('Var')
            return Nodes.VariableNode(identifier.lexeme)
        
        else:
            raise Exception(f"Expected expression but got {self.Peek().type} ({self.Peek().lexeme})")




    def Match(self, type):
        if (self.currentIndex >= len(self.tokens)):
            raise Exception("Unexpected end of input")
        
        return self.Peek().type == type

    def Peek(self):
        if (self.currentIndex >= len(self.tokens)):
            raise Exception("Unexpected end of input")
        
        self.currentIndex += 1
        return self.tokens[self.currentIndex - 1]
    
    def Expect(self, tokentype):
        if (self.currentIndex >= len(self.tokens)):
            raise Exception("Unexpected end of input")
        
        token = self.tokens[self.currentIndex]
        
        if token.type == tokentype:
            self.currentIndex += 1
            return token
        else:
            raise Exception(f"Expected {token} but got {self.Peek().type} ({self.Peek().lexeme})")
        
    def ExpectNumber(self):
        if (self.currentIndex >= len(self.tokens)):
            raise Exception("Unexpected end of input")
        
        if self.tokens[self.currentIndex].type == 'Number':
            self.currentIndex += 1
            return int(self.tokens[self.currentIndex].lexeme)
        else:
            raise Exception(f"Expected number but got {self.Peek().type} ({self.Peek().lexeme})")

    def ExpectFunction(self):
        if (self.currentIndex >= len(self.tokens)):
            raise Exception("Unexpected end of input")
        
        opType = self.tokens[self.currentIndex].type
        if opType == 'sen' or opType == 'cos' or opType == 'tan' or opType == 'log' or opType == 'exp' or opType == 'sqrt' or opType == 'abs':
            self.currentIndex += 1
            return True
        return 