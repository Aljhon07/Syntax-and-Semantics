# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis

INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'


class Token:
    def __init__(self, type, value):
        # Token type: INTEGER, PLUS, MINUS, or EOF
        self.type = type
        # Token value: non-negative integer, '+', '-', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        """
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()


class Interpreter:
    def __init__(self, text):
        # Client string input, e.g., "3 + 5", "12 - 5 + 3", etc.
        self.text = text
        # Index into self.text
        self.pos = 0
        # Current token instance
        self.current_token = None
        # Current character
        self.current_char = self.text[self.pos]

    # Lexer code
    def error(self):
        raise Exception('Invalid syntax')

    def advance(self):
        """Advance the 'pos' pointer and update 'current_char'."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        """Skip whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multi-digit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer).
        This method breaks a sentence into tokens one at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            self.error()

        return Token(EOF, None)

    # Parser / Interpreter code
    def eat(self, token_type):
        """Compare the current token type with the expected type.
        If they match, move to the next token; otherwise, raise an error.
        """
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """Return an INTEGER token value."""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """Arithmetic expression parser / interpreter."""
        # Get the first token
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            elif token.type == MINUS:
                self.eat(MINUS)
                result = result - self.term()

        return result


def main():
    while True:
        try:
            # To run under Python3, use 'input' instead of 'raw_input'
            text = input('calc> ')  # Fixed 'raw_input' to 'input'
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
