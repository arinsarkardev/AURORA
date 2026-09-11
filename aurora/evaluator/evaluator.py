from dataclasses import dataclass
from aurora.experiments.experiment import ExperimentResult


@dataclass(frozen=True)
class Evaluation:
    success: bool
    score: float
    reason: str


def evaluate(result: ExperimentResult) -> Evaluation:
    """Evaluate an experiment against the demo success criterion."""
    success = result.score == 0
    reason = "Exact optimum found." if success else "Candidate is not yet optimal."
    return Evaluation(success=success, score=result.score, reason=reason)
