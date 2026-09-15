"""Application entrypoint: the FastAPI app factory."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the Plank API application."""
    app = FastAPI(title="Plank API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        # Placeholder until KAN-25 wires in a real database check.
        return {"status": "ok"}

    return app


app = create_app()
