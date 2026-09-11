# AURORA

**Autonomous Research & Optimization Runtime Architecture**

AURORA is a long-term CSE project for building an autonomous research and engineering system. The first milestone is a small, testable research loop:

**goal → hypothesis → experiment → evaluation → memory → next iteration**

The project will later grow toward mathematical reasoning, simulation, optimization, scientific data connectors, computer vision, engineering design, and authorized security research.

## Current milestone: v0.1

The v0.1 prototype:
- accepts a research goal from the command line;
- generates a deterministic set of hypotheses for a simple mathematical optimization problem;
- runs experiments;
- evaluates outcomes;
- stores successful/failed experiences in JSON;
- selects the next candidate using prior experience.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m aurora
```

Run tests:

```bash
pytest
```

## Repository structure

```text
aurora/
  agent/          orchestration loop
  memory/         persistent experience store
  planner/        hypothesis/experiment planning
  evaluator/      result evaluation
  math/           future symbolic/numerical engines
  experiments/    experiment abstractions
  simulation/     future scientific simulators
  data/           future authorized data connectors/fusion
  vision/         future computer-vision modules
  security/       future authorized security-analysis modules
  engineering/    future design/prototyping modules
  interface/      future CLI/API/UI

tests/
docs/
```

## Design principle

AURORA should never treat an LLM's output as proof. Mathematical verification, simulation, measurements, uncertainty, and explicit assumptions remain separate layers.
