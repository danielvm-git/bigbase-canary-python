# story: e01s01
import os
from pathlib import Path

from flask import Flask

_ROOT = Path(__file__).resolve().parents[2]
_HTML_TEMPLATE = (_ROOT / "index.html").read_text()


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def home() -> str:
        version = (_ROOT / "VERSION").read_text().strip()
        return _HTML_TEMPLATE.replace("{{VERSION}}", version)

    return app


def main() -> None:
    # bigbase's deploy engine injects PORT for non-uvicorn Python apps and
    # expects the process itself to bind to it (see bigbase components/deploy/python.go).
    port = int(os.environ.get("PORT", "8080"))
    create_app().run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
