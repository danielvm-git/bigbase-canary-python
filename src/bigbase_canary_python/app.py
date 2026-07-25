# story: e01s01
import os
from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def home() -> str:
        version = (Path(__file__).resolve().parents[2] / "VERSION").read_text().strip()
        return f"<h1>bigbase canary (Python)</h1><footer>v{version}</footer>"

    return app


def main() -> None:
    # bigbase's deploy engine injects PORT for non-uvicorn Python apps and
    # expects the process itself to bind to it (see bigbase components/deploy/python.go).
    port = int(os.environ.get("PORT", "8080"))
    create_app().run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
