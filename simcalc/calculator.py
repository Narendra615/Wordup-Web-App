"""
Core calculator module providing arithmetic operations, history management,
and a safe AST-based mathematical expression evaluator.
"""

import ast
import operator
from typing import Any, List, Tuple, Union


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when division or modulo by zero is attempted."""
    pass


class InvalidExpressionError(CalculatorError):
    """Raised when an expression cannot be parsed or contains disallowed syntax."""
    pass


class Calculator:
    """Core calculator implementing standard arithmetic operations and history."""

    def __init__(self) -> None:
        self.history: List[Tuple[str, Union[int, float]]] = []

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b

    def int_divide(self, a: float, b: float) -> int:
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return int(a // b)

    def modulo(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Cannot modulo by zero.")
        return a % b

    def power(self, a: float, b: float) -> float:
        try:
            return a ** b
        except OverflowError:
            raise CalculatorError("Result exceeded maximum numeric limits.")

    def record_history(self, expression: str, result: Union[int, float]) -> None:
        self.history.append((expression, result))

    def get_history(self) -> List[Tuple[str, Union[int, float]]]:
        return list(self.history)

    def clear_history(self) -> None:
        self.history.clear()


class ExpressionEvaluator:
    """Safely evaluates math expressions using Python's Abstract Syntax Tree (ast).

    Avoids dangerous `eval()` by only evaluating mathematical nodes.
    """

    SUPPORTED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self, calculator: Calculator = None) -> None:
        self.calculator = calculator or Calculator()

    def _eval_node(self, node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise InvalidExpressionError(f"Unsupported constant type: {type(node.value).__name__}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self.SUPPORTED_OPERATORS:
                raise InvalidExpressionError(f"Unsupported binary operator: {op_type.__name__}")

            left_val = self._eval_node(node.left)
            right_val = self._eval_node(node.right)

            if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right_val == 0:
                raise DivisionByZeroError("Division by zero in expression.")

            op_func = self.SUPPORTED_OPERATORS[op_type]
            try:
                result = op_func(left_val, right_val)
                return result
            except OverflowError:
                raise CalculatorError("Calculation caused an overflow.")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self.SUPPORTED_OPERATORS:
                raise InvalidExpressionError(f"Unsupported unary operator: {op_type.__name__}")
            operand_val = self._eval_node(node.operand)
            return self.SUPPORTED_OPERATORS[op_type](operand_val)

        if isinstance(node, ast.Expression):
            return self._eval_node(node.body)

        raise InvalidExpressionError(f"Disallowed expression element: {type(node).__name__}")

    def evaluate(self, expression: str) -> Union[int, float]:
        """Parses and calculates the result of the mathematical expression."""
        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression is empty.")

        # Normalize caret '^' to '**' for exponentiation
        cleaned_expr = expression.replace("^", "**").strip()

        try:
            parsed_tree = ast.parse(cleaned_expr, mode="eval")
        except SyntaxError as e:
            raise InvalidExpressionError(f"Syntax error in expression: {e.msg}") from e

        result = self._eval_node(parsed_tree)

        # Pretty-format integer results where appropriate (e.g. 4.0 -> 4)
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        self.calculator.record_history(expression.strip(), result)
        return result
