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
## How It Works
 
The checker processes a program in two stages:
 
```text
Source program --> Tokenizer (DFA) --> Tokens --> Parser (CFG) --> SYNTAX OK / SYNTAX ERROR
```
 
1. **Tokenizer (DFA):** reads the characters of the program and groups them into tokens such as identifiers, numbers, operators, and keywords. Invalid characters are reported as a lexical error.
2. **Parser (CFG):** a recursive descent parser checks whether the tokens follow the grammar rules. Any violation is reported as a syntax error with its line and column.
## The Mini Language
 
The language supports the following constructs:
 
| Construct | Syntax |
|---|---|
| Assignment | `x = 5` |
| Arithmetic | `y = (x + 2) * 3 - 4 / 2` |
| Negative numbers | `z = -y + 3` |
| If statement | `if x > 3 then y = 1 end` |
| If-else statement | `if x > 3 then y = 1 else y = 2 end` |
| While loop | `while i < 10 do i = i + 1 end` |
| Comments | `# this is a comment` |
 
Comparison operators (used inside `if` and `while` conditions): `<`, `>`, `<=`, `>=`, `==`, `!=`
 
Keywords: `if`, `then`, `else`, `end`, `while`, `do`
 
**Example program:**
 
```text
x = 10
y = x + 5
if y > 10 then
    z = y * 2
else
    z = 0
end
```
 
The full grammar, terminal symbols, and operator precedence are described in `GRAMMAR.md`.
 
## Project Structure
 
```text
SyntaxCheckerTOC/
├── checker.py            # Command-line interface (run this)
├── tokenizer.py          # DFA-based tokenizer
├── mini_parser.py        # Recursive descent parser
├── test_checker.py       # Unit tests
├── demo_ai_loop.py       # Generate, validate, and retry demo
├── GRAMMAR.md            # Grammar, CFG rules, and theory
├── README.md             # Project documentation
├── .gitignore            # Files ignored by Git (__pycache__, *.pyc)
├── examples_programs/
│   ├── valid/            # 10 valid sample programs (.mini)
│   └── invalid/          # 10 invalid sample programs (.mini)
├── images/               # PDF exports of the CFG, DFA, and parse tree diagrams
└── draw.io codes/        # Editable draw.io source files for the diagrams
```
 
## Project Files
 
| File / Folder | Description |
|---|---|
| `tokenizer.py` | Converts the input program into tokens using DFA rules. |
| `mini_parser.py` | Checks program syntax using a recursive descent parser. |
| `checker.py` | Provides the command-line interface and displays results. |
| `test_checker.py` | Contains test cases for valid and invalid programs. |
| `demo_ai_loop.py` | Demonstrates a generate, validate, and retry workflow. |
| `GRAMMAR.md` | Explains the grammar, DFA, derivations, and theory. |
| `examples_programs/` | Sample `.mini` programs: 10 valid and 10 invalid. |
| `images/` | PDF diagrams of the CFG, the DFA-based tokenizer, and the parse tree. |
| `draw.io codes/` | Editable `.drawio` source files for the diagrams. |
| `.gitignore` | Stops Python cache files from being committed. |
 
## Requirements
 
- Python 3.8 or newer
- No external libraries are required.
Check your Python version with:
 
```bash
python --version
```
 
On Windows you can also use `py --version`. On Mac or Linux, use `python3`.
 
## How to Run
 
Run these commands from the project directory (the folder that contains `checker.py`).
 
**Run the built-in demo**
```bash
python checker.py --demo
```
 
**Check a program file**
```bash
python checker.py prog.txt
```
 
**Check one of the example programs**
```bash
python checker.py examples_programs/valid/05_if_then.mini
python checker.py examples_programs/invalid/02_missing_then.mini
```
 
**Display the parse tree**
```bash
python checker.py --tree prog.txt
```
 
**Read a program from standard input**
```bash
echo "x = 5" | python checker.py -
```
 
**Run the test cases**
```bash
python -m unittest -v test_checker
```
 
**Run the AI loop demonstration**
```bash
python demo_ai_loop.py
```
 
### Running on Windows (PowerShell)
 
Use backslashes in paths, and use `py` if `python` is not recognized:
 
```powershell
python checker.py examples_programs\valid\05_if_then.mini
```
 
To check all example programs at once:
 
```powershell
Get-ChildItem examples_programs -Recurse -Filter *.mini | ForEach-Object { python checker.py $_.FullName }
```
 
### Running on Mac / Linux
 
```bash
for f in examples_programs/valid/*.mini examples_programs/invalid/*.mini; do python3 checker.py "$f"; done
```
 
## Example
 
For a valid program, the checker prints `SYNTAX OK`, the token list, and the number of top-level statements.
 
```text
examples_programs/valid/05_if_then.mini: SYNTAX OK
  Tokens: [IDENT, ASSIGN, NUMBER, IF, IDENT, COMP, NUMBER, THEN, IDENT, ASSIGN, NUMBER, END]
  Parse: 2 top-level statement(s): assign, if_stmt
```
 
For an invalid program, the checker displays an error with its location, the offending line, and a helpful hint.
 
```text
examples_programs/invalid/02_missing_then.mini: SYNTAX ERROR at line 3, column 5
  Expected 'then' after condition, found 'y'
    3 |     y = 1
      |     ^
  Hint: if <condition> then <statements> [else <statements>] end
```
 
For example, an `if` statement must contain the `then` keyword after its condition.
 
### Types of errors reported
 
| Error type | Cause | Example |
|---|---|---|
| `LEXICAL ERROR` | A character that is not part of the language | `x = 3 @ 4` |
| `SYNTAX ERROR` | Tokens that break a grammar rule | `if x > 3 y = 1 end` (missing `then`) |
 
### Sample programs
 
The `examples_programs/` folder contains ready-to-use test inputs.
 
**Valid programs** (`examples_programs/valid/`): basic assignments, arithmetic precedence, parentheses, negative numbers, `if-then`, `if-else`, `while` loops, nested `if`, nested `while`, and comparisons with expressions.
 
**Invalid programs** (`examples_programs/invalid/`): missing assignment value, missing `then`, missing `end` for `if`, missing `do` in `while`, condition without a comparison, missing right operand in a condition, unmatched `end`, unmatched `else`, unclosed parenthesis, and invalid operator sequence.
 
## Diagrams
 
The `images/` folder contains PDF diagrams used for the project report and presentation:
 
- **CFG diagram:** `cfg_diagram.drawio.pdf`
- **DFA-based tokenizer:** `DFA_Based_Tokenizer.drawio.pdf`
- **Parse tree diagram:** `parse_tree_diagram.drawio.pdf`
The editable sources are in `draw.io codes/` and can be opened at [app.diagrams.net](https://app.diagrams.net) (draw.io).
 
## Work Distribution
 
- **Kritika:** Language design and CFG rules.
- **Nischitha R N:** Tokenizer and DFA implementation.
- **Manan Maheshwari:** Parser implementation.
- **M Shreyank Gowda:** Error messages, test cases, and presentation slides.
## Testing and Contributions
 
Test cases are used to check how the syntax checker handles valid and invalid programs. `test_checker.py` contains 10 valid and 10 invalid programs, and checks that invalid programs report the correct line, column, and error message.
 
Before the final submission, we will run the tests and verify that the project works correctly:
 
```bash
python -m unittest -v test_checker
```
 
The project is maintained in the group's GitHub repository. Each member commits their own changes so the team's contributions can be tracked. Python cache files (`__pycache__/`, `*.pyc`) are excluded through `.gitignore`.
 