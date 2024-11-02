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
    'Semicolon', 'BraceL', 'BraceR', 'ParenL', 'ParenR', 'BracketL', 'BracketR', 'Comma', 'Equal',
    'Plus', 'Sub', 'Star', 'Div', 'Rem', 'Pow', 'Dot', 'Colon', 'At', 'And', 'Or', 'Not',
    'GreaterThan', 'LessThan', 'New', 'As', 'Function', 'Let', 'In', 'If', 'Elif', 'Else', 'true',
    'false', 'Is', 'While', 'For', 'Type', 'Inherit', 'Protocol', 'Extends', 'Comprehension', 'Number',
    'Identifier', 'String'
]

# Create an enum class for the token types
Terminal = enum.Enum('Terminal', names)

# Dictionary mapping symbols to their corresponding token types
sym2tk = {
    ';': Terminal.Semicolon,
    '{': Terminal.BraceL,
    '}': Terminal.BraceR,
    '(': Terminal.ParenL,
    ')': Terminal.ParenR,
    '[': Terminal.BracketL,
    ']': Terminal.BracketR,
    ',': Terminal.Comma,
    '=': Terminal.Equal,
    '+': Terminal.Plus,
    '-': Terminal.Sub,
    '*': Terminal.Star,
    '/': Terminal.Div,
    '%': Terminal.Rem,
    '^': Terminal.Pow,
    '.': Terminal.Dot,
    ':': Terminal.Colon,
    '@': Terminal.At,
    '&': Terminal.And,
    '|': Terminal.Or,
    '||': Terminal.Comprehension,
    '!': Terminal.Not,
    '>': Terminal.GreaterThan,
    '<': Terminal.LessThan,
}

# Dictionary mapping keywords to their corresponding token types
kw2tk = {
    'new': Terminal.New,
    'as': Terminal.As,
    'function': Terminal.Function,
    'let': Terminal.Let,
    'in': Terminal.In,
    'if': Terminal.If,
    'elif': Terminal.Elif,
    'else': Terminal.Else,
    'true': Terminal.true,
    'false': Terminal.false,
    'is': Terminal.Is,
    'while': Terminal.While,
    'for': Terminal.For,
    'type': Terminal.Type,
    'inherits': Terminal.Inherit,
    'protocol': Terminal.Protocol,
    'extends': Terminal.Extends,
}

# List of escaped symbols
escaped = [''.join(['\\' + char if char in re.escape(char) else char for char in k]) for k in sym2tk.keys()]

# Regular expression pattern for symbols
symbols = re.compile('|'.join(escaped))

# Regular expression pattern for numbers
number = re.compile(r'[0-9]+|[0-9]*\.[0-9]+')

# Regular expression pattern for identifiers
identifier = re.compile(r'[_a-zA-Z][_a-zA-Z0-9]*')

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

        # Match identifiers
        match = identifier.match(input)
        if match:
            lexeme = match.group(0)
            if lexeme in kw2tk.keys():
                tokens.append(Token(line, column, kw2tk[lexeme], lexeme))
            else:
                tokens.append(Token(line, column, Terminal.Identifier, lexeme))
            column += len(lexeme)
            input = input[len(lexeme):]
            continue

        # Match strings
        if input[0] == '"':
            i = 1
            while input[i] != '"':
                if input[i] == '\\':
                    i += 1
                i += 1
            tokens.append(Token(line, column, Terminal.String, input[1:i]))
            column += i + 1
            input = input[i + 1:]
            continue

        # Skip comments
        if input[0] == '#':
            while input[0] != '\n':
                column += 1
                input = input[1:]
            continue

        # Raise syntax error for invalid syntax
        raise SyntaxError(f'Invalid syntax at {line}:{column}')

    # Append end-of-file token
    tokens.append(Token(line, column, 0, '$'))
    return tokens

