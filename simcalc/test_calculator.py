"""
Unit tests for SimCalc (Calculator and ExpressionEvaluator).
"""

import unittest
from calculator import (
    Calculator,
    CalculatorError,
    DivisionByZeroError,
    ExpressionEvaluator,
    InvalidExpressionError,
)


class TestCalculatorCore(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_basic_operations(self):
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.multiply(10, 5), 50)
        self.assertEqual(self.calc.divide(10, 5), 2.0)
        self.assertEqual(self.calc.int_divide(11, 5), 2)
        self.assertEqual(self.calc.modulo(11, 5), 1)
        self.assertEqual(self.calc.power(2, 3), 8)

    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            self.calc.divide(10, 0)
        with self.assertRaises(DivisionByZeroError):
            self.calc.int_divide(10, 0)
        with self.assertRaises(DivisionByZeroError):
            self.calc.modulo(10, 0)

    def test_history(self):
        self.assertEqual(len(self.calc.get_history()), 0)
        self.calc.record_history("2 + 2", 4)
        self.calc.record_history("3 * 3", 9)
        history = self.calc.get_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0], ("2 + 2", 4))

        self.calc.clear_history()
        self.assertEqual(len(self.calc.get_history()), 0)


class TestExpressionEvaluator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()
        self.evaluator = ExpressionEvaluator(self.calc)

    def test_simple_arithmetic(self):
        self.assertEqual(self.evaluator.evaluate("1 + 2"), 3)
        self.assertEqual(self.evaluator.evaluate("10 - 4"), 6)
        self.assertEqual(self.evaluator.evaluate("3 * 7"), 21)
        self.assertEqual(self.evaluator.evaluate("15 / 3"), 5)
        self.assertEqual(self.evaluator.evaluate("7 // 2"), 3)
        self.assertEqual(self.evaluator.evaluate("14 % 4"), 2)
        self.assertEqual(self.evaluator.evaluate("2 ^ 3"), 8)
        self.assertEqual(self.evaluator.evaluate("2 ** 3"), 8)

    def test_operator_precedence(self):
        self.assertEqual(self.evaluator.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.evaluator.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.evaluator.evaluate("10 - 2 * 3 + 4 / 2"), 6)
        self.assertEqual(self.evaluator.evaluate("2 ^ 3 * 2"), 16)

    def test_unary_operators(self):
        self.assertEqual(self.evaluator.evaluate("-5 + 10"), 5)
        self.assertEqual(self.evaluator.evaluate("-(3 + 2)"), -5)
        self.assertEqual(self.evaluator.evaluate("+7 - -3"), 10)

    def test_floating_point(self):
        self.assertAlmostEqual(self.evaluator.evaluate("1.5 + 2.5"), 4)
        self.assertAlmostEqual(self.evaluator.evaluate("5 / 2"), 2.5)
        self.assertAlmostEqual(self.evaluator.evaluate("0.1 + 0.2"), 0.3, places=7)

    def test_division_by_zero_in_eval(self):
        with self.assertRaises(DivisionByZeroError):
            self.evaluator.evaluate("10 / 0")
        with self.assertRaises(DivisionByZeroError):
            self.evaluator.evaluate("5 / (2 - 2)")
        with self.assertRaises(DivisionByZeroError):
            self.evaluator.evaluate("10 % 0")

    def test_invalid_syntax(self):
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("   ")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("2 + + * 4")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("((2 + 3)")

    def test_safety_and_disallowed_syntax(self):
        # Disallow arbitrary functions / code injection
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("__import__('os').system('ls')")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("print('hello')")
        with self.assertRaises(InvalidExpressionError):
            self.evaluator.evaluate("x = 5")


if __name__ == "__main__":
    unittest.main()
