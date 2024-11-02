import enum
import re

# Token class represents a token in the lexer
class Token:
    def __init__(self, line, column, type, lexeme):
        self.line = line
        self.column = column
        self.type = type
        self.lexeme = lexeme

    def __repr__(self) -> str:
        return f"Token({self.line}, {self.column}, {self.type}, {self.lexeme})"

# List of token names
names = [
    'BraceL', 'BraceR', 'ParenL', 'ParenR', 'BracketL', 'BracketR', 'Equal',
    'Plus', 'Sub', 'Multiplie', 'Div', 'Rem', 'Pow', 'Sen', 'Cos', 'Tan',
    'Log', 'Exp', 'Sqrt', 'Abs', 'Number', 'Var',
]

# Create an enum class for the token types
Terminal = enum.Enum('Terminal', names)

# Dictionary mapping symbols to their corresponding token types
sym2tk = {
    '{': Terminal.BraceL,
    '}': Terminal.BraceR,
    '(': Terminal.ParenL,
    ')': Terminal.ParenR,
    '[': Terminal.BracketL,
    ']': Terminal.BracketR,
    '=': Terminal.Equal,
    '+': Terminal.Plus,
    '-': Terminal.Sub,
    '*': Terminal.Multiplie,
    '/': Terminal.Div,
    '%': Terminal.Rem,
    '^': Terminal.Pow,
}

# Dictionary mapping keywords to their corresponding token types
kw2tk = {
    'sen' : Terminal.Sen,
    'cos' : Terminal.Cos,
    'tan' : Terminal.Tan,
    'log' : Terminal.Log,
    'exp' : Terminal.Exp,
    'sqrt' : Terminal.Sqrt,
    'abs' : Terminal.Abs,
}

# List of escaped symbols
escaped = [''.join(['\\' + char if char in re.escape(char) else char for char in k]) for k in sym2tk.keys()]

# Regular expression pattern for symbols
symbols = re.compile('|'.join(escaped))

# Regular expression pattern for numbers
number = re.compile(r'[0-9]+|[0-9]*\.[0-9]+')

# Regular expression pattern for identifiers
vars = re.compile(r'[a-zA-Z]*')

# Tokenize the input string
def tokenize(input):
    tokens = []
    input = input.rstrip()

    line = 1
    column = 1

    while len(input):
        # Skip whitespace characters
        while input[0].isspace():
            if input[0] == '\n':
                line += 1
                column = 1
            else:
                column += 1
            input = input[1:]

        # Match symbols
        match = symbols.match(input)
        if match:
            lexeme = match.group(0)
            tokens.append(Token(line, column, sym2tk[lexeme], lexeme))
            column += len(lexeme)
            input = input[len(lexeme):]
            continue

        # Match numbers
        match = number.match(input)
        if match:
            lexeme = match.group(0)
            tokens.append(Token(line, column, Terminal.Number, lexeme))
            column += len(lexeme)
            input = input[len(lexeme):]
            continue

        # Match variables
        match = vars.match(input)
        if match:
            lexeme = match.group(0)
            if lexeme in kw2tk.keys():
                tokens.append(Token(line, column, kw2tk[lexeme], lexeme))
            else:
                tokens.append(Token(line, column, Terminal.Var, lexeme))
            column += len(lexeme)
            input = input[len(lexeme):]
            continue

        # Raise syntax error for invalid syntax
        raise SyntaxError(f'Invalid syntax at {line}:{column}')

    # Append end-of-file token
    tokens.append(Token(line, column, 0, '$'))
    return tokens

