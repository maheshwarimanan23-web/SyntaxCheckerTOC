# Mini Parser – CFG and Recursive Descent Parsing

## 1. Introduction

A parser is a part of a compiler that checks whether the sequence of tokens follows the grammar rules of a programming language.

In our Mini Programming Language Syntax Checker, the parser checks the syntax of statements such as variable assignments, `if-else` statements, `while` loops, and arithmetic expressions.

The parser receives tokens from the tokenizer and checks whether they form a valid program.

## 2. Context-Free Grammar (CFG)

A Context-Free Grammar (CFG) defines the valid structure of statements and expressions in a language.

A CFG consists of:
- **Terminals:** Actual tokens such as identifiers, numbers, operators, and keywords.
- **Non-terminals:** Grammar symbols representing language structures.
- **Production rules:** Rules describing how non-terminals can be expanded.
- **Start symbol:** The symbol from which parsing begins.

The grammar used by the parser defines the structure of valid statements and expressions supported by our mini language.

## 3. Recursive Descent Parser

A recursive descent parser is a top-down parsing technique. It uses functions to check different grammar rules.

Each function handles a particular language construct, such as a statement, condition, or arithmetic expression. Some functions call other functions to check smaller parts of the input.

The parser reads the tokens in sequence and checks whether they follow the expected grammar.

## 4. How the Parser Works

The parsing process follows these steps:

1. The tokenizer converts the source program into tokens.
2. The parser receives the tokens.
3. It checks the tokens against the grammar rules.
4. If the tokens follow the grammar, the program is accepted.
5. If a token is missing or appears in the wrong position, the parser reports a syntax error.

## 5. Example

### Valid Program

```text
x = 10
y = x + 5
```

The parser accepts this program if both statements follow the grammar rules supported by the language.

### Invalid Program

```text
x = 10 +
```

This statement is invalid because the arithmetic expression is incomplete. The parser should report a syntax error when the input does not match the expected grammar.

## 6. Error Handling

The parser checks for syntax errors such as:
- Missing expected tokens.
- Incorrect statement structure.
- Incomplete arithmetic expressions.
- Invalid conditions or control-flow statements.

Where supported by the implementation, the error message includes the line and column of the error to help identify the problem.

## 7. Role of the Parser in Our Project

The parser is responsible for checking the syntactic structure of the mini programming language.

The tokenizer identifies individual tokens, while the parser checks how those tokens are arranged according to the grammar.

Together, these components help determine whether a source program follows the syntax rules of the language.

## 8. Conclusion

The mini parser demonstrates how Context-Free Grammar and recursive descent parsing can be used to validate the syntax of a simple programming language. It also helps us understand how parsing is used in compiler design.
