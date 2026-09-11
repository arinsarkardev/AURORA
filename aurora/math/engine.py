from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class EquationAttempt:
    """One mathematically meaningful attempt made by the engine."""

    strategy: str
    success: bool
    candidate: list[str]
    explanation: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EquationResult:
    """Verified result returned by the equation engine."""

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
            "attempts": [attempt.to_dict() for attempt in self.attempts],
        }


class EquationEngine:
    """Verified symbolic equation solver used as AURORA's math tool.

    v0.2 deliberately delegates algebra to SymPy instead of asking an LLM to
    perform arithmetic. The engine keeps the solving strategy and an
    independent substitution check so future agents can reason over evidence.
    """

    def solve(self, expression: str, variable: str | None = None) -> EquationResult:
        equation = self._parse_equation(expression)
        symbol = self._select_variable(equation, variable)
        attempts: list[EquationAttempt] = []

        try:
            solutions = sp.solve(equation, symbol)
            candidate_strings = tuple(self._format_value(value) for value in solutions)
            verified = all(self._verify(equation, symbol, value) for value in solutions)
            attempts.append(
                EquationAttempt(
                    strategy="symbolic_solve",
                    success=verified,
                    candidate=list(candidate_strings),
                    explanation="Solved symbolically and independently checked each candidate by substitution.",
                )
            )
            if verified:
                return EquationResult(
                    expression=expression,
                    variable=str(symbol),
                    solutions=candidate_strings,
                    verified=True,
                    attempts=tuple(attempts),
                )
        except Exception as exc:  # pragma: no cover - defensive boundary
            attempts.append(
                EquationAttempt(
                    strategy="symbolic_solve",
                    success=False,
                    candidate=[],
                    explanation="Symbolic solver could not complete the attempt.",
                    error=str(exc),
                )
            )

        return EquationResult(
            expression=expression,
            variable=str(symbol),
            solutions=(),
            verified=False,
            attempts=tuple(attempts),
        )

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

        # A bare expression is interpreted as expression = 0.
        return sp.Eq(sp.sympify(text), 0)

    @staticmethod
    def _select_variable(equation: sp.Equality, variable: str | None) -> sp.Symbol:
        symbols = sorted(equation.free_symbols, key=lambda item: item.name)
        if variable is not None:
            selected = sp.Symbol(variable)
            if selected not in symbols:
                raise ValueError(f"Variable '{variable}' does not occur in the equation.")
            return selected
        if len(symbols) != 1:
            raise ValueError(
                "AURORA v0.2 requires exactly one variable unless --variable is supplied."
            )
        return symbols[0]

    @staticmethod
    def _verify(equation: sp.Equality, symbol: sp.Symbol, value: sp.Expr) -> bool:
        difference = sp.simplify((equation.lhs - equation.rhs).subs(symbol, value))
        return difference == 0

    @staticmethod
    def _format_value(value: sp.Expr) -> str:
        return str(sp.simplify(value))
