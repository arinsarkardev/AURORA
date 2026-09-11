import argparse

from aurora.agent.loop import ResearchAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AURORA v0.1")
    parser.add_argument(
        "goal",
        nargs="?",
        default="Find the minimum of the demonstration objective.",
        help="Research goal for this experiment run.",
    )
    parser.add_argument(
        "--memory",
        default="aurora_memory.json",
        help="Path to the persistent experience database.",
    )
    args = parser.parse_args()

    agent = ResearchAgent(args.memory)
    result = agent.run(args.goal)

    print("\n=== AURORA v0.1 ===")
    print(f"Goal: {result['goal']}")
    print(f"Best candidate: {result['best']}")
    print(f"Experiments this run: {result['experiments_this_run']}")
    print(f"Total remembered experiences: {result['total_memory']}")
    print(f"Solved: {'YES' if result['solved'] else 'NO'}")
