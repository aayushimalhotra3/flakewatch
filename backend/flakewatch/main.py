from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import routes_ci
from . import routes_tests
from .routes_debug import router as debug_router

app = FastAPI(title="FlakeWatch API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_ci.router)
app.include_router(routes_tests.router)
app.include_router(debug_router, prefix="/debug")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "flakewatch-api"}
