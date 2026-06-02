import uvicorn
from fastapi import FastAPI
from .routes import router
from .database import engine, Base
import asyncio

app = FastAPI(title="TaskMaster API")
app.include_router(router)

@app.on_event("startup")
async def startup():
    # create tables if not exist (for demo; use alembic in production)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to TaskMaster API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
