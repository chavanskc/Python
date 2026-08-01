from operations import add, subtract, multiply, divide


def _tokenize(expression: str):
    tokens = []
    i = 0
    n = len(expression)

    while i < n:
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch in "+-*/()":
            tokens.append(("OP", ch))
            i += 1
            continue

        if ch.isdigit() or ch == ".":
            j = i
            seen_dot = False
            while j < n and (expression[j].isdigit() or (expression[j] == "." and not seen_dot)):
                if expression[j] == ".":
                    seen_dot = True
                j += 1
            tokens.append(("NUMBER", float(expression[i:j])))
            i = j
            continue

        raise ValueError(f"Unexpected character '{ch}' in expression")

    return tokens


class _Parser:
    """Recursive-descent parser: expr := term (('+'|'-') term)*, term := factor (('*'|'/') factor)*"""

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _advance(self):
        token = self._peek()
        self.pos += 1
        return token

    def parse(self):
        result = self._expr()
        if self._peek() is not None:
            raise ValueError(f"Unexpected token '{self._peek()[1]}' in expression")
        return result

    def _expr(self):
        result = self._term()
        while self._peek() in (("OP", "+"), ("OP", "-")):
            _, op = self._advance()
            result = add(result, self._term()) if op == "+" else subtract(result, self._term())
        return result

    def _term(self):
        result = self._factor()
        while self._peek() in (("OP", "*"), ("OP", "/")):
            _, op = self._advance()
            result = multiply(result, self._factor()) if op == "*" else divide(result, self._factor())
        return result

    def _factor(self):
        token = self._peek()
        if token is None:
            raise ValueError("Unexpected end of expression")

        if token == ("OP", "-"):
            self._advance()
            return -self._factor()
        if token == ("OP", "+"):
            self._advance()
            return self._factor()

        if token == ("OP", "("):
            self._advance()
            result = self._expr()
            if self._peek() != ("OP", ")"):
                raise ValueError("Missing closing parenthesis")
            self._advance()
            return result

        if token[0] == "NUMBER":
            self._advance()
            return token[1]

        raise ValueError(f"Unexpected token '{token[1]}'")


def evaluate_expression(expression: str) -> float:
    tokens = _tokenize(expression)
    if not tokens:
        raise ValueError("Empty expression")
    return _Parser(tokens).parse()
