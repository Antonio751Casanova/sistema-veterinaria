from app.domain.entities.cliente import Cliente
from app.domain.entities.mascota import Mascota
from app.domain.entities.usuario import Usuario
from app.domain.entities.veterinaria import Veterinaria
from app.infrastructure.persistence import models


def veterinaria_to_entity(m: models.Veterinaria) -> Veterinaria:
    return Veterinaria(
        id=m.id, nombre=m.nombre, telefono=m.telefono, direccion=m.direccion,
        email=m.email, hashed_password=m.hashed_password,
    )


def usuario_to_entity(m: models.Usuario) -> Usuario:
    return Usuario(
        id=m.id, nombre=m.nombre, email=m.email, hashed_password=m.hashed_password,
        rol=m.rol, activo=m.activo, veterinaria_id=m.veterinaria_id,
    )


def cliente_to_entity(m: models.Cliente, total_mascotas: int = 0) -> Cliente:
    return Cliente(
        id=m.id, nombre=m.nombre, telefono=m.telefono, email=m.email,
        direccion=m.direccion, fecha_creacion=m.fecha_creacion,
        veterinaria_id=m.veterinaria_id, total_mascotas=total_mascotas,
    )


def mascota_to_entity(m: models.Mascota, con_dueno: bool = False) -> Mascota:
    return Mascota(
        id=m.id, nombre=m.nombre, especie=m.especie, raza=m.raza, edad=m.edad,
        peso=m.peso, notas=m.notas, fecha_creacion=m.fecha_creacion,
        cliente_id=m.cliente_id,
        nombre_dueno=m.cliente.nombre if con_dueno else None,
        telefono_dueno=m.cliente.telefono if con_dueno else None,
    )

