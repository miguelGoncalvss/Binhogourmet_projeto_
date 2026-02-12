from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import Base, SessionLocal, engine
from app.routers import auth, finance, inventory, pos, recipes, taxes
from app.seed.seed import run_seed

app = FastAPI(title="Binho Gourmet API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


@app.get("/")
def healthcheck():
    return {"message": "API Binho Gourmet online"}


app.include_router(auth.router)
app.include_router(inventory.router)
app.include_router(finance.router)
app.include_router(recipes.router)
app.include_router(pos.router)
app.include_router(taxes.router)
