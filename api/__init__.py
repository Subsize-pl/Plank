"""Plank API package."""

# Layered layout (KAN-6):
#   app/          — FastAPI application, routes, wiring
#   services/     — business logic
#   repositories/ — database access
#   ranking/      — fractional indexing for card ordering
#   realtime/     — WebSocket hub and event broadcasting
