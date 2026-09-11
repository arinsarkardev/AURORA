# AURORA v0.1 Architecture

```text
User Goal
   |
   v
ResearchAgent
   |
   +--> Planner --------> Hypotheses
   |
   +--> Experiment -----> Results
   |
   +--> Evaluator ------> Success/Failure
   |
   +--> Memory ---------> Persistent experience
   |
   +--------------------> Next iteration
```

The current mathematical experiment is intentionally deterministic so that the architecture can be tested before introducing an LLM. Future versions will add verified math tools and scientific simulators behind explicit interfaces.
