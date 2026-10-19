"""10 valid + 10 invalid programs. Run: python -m unittest -v test_checker"""

import unittest
from checker import check

VALID = [
    "x = 5",
    "x = 5\ny = x + 1",
    "x = 5\nif x > 3 then y = x + 1 end",
    "if a == b then c = 1 else c = 2 end",
    "i = 0\nwhile i < 10 do i = i + 1 end",
    "x = (1 + 2) * 3 - 4 / 2",
    "x = -y + 3",
    "while a != 0 do\n  if a > 5 then a = a - 5 else a = a - 1 end\nend",
    "# comment only\nx = 1  # trailing comment",
    "",  # empty program is valid (stmt_list -> epsilon)
]

# (source, line, col, substring expected in message)
INVALID = [
    ("x = 5\nif x > 3 y = x + 1", 2, 10, "Expected 'then'"),
    ("if x > 3 then y = 1", 1, 20, "Expected 'end'"),
    ("while x < 3 y = 1 end", 1, 13, "Expected 'do'"),
    ("x = ", 1, 5, "Expected an expression after '='"),
    ("x = (1 + 2", 1, 11, "Expected ')'"),
    ("if x then y = 1 end", 1, 6, "comparison operator"),
    ("x = 5 +", 1, 8, "Expected a number, variable or '('"),
    ("x = 5\nend", 2, 1, "Unexpected 'end'"),
    ("x = 3 @ 4", 1, 7, "Unexpected character"),
    ("while a < 3 do\n  a = a + 1\n", 3, 1, "opened at line 1"),
]


class Tests(unittest.TestCase):
    def test_valid(self):
        for i, src in enumerate(VALID, 1):
            with self.subTest(i=i):
                ok, report = check(src)
                self.assertTrue(ok, report)

    def test_invalid(self):
        for i, (src, line, col, msg) in enumerate(INVALID, 1):
            with self.subTest(i=i):
                ok, report = check(src)
                self.assertFalse(ok, f"expected error for {src!r}")
                self.assertIn(f"line {line}, column {col}", report)
                self.assertIn(msg, report)


if __name__ == "__main__":
    unittest.main()
