from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentResult:
    x: float
    score: float


def run_experiment(x: float) -> ExperimentResult:
    """Run the deterministic v0.1 simulation: f(x) = (x - 3)^2."""
    score = (x - 3) ** 2
    return ExperimentResult(x=x, score=score)
