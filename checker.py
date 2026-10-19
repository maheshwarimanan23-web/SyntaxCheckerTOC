"""
checker.py -- Mini Language syntax checker (command-line front end).

Usage:
    python checker.py program.txt        # check a file
    python checker.py --demo             # run the built-in sample programs
    python checker.py --tree program.txt # also print the parse tree
    echo "x = 5" | python checker.py -   # read from stdin
"""

import sys
from tokenizer import LexError
from mini_parser import parse, SyntaxErr


def check(source, show_tree=False, name="Program"):
    """Return (ok, report_text)."""
    lines = source.splitlines()
    try:
        tokens, tree = parse(source)
    except (LexError, SyntaxErr) as e:
        kind = "LEXICAL ERROR" if isinstance(e, LexError) else "SYNTAX ERROR"
        out = [f"{name}: {kind} at line {e.line}, column {e.col}",
               f"  {e.message}"]
        if 1 <= e.line <= len(lines):
            src_line = lines[e.line - 1]
            out.append(f"  {e.line:>3} | {src_line}")
            out.append("      | " + " " * (e.col - 1) + "^")
        if e.hint:
            out.append(f"  Hint: {e.hint}")
        return False, "\n".join(out)

    toks = [t.type for t in tokens if t.type != "EOF"]
    out = [f"{name}: SYNTAX OK", f"  Tokens: [{', '.join(toks)}]"]
    kinds = [c.label for c in tree.children]
    out.append(f"  Parse: {len(kinds)} top-level statement(s): {', '.join(kinds) or 'none'}")
    if show_tree:
        out.append("  Parse tree:")
        out.extend("    " + l for l in tree.pretty().splitlines())
    return True, "\n".join(out)


DEMO = {
    "Program 1": "x = 5\nif x > 3 then y = x + 1 end\n",
    "Program 2": "x = 5\nif x > 3 y = x + 1\n",
}


def main(argv):
    show_tree = "--tree" in argv
    argv = [a for a in argv if a != "--tree"]
    if not argv or argv[0] == "--demo":
        for name, src in DEMO.items():
            print(check(src, show_tree=True, name=name)[1], end="\n\n")
        return 0
    path = argv[0]
    src = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    ok, report = check(src, show_tree=show_tree, name=path)
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
