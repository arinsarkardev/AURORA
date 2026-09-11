from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class EquationAttempt:
    strategy: str
    success: bool
    candidate: list[str]
    explanation: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EquationResult:
    expression: str
    variable: str
    solutions: tuple[str, ...]
    verified: bool
    attempts: tuple[EquationAttempt, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "expression": self.expression,
            "variable": self.variable,
            "solutions": list(self.solutions),
            "verified": self.verified,
            "attempts": [a.to_dict() for a in self.attempts],
        }


class EquationEngine:
    """Verified symbolic equation solver for AURORA v0.2."""

    def solve(self, expression: str, variable: str | None = None) -> EquationResult:
        equation = self._parse_equation(expression)
        symbol = self._select_variable(equation, variable)
        attempts: list[EquationAttempt] = []

        try:
            solutions = sp.solve(equation, symbol)
            candidates = tuple(self._format_value(v) for v in solutions)
            verified = all(self._verify(equation, symbol, v) for v in solutions)
            attempts.append(EquationAttempt(
                "symbolic_solve", verified, list(candidates),
                "Solved symbolically and independently checked candidates by substitution."
            ))
            if verified:
                return EquationResult(expression, str(symbol), candidates, True, tuple(attempts))
        except Exception as exc:
            attempts.append(EquationAttempt(
                "symbolic_solve", False, [],
                "Symbolic solver could not complete the attempt.", str(exc)
            ))

        return EquationResult(expression, str(symbol), (), False, tuple(attempts))

    @staticmethod
    def _parse_equation(expression: str) -> sp.Equality:
        text = expression.strip()
        if not text:
            raise ValueError("Equation cannot be empty.")
        if "=" in text:
            left, right = text.split("=", 1)
            if not left.strip() or not right.strip():
                raise ValueError("Equation must have expressions on both sides of '='.")
            return sp.Eq(sp.sympify(left), sp.sympify(right))
        return sp.Eq(sp.sympify(text), 0)

    @staticmethod
    def _select_variable(equation: sp.Equality, variable: str | None) -> sp.Symbol:
        symbols = sorted(equation.free_symbols, key=lambda s: s.name)
        if variable is not None:
            selected = sp.Symbol(variable)
            if selected not in symbols:
                raise ValueError(f"Variable '{variable}' does not occur in the equation.")
            return selected
        if len(symbols) != 1:
            raise ValueError(
                "AURORA v0.2 requires exactly one variable unless a variable is supplied."
            )
        return symbols[0]

    @staticmethod
    def _verify(equation: sp.Equality, symbol: sp.Symbol, value: sp.Expr) -> bool:
        return sp.simplify((equation.lhs - equation.rhs).subs(symbol, value)) == 0

    @staticmethod
    def _format_value(value: sp.Expr) -> str:
        return str(sp.simplify(value))
