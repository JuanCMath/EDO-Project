import Lexer

def test_tokenize():
    input_string = "let x = 10 + 20; if (x > 15) { x = x + 1; }" 
    expected_tokens = [
        Lexer.Token(1, 1, Lexer.Terminal.Let, 'let'),
        Lexer.Token(1, 5, Lexer.Terminal.Identifier, 'x'),
        Lexer.Token(1, 7, Lexer.Terminal.Equal, '='),
        Lexer.Token(1, 9, Lexer.Terminal.Number, '10'),
        Lexer.Token(1, 12, Lexer.Terminal.Plus, '+'),
        Lexer.Token(1, 14, Lexer.Terminal.Number, '20'),
        Lexer.Token(1, 16, Lexer.Terminal.Semicolon, ';'),
        Lexer.Token(1, 18, Lexer.Terminal.If, 'if'),
        Lexer.Token(1, 21, Lexer.Terminal.ParenL, '('),
        Lexer.Token(1, 22, Lexer.Terminal.Identifier, 'x'),
        Lexer.Token(1, 24, Lexer.Terminal.GreaterThan, '>'),
        Lexer.Token(1, 26, Lexer.Terminal.Number, '15'),
        Lexer.Token(1, 28, Lexer.Terminal.ParenR, ')'),
        Lexer.Token(1, 30, Lexer.Terminal.BraceL, '{'),
        Lexer.Token(1, 32, Lexer.Terminal.Identifier, 'x'),
        Lexer.Token(1, 34, Lexer.Terminal.Equal, '='),
        Lexer.Token(1, 36, Lexer.Terminal.Identifier, 'x'),
        Lexer.Token(1, 38, Lexer.Terminal.Plus, '+'),
        Lexer.Token(1, 40, Lexer.Terminal.Number, '1'),
        Lexer.Token(1, 41, Lexer.Terminal.Semicolon, ';'),
        Lexer.Token(1, 43, Lexer.Terminal.BraceR, '}'),
        Lexer.Token(1, 44, 0, '$')
    ]

    tokens = Lexer.tokenize(input_string)
    for token in tokens:
        print(token)

test_tokenize()