import unittest

from web_app import render_page


class WebAppRenderTests(unittest.TestCase):
    def test_render_page_includes_form_and_title(self) -> None:
        html = render_page()
        self.assertIn("Multi-Agent AI App", html)
        self.assertIn("<form", html)
        self.assertIn("name=\"task\"", html)

    def test_render_page_renders_agent_sections(self) -> None:
        html = render_page(
            task="Plan launch",
            result={
                "plan": ["step 1"],
                "research": ["note 1"],
                "critique": "critique text",
                "final": "final text",
            },
        )
        self.assertIn("<h2>Plan</h2>", html)
        self.assertIn("<h2>Research Notes</h2>", html)
        self.assertIn("<h2>Critique</h2>", html)
        self.assertIn("<h2>Final Response</h2>", html)


if __name__ == "__main__":
    unittest.main()
