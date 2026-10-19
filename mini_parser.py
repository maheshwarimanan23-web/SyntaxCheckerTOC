"""
mini_parser.py -- Recursive descent parser for the Mini Language.

CFG (one function per non-terminal; the Python call stack plays the role of
the PDA stack):

    program    -> stmt_list EOF
    stmt_list  -> stmt stmt_list | epsilon
    stmt       -> assign | if_stmt | while_stmt | expr_stmt
    assign     -> IDENT ASSIGN expr
    if_stmt    -> IF cond THEN stmt_list [ELSE stmt_list] END
    while_stmt -> WHILE cond DO stmt_list END
    expr_stmt  -> expr
    cond       -> expr COMP expr
    expr       -> term ((PLUS | MINUS) term)*
    term       -> factor ((STAR | SLASH) factor)*
    factor     -> NUMBER | IDENT | LPAREN expr RPAREN | MINUS factor

The grammar is LL(1) except that a statement starting with IDENT needs one
extra token of lookahead (IDENT ASSIGN => assign, otherwise expr_stmt).
"""

from tokenizer import tokenize, LexError


class SyntaxErr(Exception):
    def __init__(self, message, line, col, hint=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col
        self.hint = hint


class Node:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

    def pretty(self, indent=0):
        out = "  " * indent + self.label + "\n"
        for c in self.children:
            out += c.pretty(indent + 1)
        return out


HINTS = {
    "assign": "<identifier> = <expression>",
    "if": "if <condition> then <statements> [else <statements>] end",
    "while": "while <condition> do <statements> end",
    "cond": "<expression> <comparison> <expression>, e.g. x > 3",
    "expr": "an expression is built from numbers, variables, + - * / and ( )",
}

STMT_START = {"IDENT", "NUMBER", "LPAREN", "MINUS", "IF", "WHILE"}


def describe(tok):
    if tok.type == "EOF":
        return "end of input"
    return repr(tok.text)


class Parser:
    def __init__(self, tokens):
        self.toks = tokens
        self.pos = 0

    # ---- helpers ----------------------------------------------------------
    @property
    def cur(self):
        return self.toks[self.pos]

    def peek(self, k=1):
        return self.toks[min(self.pos + k, len(self.toks) - 1)]

    def advance(self):
        t = self.cur
        if t.type != "EOF":
            self.pos += 1
        return t

    def error(self, message, hint=None, tok=None):
        tok = tok or self.cur
        raise SyntaxErr(message, tok.line, tok.col, hint)

    def expect(self, ttype, what, hint=None):
        if self.cur.type != ttype:
            self.error(f"Expected {what}, found {describe(self.cur)}", hint)
        return self.advance()

    # ---- grammar ----------------------------------------------------------
    def program(self):
        body = self.stmt_list(stop=())
        if self.cur.type == "END":
            self.error("Unexpected 'end' with no matching 'if' or 'while'",
                       "every 'end' must close an 'if' or 'while' block")
        if self.cur.type == "ELSE":
            self.error("Unexpected 'else' with no matching 'if'",
                       HINTS["if"])
        return Node("program", body)

    def stmt_list(self, stop):
        stmts = []
        while self.cur.type not in stop and self.cur.type != "EOF" \
                and self.cur.type not in ("END", "ELSE"):
            stmts.append(self.stmt())
        return stmts

    def stmt(self):
        t = self.cur
        if t.type == "IF":
            return self.if_stmt()
        if t.type == "WHILE":
            return self.while_stmt()
        if t.type == "IDENT" and self.peek().type == "ASSIGN":
            return self.assign()
        if t.type in STMT_START:
            return Node("expr_stmt", [self.expr()])
        self.error(f"Unexpected {describe(t)} at start of a statement",
                   "a statement starts with a variable, 'if', 'while' or an expression")

    def assign(self):
        name = self.advance()
        self.advance()  # '='
        if self.cur.type not in ("IDENT", "NUMBER", "LPAREN", "MINUS"):
            self.error(f"Expected an expression after '=', found {describe(self.cur)}",
                       HINTS["assign"])
        return Node("assign", [Node(f"IDENT {name.text}"), self.expr()])

    def if_stmt(self):
        kw = self.advance()
        cond = self.cond("if")
        if self.cur.type != "THEN":
            self.error(f"Expected 'then' after condition, found {describe(self.cur)}",
                       HINTS["if"])
        self.advance()
        then_body = self.stmt_list(())
        children = [Node("cond", [cond]), Node("then", then_body)]
        if self.cur.type == "ELSE":
            self.advance()
            children.append(Node("else", self.stmt_list(())))
        self.close_block("if", kw)
        return Node("if_stmt", children)

    def while_stmt(self):
        kw = self.advance()
        cond = self.cond("while")
        if self.cur.type != "DO":
            self.error(f"Expected 'do' after condition, found {describe(self.cur)}",
                       HINTS["while"])
        self.advance()
        body = self.stmt_list(())
        self.close_block("while", kw)
        return Node("while_stmt", [Node("cond", [cond]), Node("body", body)])

    def close_block(self, name, opener):
        if self.cur.type != "END":
            self.error(
                f"Expected 'end' to close '{name}' opened at line {opener.line}, "
                f"found {describe(self.cur)}",
                HINTS[name],
            )
        self.advance()

    def cond(self, owner):
        if self.cur.type not in ("IDENT", "NUMBER", "LPAREN", "MINUS"):
            self.error(f"Expected a condition after '{owner}', found {describe(self.cur)}",
                       HINTS["cond"])
        left = self.expr()
        if self.cur.type != "COMP":
            self.error(
                f"Expected a comparison operator (<, >, <=, >=, ==, !=) in condition, "
                f"found {describe(self.cur)}",
                HINTS["cond"],
            )
        op = self.advance()
        if self.cur.type not in ("IDENT", "NUMBER", "LPAREN", "MINUS"):
            self.error(f"Expected an expression after '{op.text}', found {describe(self.cur)}",
                       HINTS["cond"])
        right = self.expr()
        return Node(f"COMP {op.text}", [left, right])

    def expr(self):
        node = self.term()
        while self.cur.type in ("PLUS", "MINUS"):
            op = self.advance()
            node = Node(f"op {op.text}", [node, self.term()])
        return node

    def term(self):
        node = self.factor()
        while self.cur.type in ("STAR", "SLASH"):
            op = self.advance()
            node = Node(f"op {op.text}", [node, self.factor()])
        return node

    def factor(self):
        t = self.cur
        if t.type == "NUMBER":
            self.advance()
            return Node(f"NUMBER {t.text}")
        if t.type == "IDENT":
            self.advance()
            return Node(f"IDENT {t.text}")
        if t.type == "LPAREN":
            self.advance()
            if self.cur.type == "RPAREN":
                self.error("Empty parentheses: expected an expression after '('",
                           HINTS["expr"])
            inner = self.expr()
            if self.cur.type != "RPAREN":
                self.error(f"Expected ')' to match '(' at column {t.col}, "
                           f"found {describe(self.cur)}", HINTS["expr"])
            self.advance()
            return inner
        if t.type == "MINUS":
            self.advance()
            return Node("neg", [self.factor()])
        self.error(f"Expected a number, variable or '(' but found {describe(t)}",
                   HINTS["expr"])


def parse(source):
    """Tokenize + parse. Returns (tokens, tree). Raises LexError / SyntaxErr."""
    tokens = tokenize(source)
    tree = Parser(tokens).program()
    return tokens, tree
