# Sistema ERP y CRM Veterinario

## Avance 1: Arquitectura Base (Clean Architecture + SOLID), Módulo de Usuarios/Roles (ERP) y Módulo de Clientes y Mascotas (CRM)

Este avance contiene la base del sistema:

- **Arquitectura Base**: backend organizado con Clean Architecture y principios SOLID.
- **Módulo de Usuarios/Roles (ERP)**: autenticación JWT y control de acceso por roles.
- **Módulo de Clientes y Mascotas (CRM)**: gestión de clientes (dueños) y sus mascotas.

## Arquitectura del backend (`backend/app/`)

```
domain/            # Entidades, interfaces de repositorios/servicios (ABC), excepciones
application/       # DTOs (Pydantic) y casos de uso (una responsabilidad por clase)
infrastructure/
  persistence/     # SQLAlchemy: database, models, repositorios concretos, unit of work
  security/        # JWT y hashing de contraseñas
  api/routers/     # Routers FastAPI (auth, usuarios, clientes, mascotas + avances futuros)
main.py            # Composición de la app; routers de Avance 2/3 comentados (TODO)
```

## Tecnologías

- **Backend**: FastAPI, SQLAlchemy, SQLite, PyJWT
- **Frontend**: Astro, Tailwind CSS, TypeScript

## Instalación y ejecución

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API: `http://localhost:8000` — Documentación: `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:4321`
