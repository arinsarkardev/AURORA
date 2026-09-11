import pytest

from aurora.math.engine import EquationEngine


def test_quadratic_is_solved_and_verified():
    result = EquationEngine().solve("x**2 - 5*x + 6 = 0")
    assert result.variable == "x"
    assert result.solutions == ("2", "3")
    assert result.verified is True


def test_linear_equation():
    result = EquationEngine().solve("2*x + 4 = 0")
    assert result.solutions == ("-2",)
    assert result.verified is True


def test_explicit_variable_for_multivariable_equation():
    result = EquationEngine().solve("x + y = 5", variable="x")
    assert result.variable == "x"
    assert result.solutions == ("5 - y",)
    assert result.verified is True


def test_empty_equation_rejected():
    with pytest.raises(ValueError):
        EquationEngine().solve("")
