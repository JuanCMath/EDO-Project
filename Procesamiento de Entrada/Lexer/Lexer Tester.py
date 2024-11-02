import unittest
from Lexer import tokenize, Token, Terminal

class TestLexer(unittest.TestCase):
    def test_tokenize(self):
        input_str = '3 + 4 * 10'
        expected_tokens = [
            Token(1, 1, Terminal.Number, '3'),
            Token(1, 3, Terminal.Plus, '+'),
            Token(1, 5, Terminal.Number, '4'),
            Token(1, 7, Terminal.Multiplie, '*'),
            Token(1, 9, Terminal.Number, '10'),
            Token(1, 11, 0, '$')
        ]
        result = tokenize(input_str)
        
        for token in result:
            print(token)
        

if __name__ == '__main__':
    unittest.main()