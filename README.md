# AURORA

**Autonomous Research & Optimization Runtime Architecture**

AURORA is a long-term CSE project for building an autonomous research and engineering system. It is designed around a strict evidence loop:

**goal → hypothesis → mathematical model → experiment → verification → memory → next iteration**

## Current milestone: v0.2

AURORA v0.2 adds a verified symbolic mathematics tool. It can:
- parse equations such as `x**2 - 5*x + 6 = 0`;
- solve them symbolically with SymPy;
- independently verify candidate solutions by substitution;
- persist the complete result and verification evidence in the experience store;
- route equation-like research goals through the math engine.

### Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python -m aurora --equation 'x**2 - 5*x + 6 = 0'
python -m pytest
```

You can also run the original optimization loop:

```bash
python -m aurora 'Find the minimum of the demonstration objective.'
```

## Architecture

```text
User Goal
   |
   v
ResearchAgent
   |
   +--> Planner --------> Hypotheses
   |
   +--> Math Engine ----> Symbolic solution + verification
   |
   +--> Experiment -----> Results
   |
   +--> Evaluator ------> Success/Failure
   |
   +--> Memory ---------> Persistent experience
   |
   +--------------------> Next iteration
```

The LLM, when introduced in a later milestone, will orchestrate verified tools rather than act as the source of mathematical proof.

## 4-year direction

1. **Foundations:** mathematics, algorithms, systems programming, symbolic/numerical computing.
2. **Autonomous experimentation:** simulation, optimization, failure analysis, experiment lineage, distributed execution.
3. **AI research agent:** LLM tool use, scientific retrieval, hypothesis generation, evidence evaluation, uncertainty.
4. **Engineering system:** domain simulators, CAD/design interfaces, multi-objective optimization, hardware/sensor interfaces, and real-world experiments.

## Data and security

Future data connectors may integrate public or explicitly authorized cameras, satellite feeds, sensors, computers, and servers. Security research is intended for systems the operator owns or is authorized to test, with auditable permissions.
