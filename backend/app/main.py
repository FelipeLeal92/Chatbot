import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat
from app.core.database import async_engine, Base

async def create_tables():
    async with async_engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Optional: drop tables for a clean start
        await conn.run_sync(Base.metadata.create_all)

async def startup_event_handler():
    print("Creating database tables...")
    await create_tables()
    print("Startup complete.")

app = FastAPI()

app.add_event_handler("startup", startup_event_handler)

# Permite que o widget rode em qualquer site (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)

# Configuração para servir o Frontend (Widget) estático
# O script de build colocará os arquivos em backend/app/static
static_dir = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(static_dir):
    # Monta os arquivos estáticos na raiz. 
    # html=True faz com que acessar "/" carregue o index.html automaticamente
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"message": "API running (Frontend not built yet)"}
