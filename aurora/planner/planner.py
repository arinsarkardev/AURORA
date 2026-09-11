from dataclasses import dataclass


@dataclass(frozen=True)
class Hypothesis:
    """A candidate parameter setting for an experiment."""

    x: float


def generate_hypotheses() -> list[Hypothesis]:
    """Generate an initial search space for the demo objective.

    The objective is deliberately simple: minimize f(x) = (x - 3)^2.
    Later this planner will be replaced by model-based scientific planning.
    """
    return [Hypothesis(x) for x in range(-5, 12)]
