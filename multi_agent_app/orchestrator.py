from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .agents import CriticAgent, PlannerAgent, ResearchAgent, SynthesizerAgent


@dataclass
class OrchestrationOutput:
    """Structured output from the multi-agent workflow."""

    plan: list[str]
    research: list[str]
    critique: str
    final: str


class MultiAgentOrchestrator:
    """Coordinates planner, researcher, critic, and synthesizer agents."""

    def __init__(self, max_workers: int = 4) -> None:
        self.max_workers = max_workers
        self.planner = PlannerAgent()
        self.researcher = ResearchAgent()
        self.critic = CriticAgent()
        self.synthesizer = SynthesizerAgent()

    def _research_step(self, step: str) -> str:
        cleaned = step.split(". ", maxsplit=1)[-1]
        return self.researcher.run(cleaned).content

    def solve(self, user_task: str) -> OrchestrationOutput:
        plan_result = self.planner.run(user_task)
        plan_lines = [line.strip() for line in plan_result.content.splitlines() if line.strip()]

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            research_notes = list(executor.map(self._research_step, plan_lines))

        critique_input = (
            f"Task: {user_task}\n\n"
            f"Plan:\n" + "\n".join(plan_lines) + "\n\n"
            f"Research:\n" + "\n".join(f"- {note}" for note in research_notes)
        )
        critique_result = self.critic.run(critique_input)

        synthesis_input = (
            f"Task: {user_task}\n\n"
            "Plan highlights:\n"
            + "\n".join(plan_lines)
            + "\n\nResearch highlights:\n"
            + "\n".join(f"- {note}" for note in research_notes)
            + "\n\nCritique:\n"
            + critique_result.content
        )
        final_result = self.synthesizer.run(synthesis_input)

        return OrchestrationOutput(
            plan=plan_lines,
            research=research_notes,
            critique=critique_result.content,
            final=final_result.content,
        )
