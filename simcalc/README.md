# SimCalc - Simple Python Calculator

A lightweight, robust, and safe command-line calculator written in Python 3.

## Features
- **Arithmetic Operations**: Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), Floor Division (`//`), Modulo (`%`), Exponentiation (`^` or `**`).
- **Parentheses Support**: Evaluates complex nested expressions using standard mathematical order of operations (PEMDAS).
- **Safe Evaluation**: Powered by Python's Abstract Syntax Tree (`ast`) module. Does not use unsafe `eval()`.
- **History Tracking**: Keeps track of calculations performed in the current session.
- **Dual Execution Modes**: Interactive shell (REPL) or instant one-line evaluation via CLI arguments.

---

## Directory Structure
```
simcalc/
├── DESIGN.md           # Architecture, specifications, and design documents
├── calculator.py       # Core calculator logic and safe expression parser
├── cli.py              # CLI entry point (interactive & direct mode)
├── test_calculator.py  # Unit test suite
└── README.md           # User guide and instructions
```

---

## Usage

### 1. Interactive Mode (REPL)
Run the CLI without arguments:
```bash
python3 cli.py
```
**Commands within interactive mode:**
- Type any mathematical expression, e.g. `(10 + 5) * 3`
- `history` - View previous calculations and results
- `clear` - Clear calculation history
- `help` - View supported operators
- `exit` or `quit` - Exit the calculator

### 2. Direct Evaluation Mode
Pass an expression as arguments:
```bash
python3 cli.py "15 * (4 + 2) / 3"
# Output: 30
```
Or using the `-e` flag:
```bash
python3 cli.py -e "2 ^ 10"
# Output: 1024
```

---

## Running Unit Tests
To run the automated test suite:
```bash
python3 -m unittest test_calculator.py
```
