"""
Script para inicializar una base de datos limpia (auth.db) para el Avance 1:
- 1 Veterinaria de prueba
- 3 Usuarios (1 Administrador, 1 Veterinario, 1 Recepcionista)
- 5 Clientes (dueños)
- 6 Mascotas vinculadas a esos clientes

Ejecutar desde el directorio backend:
    python seed_data.py
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.persistence.database import Base, SessionLocal, engine
from app.infrastructure.persistence.models import Cliente, Mascota, Usuario, Veterinaria
from app.infrastructure.security.password_hasher import PasslibPasswordHasher


def seed_database() -> None:
    # Reiniciar el esquema sobre auth.db para garantizar una base limpia
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    hasher = PasslibPasswordHasher()
    default_pwd = hasher.hash("123456")
    now = datetime.utcnow()

    db = SessionLocal()
    try:
        # 1. Veterinaria principal
        vet = Veterinaria(
            nombre="Clínica Veterinaria VetPets",
            telefono="5551234567",
            direccion="Av. Insurgentes Sur #450, Col. Roma Norte, CDMX",
            email="admin@vetpets.com",
            hashed_password=default_pwd,
        )
        db.add(vet)
        db.flush()

        # 2. Tres usuarios de prueba (1 Administrador, 1 Veterinario, 1 Recepcionista)
        # Nota: en el modelo RBAC actual los permisos administrativos corresponden al rol "secretaria".
        usuarios_data = [
            {
                "nombre": "Carlos Mendoza (Administrador)",
                "email": "admin@vetpets.com",
                "rol": "secretaria",
            },
            {
                "nombre": "Dra. Laura Gómez",
                "email": "veterinario@vetpets.com",
                "rol": "veterinario",
            },
            {
                "nombre": "Ana Torres (Recepcionista)",
                "email": "recepcion@vetpets.com",
                "rol": "secretaria",
            },
        ]
        for u in usuarios_data:
            db.add(Usuario(
                nombre=u["nombre"],
                email=u["email"],
                hashed_password=default_pwd,
                rol=u["rol"],
                activo=1,
                veterinaria_id=vet.id,
            ))

        # 3. Cinco clientes (dueños)
        clientes_data = [
            {
                "nombre": "Juan Antonio Pérez García",
                "telefono": "5512345601",
                "email": "juan.perez@gmail.com",
                "direccion": "Calle Medellín #112, Col. Roma Norte",
                "dias_atras": 25,
            },
            {
                "nombre": "María Fernanda López Hernández",
                "telefono": "5512345602",
                "email": "mfernanda.lopez@outlook.com",
                "direccion": "Av. Coyoacán #830, Col. Del Valle",
                "dias_atras": 18,
            },
            {
                "nombre": "Roberto Sánchez Ramírez",
                "telefono": "5512345603",
                "email": "roberto.sanchez@gmail.com",
                "direccion": "Calle Ámsterdam #45, Col. Condesa",
                "dias_atras": 12,
            },
            {
                "nombre": "Sofía Martínez Torres",
                "telefono": "5512345604",
                "email": "sofia.mtz@hotmail.com",
                "direccion": "Av. Universidad #1200, Col. Xoco",
                "dias_atras": 6,
            },
            {
                "nombre": "Diego Alejandro Cruz Morales",
                "telefono": "5512345605",
                "email": "diego.cruz@gmail.com",
                "direccion": "Calle Durango #215, Col. Roma Norte",
                "dias_atras": 2,
            },
        ]

        clientes: list[Cliente] = []
        for c in clientes_data:
            cliente = Cliente(
                veterinaria_id=vet.id,
                nombre=c["nombre"],
                telefono=c["telefono"],
                email=c["email"],
                direccion=c["direccion"],
                fecha_creacion=now - timedelta(days=c["dias_atras"]),
            )
            db.add(cliente)
            db.flush()
            clientes.append(cliente)

        # 4. Seis mascotas vinculadas a los 5 clientes (el primer cliente tiene 2 mascotas)
        mascotas_data = [
            {
                "cliente": clientes[0],
                "nombre": "Max",
                "especie": "Perro",
                "raza": "Golden Retriever",
                "edad": "3 años",
                "peso": "28.5 kg",
                "notas": "Vacunas al día. Muy dócil durante la consulta.",
            },
            {
                "cliente": clientes[0],
                "nombre": "Luna",
                "especie": "Gato",
                "raza": "Siamés",
                "edad": "2 años",
                "peso": "3.8 kg",
                "notas": "Esterilizada. Sensible a cambios de alimento.",
            },
            {
                "cliente": clientes[1],
                "nombre": "Rocky",
                "especie": "Perro",
                "raza": "Bulldog Francés",
                "edad": "4 años",
                "peso": "12.2 kg",
                "notas": "Alérgico al pollo; vigilar respiración en días calurosos.",
            },
            {
                "cliente": clientes[2],
                "nombre": "Michi",
                "especie": "Gato",
                "raza": "Mestizo",
                "edad": "1 año",
                "peso": "4.1 kg",
                "notas": "Sin alergias conocidas. Desparasitación reciente.",
            },
            {
                "cliente": clientes[3],
                "nombre": "Kira",
                "especie": "Perro",
                "raza": "Pastor Alemán",
                "edad": "5 años",
                "peso": "31.0 kg",
                "notas": "Nerviosa con otros perros; usar bozal preventivo en revisión.",
            },
            {
                "cliente": clientes[4],
                "nombre": "Coco",
                "especie": "Ave",
                "raza": "Loro Amazónico",
                "edad": "2 años",
                "peso": "420 g",
                "notas": "Revisión periódica de plumaje y recorte de pico.",
            },
        ]

        for m in mascotas_data:
            db.add(Mascota(
                cliente_id=m["cliente"].id,
                nombre=m["nombre"],
                especie=m["especie"],
                raza=m["raza"],
                edad=m["edad"],
                peso=m["peso"],
                notas=m["notas"],
                fecha_creacion=now,
            ))

        db.commit()

        print("=== Base de datos inicializada correctamente (auth.db) ===")
        print(f"Veterinaria: {vet.nombre} (ID: {vet.id})")
        print(f"Usuarios creados: {db.query(Usuario).count()} (contraseña de prueba: 123456)")
        for u in db.query(Usuario).order_by(Usuario.id).all():
            print(f"  - [{u.rol}] {u.nombre} <{u.email}>")
        print(f"Clientes creados: {db.query(Cliente).count()}")
        print(f"Mascotas creadas: {db.query(Mascota).count()}")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
