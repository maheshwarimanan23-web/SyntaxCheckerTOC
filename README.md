# Mini Programming Language Syntax Checker

**Course:** Theory of Computation (BIS503)  
**Semester:** 5th Semester, Section B  
**Project:** 12  
**Group:** 12

## About the Project

This project is a simple syntax checker developed using Python. It checks whether a program follows the grammar rules of our mini programming language.

The language supports variable assignments, `if-else` statements, `while` loops, and arithmetic expressions. A DFA-based tokenizer converts the input into tokens, and a recursive descent parser checks whether the program follows the grammar rules.

If the program is valid, it displays `SYNTAX OK`. If there is a syntax error, the checker shows an error message along with the line and column number to help identify the problem.

## Team Members

- M Shreyank Gowda — 4NI24IS094
- Kritika — 4NI24IS087
- Manan Maheshwari — 4NI24IS099
- Nischitha R N — 4NI24IS119

## Project Files

| File | Description |
|---|---|
| `tokenizer.py` | Converts the input program into tokens using DFA rules. |
| `mini_parser.py` | Checks program syntax using a recursive descent parser. |
| `checker.py` | Provides the command-line interface and displays results. |
| `test_checker.py` | Contains test cases for valid and invalid programs. |
| `demo_ai_loop.py` | Demonstrates a generate, validate, and retry workflow. |
| `GRAMMAR.md` | Explains the grammar, DFA, derivations, and theory. |

## Requirements

- Python 3.8 or newer
- No external libraries are required.

## How to Run

Run these commands from the project directory.

**Run the sample programs**
```bash
python checker.py --demo
```

**Check a program file**
```bash
python checker.py prog.txt
```

**Display the parse tree**
```bash
python checker.py --tree prog.txt
```

**Run the test cases**
```bash
python -m unittest -v test_checker
```

**Run the AI loop demonstration**
```bash
python demo_ai_loop.py
```

## Example

For an invalid program, the checker displays an error with its location and a helpful hint.

```text
SYNTAX ERROR at line 2, column 10
Expected 'then' after condition, found 'y'
```

For example, an `if` statement must contain the `then` keyword after its condition.

## Work Distribution

- **Kritika:** Language design and CFG rules.
- **Nischitha R N:** Tokenizer and DFA implementation.
- **Manan Maheshwari:** Parser implementation.
- **M Shreyank Gowda:** Error messages, test cases, and presentation slides.

## Testing and Contributions

Test cases are used to check how the syntax checker handles valid and invalid programs. Before the final submission, we will run the tests and verify that the project works correctly.

The project will be maintained in the group's GitHub repository. Each member will commit their own changes so the team's contributions can be tracked.
