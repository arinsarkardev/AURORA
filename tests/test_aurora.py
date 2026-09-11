from aurora.agent.loop import ResearchAgent
from aurora.experiments.experiment import run_experiment


def test_demo_objective_has_known_optimum():
    result = run_experiment(3)
    assert result.score == 0


def test_agent_finds_optimum_and_remembers(tmp_path):
    memory = tmp_path / "memory.json"
    agent = ResearchAgent(str(memory))

    first = agent.run("Find the minimum")
    assert first["solved"] is True
    assert first["best"] == {"x": 3, "score": 0}

    second = agent.run("Find the minimum again")
    assert second["solved"] is True
    assert second["total_memory"] >= first["total_memory"]
