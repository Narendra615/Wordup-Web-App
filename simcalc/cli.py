#!/usr/bin/env python3
"""
Command Line Interface (CLI) for SimCalc.
Provides interactive REPL mode and single-expression evaluation via arguments.
"""

import argparse
import sys
from calculator import (
    Calculator,
    CalculatorError,
    DivisionByZeroError,
    ExpressionEvaluator,
    InvalidExpressionError,
)


def print_banner() -> None:
    banner = """
======================================================
           SimCalc - Simple Python Calculator
======================================================
 Type a math expression (e.g., '12 + 4 * (5 - 2)')
 Commands:
   history  - View past calculations
   clear    - Clear history
   help     - Show instructions
   exit     - Exit calculator
======================================================
"""
    print(banner)


def show_help() -> None:
    help_text = """
Supported Operators:
  +   Addition
  -   Subtraction (or negation)
  *   Multiplication
  /   Division
  //  Integer Floor Division
  %   Modulo (Remainder)
  ^   Exponentiation (or **)
  ()  Parentheses for grouping

Examples:
  > 15 + 27
  42
  > (10 + 5) * 2 - 4 / 2
  28
  > 2 ^ 8
  256
  > 17 % 5
  2
"""
    print(help_text)


def run_interactive() -> None:
    calculator = Calculator()
    evaluator = ExpressionEvaluator(calculator)
    print_banner()

    while True:
        try:
            user_input = input("calc > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        cmd = user_input.lower()

        if cmd in ("exit", "quit", "q"):
            print("Goodbye!")
            break
        elif cmd == "help":
            show_help()
        elif cmd == "history":
            history = calculator.get_history()
            if not history:
                print("No calculations in history.")
            else:
                print("\n--- Calculation History ---")
                for idx, (expr, res) in enumerate(history, 1):
                    print(f"  [{idx}] {expr} = {res}")
                print("---------------------------\n")
        elif cmd == "clear":
            calculator.clear_history()
            print("History cleared.")
        else:
            try:
                result = evaluator.evaluate(user_input)
                print(f"=> {result}")
            except DivisionByZeroError as e:
                print(f"Error: {e}")
            except InvalidExpressionError as e:
                print(f"Invalid Expression: {e}")
            except CalculatorError as e:
                print(f"Calculation Error: {e}")
            except Exception as e:
                print(f"Unexpected Error: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="SimCalc - Simple Python Calculator")
    parser.add_argument(
        "-e",
        "--eval",
        dest="expression",
        type=str,
        help="Evaluate a mathematical expression directly and exit",
    )
    parser.add_argument(
        "expr_args",
        nargs="*",
        help="Optional expression arguments to evaluate directly",
    )

    args = parser.parse_args()

    # If an expression was passed directly via CLI
    expr = args.expression or (" ".join(args.expr_args) if args.expr_args else None)

    if expr:
        evaluator = ExpressionEvaluator()
        try:
            result = evaluator.evaluate(expr)
            print(result)
            sys.exit(0)
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.exit(1)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
