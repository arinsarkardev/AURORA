"""Autonomous research orchestration for AURORA v0.2."""

from aurora.evaluator.evaluator import evaluate
from aurora.experiments.experiment import run_experiment
from aurora.math.engine import EquationEngine
from aurora.memory.store import ExperienceStore
from aurora.planner.planner import generate_hypotheses


class ResearchAgent:
    """Run experiments and retain evidence for future iterations."""

    def __init__(self, memory_path: str = "aurora_memory.json") -> None:
        self.memory = ExperienceStore(memory_path)
        self.math = EquationEngine()

    def run(self, goal: str) -> dict:
        # Route equation-like goals through the verified math tool.
        if self._looks_like_equation(goal):
            result = self.math.solve(goal)
            experience = {
                "goal": goal,
                "type": "equation",
                "result": result.to_dict(),
            }
            self.memory.add(experience)
            return {
                "goal": goal,
                "type": "equation",
                "solutions": list(result.solutions),
                "verified": result.verified,
                "experiments_this_run": 1,
                "total_memory": self.memory.count(),
                "solved": result.verified,
            }

        # Preserve the original v0.1 optimization demonstration.
        hypotheses = generate_hypotheses()
        experiences = []
        best = None
        tested_x = {
            item["hypothesis"]["x"]
            for item in self.memory.load()
            if item.get("type") != "equation"
            and "hypothesis" in item
            and "x" in item["hypothesis"]
        }
        ordered = [h for h in hypotheses if h.x not in tested_x]
        ordered += [h for h in hypotheses if h.x in tested_x]

        for hypothesis in ordered:
            result = run_experiment(hypothesis.x)
            evaluation = evaluate(result)
            experience = {
                "goal": goal,
                "type": "optimization",
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
            "type": "optimization",
            "best": best,
            "experiments_this_run": len(experiences),
            "total_memory": self.memory.count(),
            "solved": bool(best and best["score"] == 0),
        }

    @staticmethod
    def _looks_like_equation(goal: str) -> bool:
        return "=" in goal and any(ch.isalpha() for ch in goal)
