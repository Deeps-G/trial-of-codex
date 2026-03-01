import json
import subprocess
import sys
import unittest

from multi_agent_app import MultiAgentOrchestrator


class OrchestratorTests(unittest.TestCase):
    def test_solve_returns_structured_sections(self) -> None:
        orchestrator = MultiAgentOrchestrator(max_workers=2)
        result = orchestrator.solve("Build a customer onboarding flow")

        self.assertEqual(len(result.plan), 5)
        self.assertEqual(len(result.research), 5)
        self.assertTrue(all("Step analysis" in note for note in result.research))
        self.assertIn("Quality and risk review", result.critique)
        self.assertIn("Executive brief", result.final)

    def test_cli_json_mode_outputs_valid_json(self) -> None:
        proc = subprocess.run(
            [sys.executable, "app.py", "Plan a launch", "--json"],
            capture_output=True,
            text=True,
            check=True,
        )
        payload = json.loads(proc.stdout)

        self.assertEqual(len(payload["plan"]), 5)
        self.assertEqual(len(payload["research"]), 5)
        self.assertIn("Quality and risk review", payload["critique"])


if __name__ == "__main__":
    unittest.main()
