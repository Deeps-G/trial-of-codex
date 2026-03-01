# Multi-Agent AI App

A practical, local-first **multi-agent AI application** that coordinates specialized agents to solve a user task end-to-end.

## Architecture

The app uses four agents with explicit responsibilities:

1. **PlannerAgent**: turns the user goal into a structured 5-step plan with owners.
2. **ResearchAgent**: expands each step into decisions, dependencies, and validation.
3. **CriticAgent**: performs quality/risk review on plan + research.
4. **SynthesizerAgent**: produces an executive brief and next action.

The orchestrator runs the research stage in parallel using a thread pool to model true multi-agent collaboration.

## Run in browser (visible on screen)

```bash
python web_app.py --port 8000
```

Then open:

```text
http://localhost:8000
```

Enter a task and click **Run agents**.

## Run in terminal

```bash
python app.py "Create a GTM plan for an AI scheduling assistant"
```

### JSON output mode

```bash
python app.py "Create a GTM plan for an AI scheduling assistant" --json
```

## Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Project layout

- `multi_agent_app/agents.py` – agent implementations and planning data structures.
- `multi_agent_app/orchestrator.py` – pipeline coordination and parallel research execution.
- `app.py` – terminal CLI interface.
- `web_app.py` – browser UI server.
- `tests/test_orchestrator.py` – orchestration and CLI checks.
- `tests/test_web_app.py` – UI rendering checks.

## How to customize

- Replace deterministic text generation in each agent with calls to your LLM provider.
- Add domain-specific tools in `ResearchAgent` (search, retrieval, calculators).
- Add additional specialist agents (e.g., security reviewer, legal reviewer, finance planner).
