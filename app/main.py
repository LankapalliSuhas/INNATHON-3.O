from fastapi import FastAPI
from app.api.routes_ingest import router as ingest_router
from app.api.routes_frontend import router as frontend_router
from app.api.routes_control import router as control_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="VoltWise Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest_router, prefix="/api")
app.include_router(frontend_router, prefix="/api")
app.include_router(control_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "VoltWise Backend Running"}