"""
tokenizer.py -- DFA-based tokenizer for the Mini Language.

The scanner is a real DFA: a transition table (state, char_class) -> state.
Tokens are produced by "maximal munch": keep following transitions until none
exists, then emit the token for the last state reached (if it is accepting).

DFA states
----------
S0      start
ID      identifier / keyword      [A-Za-z_][A-Za-z0-9_]*
NUM     integer literal           [0-9]+
LT, GT  '<' '>'                   (accepting, COMP)
LE, GE  '<=' '>='                 (accepting, COMP)
EQ      '='                       (accepting, ASSIGN)
EQEQ    '=='                      (accepting, COMP)
BANG    '!'                       (NOT accepting; needs '=' next)
NE      '!='                      (accepting, COMP)
PLUS MINUS STAR SLASH LPAR RPAR   single-character accepting states
"""

from dataclasses import dataclass

KEYWORDS = {
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "end": "END",
    "while": "WHILE",
    "do": "DO",
}

# ---- character classes -----------------------------------------------------

def char_class(ch):
    if ch.isalpha() and ch.isascii() or ch == "_":
        return "LETTER"
    if ch.isdigit() and ch.isascii():
        return "DIGIT"
    if ch in " \t\r":
        return "SPACE"
    if ch == "\n":
        return "NEWLINE"
    if ch in "+-*/()<>=!":
        return ch
    return "OTHER"


# ---- DFA transition table --------------------------------------------------

TRANSITIONS = {
    ("S0", "LETTER"): "ID",
    ("S0", "DIGIT"): "NUM",
    ("S0", "+"): "PLUS",
    ("S0", "-"): "MINUS",
    ("S0", "*"): "STAR",
    ("S0", "/"): "SLASH",
    ("S0", "("): "LPAR",
    ("S0", ")"): "RPAR",
    ("S0", "<"): "LT",
    ("S0", ">"): "GT",
    ("S0", "="): "EQ",
    ("S0", "!"): "BANG",
    ("ID", "LETTER"): "ID",
    ("ID", "DIGIT"): "ID",
    ("NUM", "DIGIT"): "NUM",
    ("LT", "="): "LE",
    ("GT", "="): "GE",
    ("EQ", "="): "EQEQ",
    ("BANG", "="): "NE",
}

# accepting state -> token type
ACCEPTING = {
    "ID": "IDENT",  # may be promoted to a keyword
    "NUM": "NUMBER",
    "PLUS": "PLUS",
    "MINUS": "MINUS",
    "STAR": "STAR",
    "SLASH": "SLASH",
    "LPAR": "LPAREN",
    "RPAR": "RPAREN",
    "LT": "COMP",
    "GT": "COMP",
    "LE": "COMP",
    "GE": "COMP",
    "EQEQ": "COMP",
    "NE": "COMP",
    "EQ": "ASSIGN",
}


@dataclass
class Token:
    type: str
    text: str
    line: int
    col: int

    def __repr__(self):
        return f"{self.type}({self.text!r})@{self.line}:{self.col}"


class LexError(Exception):
    def __init__(self, message, line, col, hint=None):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col
        self.hint = hint


def tokenize(source):
    """Return a list of Tokens ending with an EOF token. Raises LexError."""
    tokens = []
    i, line, col = 0, 1, 1
    n = len(source)

    while i < n:
        ch = source[i]
        cls = char_class(ch)

        # whitespace / newlines: skip
        if cls == "SPACE":
            i += 1
            col += 1
            continue
        if cls == "NEWLINE":
            i += 1
            line += 1
            col = 1
            continue

        # comments: '#' to end of line
        if ch == "#":
            while i < n and source[i] != "\n":
                i += 1
                col += 1
            continue

        # run the DFA from S0 using maximal munch
        state = "S0"
        j = i
        while j < n:
            nxt = TRANSITIONS.get((state, char_class(source[j])))
            if nxt is None:
                break
            state = nxt
            j += 1

        if state == "S0":
            raise LexError(
                f"Unexpected character {ch!r}", line, col,
                hint="Allowed: letters, digits, + - * / ( ) < > = ! and '#' comments",
            )
        if state not in ACCEPTING:  # only BANG ends up here
            raise LexError(
                "Lone '!' is not a valid token", line, col,
                hint="Did you mean '!=' ?",
            )

        text = source[i:j]
        ttype = ACCEPTING[state]
        if ttype == "IDENT" and text in KEYWORDS:
            ttype = KEYWORDS[text]
        tokens.append(Token(ttype, text, line, col))
        col += j - i
        i = j

    tokens.append(Token("EOF", "", line, col))
    return tokens
