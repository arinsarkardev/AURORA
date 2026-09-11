"""CLI entry point for AURORA v0.2."""

import argparse

from aurora.agent.loop import ResearchAgent
from aurora.math.engine import EquationEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AURORA v0.2")
    parser.add_argument("goal", nargs="?", default="Solve x**2 - 5*x + 6 = 0")
    parser.add_argument("--memory", default="aurora_memory.json")
    parser.add_argument("--equation", help="Solve and verify one equation directly.")
    parser.add_argument("--variable", help="Variable to solve for when an equation has multiple symbols.")
    args = parser.parse_args()

    if args.equation:
        result = EquationEngine().solve(args.equation, args.variable)
        print("\n=== AURORA v0.2 — Math Engine ===")
        print(f"Equation: {result.expression}")
        print(f"Variable: {result.variable}")
        print(f"Solutions: {', '.join(result.solutions) or 'none'}")
        print(f"Verified: {'YES' if result.verified else 'NO'}")
        for attempt in result.attempts:
            print(f"- {attempt.strategy}: {'PASS' if attempt.success else 'FAIL'} — {attempt.explanation}")
        return

    agent = ResearchAgent(args.memory)
    result = agent.run(args.goal)

    print("\n=== AURORA v0.2 ===")
    print(f"Goal: {result['goal']}")
    print(f"Best candidate: {result['best']}")
    print(f"Experiments this run: {result['experiments_this_run']}")
    print(f"Total remembered experiences: {result['total_memory']}")
    print(f"Solved: {'YES' if result['solved'] else 'NO'}")
