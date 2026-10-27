from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.api.error_handlers import register_error_handlers
from app.infrastructure.persistence import models  # noqa: F401  (registra todas las tablas en Base)
from app.infrastructure.persistence.database import Base, engine
from app.infrastructure.persistence.startup_guard import ensure_migrations

# --- Routers del Avance 1 ---
from app.infrastructure.api.routers import (
    auth_router, usuarios_router, clientes_router, mascotas_router,
)

# --- Routers de avances futuros (definidos, pero NO expuestos todavía) ---
# TODO: Activar en Avance 2 / Avance 3
# from app.infrastructure.api.routers import (
#     citas_router, lista_espera_router, notificaciones_router,
#     estadisticas_router, bitacora_router,
# )

# Create database tables
Base.metadata.create_all(bind=engine)

ensure_migrations()

app = FastAPI(
    title="Sistema de Veterinarias API",
    description="API para gestión de veterinarias, clientes y mascotas",
    version="3.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4321",
        "http://localhost:4322",
        "http://localhost:3000",
        "http://127.0.0.1:4321",
        "http://127.0.0.1:4322",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "Authorization", "Content-Type", "Accept"],
    expose_headers=["*"],
)

register_error_handlers(app)


# ==================== Root ====================

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Sistema de Veterinarias API v3.0 - Bienvenido!"}


# ==================== Routers (Avance 1) ====================

app.include_router(auth_router.router)
app.include_router(usuarios_router.router)
app.include_router(clientes_router.router)
app.include_router(mascotas_router.router)

# ==================== Routers (avances futuros) ====================
# TODO: Activar en Avance 2 / Avance 3
# app.include_router(bitacora_router.router)          # Avance 2
# app.include_router(citas_router.router)             # Avance 2
# app.include_router(lista_espera_router.router)      # Avance 3
# app.include_router(notificaciones_router.router)    # Avance 3
# app.include_router(estadisticas_router.router)      # Avance 3
