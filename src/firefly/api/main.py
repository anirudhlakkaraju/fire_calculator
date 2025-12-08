"""Main FastAPI Application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from firefly.api.routes.calculator import router as calculator_routes

app = FastAPI(
    title="LikeAFirefly API",
    description="The greatest tool to assist you on your path to FIRE",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(calculator_routes)


@app.get("/")
def root():
    """Root endpoint - welcome message."""
    return {"message": "Welcome to Firefly API", "docs": "/docs", "health": "/api/health"}


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}
