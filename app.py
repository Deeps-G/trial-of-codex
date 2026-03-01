from __future__ import annotations

import argparse
import json

from multi_agent_app import MultiAgentOrchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the multi-agent AI app.")
    parser.add_argument("task", help="The task for the agent team to solve.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print orchestration output in JSON format.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    orchestrator = MultiAgentOrchestrator()
    result = orchestrator.solve(args.task)

    if args.json:
        print(
            json.dumps(
                {
                    "plan": result.plan,
                    "research": result.research,
                    "critique": result.critique,
                    "final": result.final,
                },
                indent=2,
            )
        )
        return

    print("=== PLAN ===")
    for step in result.plan:
        print(step)

    print("\n=== RESEARCH NOTES ===")
    for idx, note in enumerate(result.research, start=1):
        print(f"{idx}. {note}")

    print("\n=== CRITIQUE ===")
    print(result.critique)

    print("\n=== FINAL RESPONSE ===")
    print(result.final)


if __name__ == "__main__":
    main()
