# Language Design and CFG Rules

## 1. Language Overview

The Mini Language is a small programming language that supports variable assignment, arithmetic expressions, conditional statements, and while loops.

A Context-Free Grammar (CFG) defines the valid syntax of this language. The parser checks whether a program follows these grammar rules.

## 2. CFG Production Rules

program    -> stmt_list EOF

stmt_list  -> stmt stmt_list | ε

stmt       -> assign
           | if_stmt
           | while_stmt
           | expr_stmt

assign     -> IDENT ASSIGN expr

if_stmt    -> IF cond THEN stmt_list END
           | IF cond THEN stmt_list ELSE stmt_list END

while_stmt -> WHILE cond DO stmt_list END

expr_stmt  -> expr

cond       -> expr COMP expr

expr       -> expr PLUS term
           | expr MINUS term
           | term

term       -> term STAR factor
           | term SLASH factor
           | factor

factor     -> NUMBER
           | IDENT
           | LPAREN expr RPAREN
           | MINUS factor

## 3. Terminal Symbols

- IDENT: variable name
- NUMBER: numeric value
- ASSIGN: assignment operator (=)
- PLUS: addition (+)
- MINUS: subtraction or unary minus (-)
- STAR: multiplication (*)
- SLASH: division (/)
- COMP: comparison operator
- IF, THEN, ELSE, END: conditional keywords
- WHILE, DO: loop keywords
- LPAREN, RPAREN: parentheses
- EOF: end of input
- ε: empty production

## 4. Operator Precedence

1. Parentheses and factors
2. Multiplication and division
3. Addition and subtraction
4. Comparison expressions

## 5. Example Program

x = 10
y = x + 5
if y > 10 then
    z = y * 2
else
    z = 0
end

## 6. Purpose

The CFG describes the syntax of valid programs. The parser uses grammar rules to identify valid statements and report syntax errors.
