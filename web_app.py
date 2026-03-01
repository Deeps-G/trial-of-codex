from __future__ import annotations

import argparse
from dataclasses import asdict
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

from multi_agent_app import MultiAgentOrchestrator


def render_page(task: str = "", result: dict | None = None, error: str = "") -> str:
    safe_task = escape(task)
    safe_error = f"<p class='error'>{escape(error)}</p>" if error else ""

    result_html = ""
    if result:
        plan_items = "".join(f"<li>{escape(step)}</li>" for step in result["plan"])
        research_items = "".join(f"<li><pre>{escape(note)}</pre></li>" for note in result["research"])
        result_html = f"""
        <section class=\"card\">
          <h2>Plan</h2>
          <ol>{plan_items}</ol>
        </section>
        <section class=\"card\">
          <h2>Research Notes</h2>
          <ol>{research_items}</ol>
        </section>
        <section class=\"card\">
          <h2>Critique</h2>
          <pre>{escape(result['critique'])}</pre>
        </section>
        <section class=\"card\">
          <h2>Final Response</h2>
          <pre>{escape(result['final'])}</pre>
        </section>
        """

    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>Multi-Agent AI App</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem auto; max-width: 900px; line-height: 1.4; }}
    h1 {{ margin-bottom: 0.25rem; }}
    form {{ margin: 1rem 0 1.5rem; }}
    textarea {{ width: 100%; min-height: 90px; padding: 0.75rem; }}
    button {{ margin-top: 0.6rem; padding: 0.6rem 1rem; cursor: pointer; }}
    .grid {{ display: grid; gap: 1rem; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 1rem; background: #fafafa; }}
    pre {{ white-space: pre-wrap; margin: 0; }}
    .error {{ color: #b00020; font-weight: 700; }}
  </style>
</head>
<body>
  <h1>Multi-Agent AI App</h1>
  <p>Type your task and see planner, researcher, critic, and synthesizer output in the browser.</p>
  {safe_error}
  <form method=\"post\" action=\"/\">
    <label for=\"task\">Task</label>
    <textarea id=\"task\" name=\"task\" placeholder=\"Create a go-to-market plan for a productivity app\">{safe_task}</textarea>
    <br />
    <button type=\"submit\">Run agents</button>
  </form>
  <div class=\"grid\">{result_html}</div>
</body>
</html>"""


class MultiAgentWebHandler(BaseHTTPRequestHandler):
    orchestrator = MultiAgentOrchestrator()

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        self._send_html(render_page())

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/":
            self._send_html(render_page(error="Route not found."), status=404)
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length).decode("utf-8")
        form = parse_qs(payload)
        task = form.get("task", [""])[0].strip()

        if not task:
            self._send_html(render_page(task=task, error="Task is required."), status=400)
            return

        output = self.orchestrator.solve(task)
        self._send_html(render_page(task=task, result=asdict(output)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the browser UI for the multi-agent app.")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind the web server to.")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind the web server to.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    server = ThreadingHTTPServer((args.host, args.port), MultiAgentWebHandler)
    print(f"Serving Multi-Agent AI App at http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
