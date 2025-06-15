"""Run the API server with ``python -m agentic_index_api``."""

from .server import app


def main() -> None:
    import uvicorn

    uvicorn.run("agentic_index_api.server:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
