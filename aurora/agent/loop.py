from aurora.evaluator.evaluator import evaluate
from aurora.experiments.experiment import run_experiment
from aurora.memory.store import ExperienceStore
from aurora.planner.planner import Hypothesis, generate_hypotheses


class ResearchAgent:
    """Minimal autonomous research loop used by AURORA v0.1."""

    def __init__(self, memory_path: str = "aurora_memory.json") -> None:
        self.memory = ExperienceStore(memory_path)

    def run(self, goal: str) -> dict:
        hypotheses = generate_hypotheses()
        experiences = []
        best = None

        # Use prior experience to avoid repeating already-tested candidates.
        tested_x = {item["hypothesis"]["x"] for item in self.memory.load() if "hypothesis" in item and "x" in item["hypothesis"]}
        ordered = [h for h in hypotheses if h.x not in tested_x]
        ordered += [h for h in hypotheses if h.x in tested_x]

        for hypothesis in ordered:
            result = run_experiment(hypothesis.x)
            evaluation = evaluate(result)
            experience = {
                "goal": goal,
                "hypothesis": {"x": hypothesis.x},
                "result": {"x": result.x, "score": result.score},
                "evaluation": {
                    "success": evaluation.success,
                    "score": evaluation.score,
                    "reason": evaluation.reason,
                },
            }
            self.memory.add(experience)
            experiences.append(experience)

            if best is None or result.score < best["score"]:
                best = {"x": result.x, "score": result.score}

            if evaluation.success:
                break

        return {
            "goal": goal,
            "best": best,
            "experiments_this_run": len(experiences),
            "total_memory": self.memory.count(),
            "solved": bool(best and best["score"] == 0),
        }
