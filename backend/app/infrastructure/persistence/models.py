from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .database import Base


class Veterinaria(Base):
    """Modelo de Veterinaria"""
    __tablename__ = "veterinarias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    direccion = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relación con clientes
    clientes = relationship("Cliente", back_populates="veterinaria", cascade="all, delete-orphan")
    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="veterinaria", cascade="all, delete-orphan")


class Usuario(Base):
    """Modelo de Usuario — veterinario o secretaria bajo una veterinaria"""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)  # "veterinario" | "secretaria"
    activo = Column(Integer, default=1)  # 0=inactivo, 1=activo

    # Relación con veterinaria
    veterinaria_id = Column(Integer, ForeignKey("veterinarias.id"), nullable=False)
    veterinaria = relationship("Veterinaria", back_populates="usuarios")

    # Citas asignadas (solo para veterinarios)
    citas_asignadas = relationship("Cita", back_populates="veterinario_asignado", foreign_keys="Cita.veterinario_asignado_id")


class Cliente(Base):
    """Modelo de Cliente (solo datos del dueño)"""
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos del dueño
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100), nullable=True)
    direccion = Column(String(255), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con veterinaria
    veterinaria_id = Column(Integer, ForeignKey("veterinarias.id"), nullable=False)
    veterinaria = relationship("Veterinaria", back_populates="clientes")
    
    # Relación con mascotas
    mascotas = relationship("Mascota", back_populates="cliente", cascade="all, delete-orphan")


class Mascota(Base):
    """Modelo de Mascota"""
    __tablename__ = "mascotas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)  # Perro, Gato, Ave, etc.
    raza = Column(String(100), nullable=True)
    edad = Column(String(20), nullable=True)  # ej: "2 años", "6 meses"
    peso = Column(String(20), nullable=True)  # ej: "5.5 kg"
    notas = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con cliente (dueño)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    cliente = relationship("Cliente", back_populates="mascotas")
    
    # Relación con bitácora
    entradas_bitacora = relationship("Bitacora", back_populates="mascota", cascade="all, delete-orphan")
    
    # Relación con citas
    citas = relationship("Cita", back_populates="mascota", cascade="all, delete-orphan")


class Bitacora(Base):
    """Modelo de Bitácora - historial médico de la mascota"""
    __tablename__ = "bitacoras"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    tipo = Column(String(50), nullable=False)  # Consulta, Vacuna, Cirugía, Desparasitación, etc.
    descripcion = Column(Text, nullable=False)
    tratamiento = Column(Text, nullable=True)
    medicamentos = Column(Text, nullable=True)
    costo = Column(String(20), nullable=True)  # ej: "$500.00"
    proxima_cita = Column(DateTime, nullable=True)
    
    # Relación con mascota
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("Mascota", back_populates="entradas_bitacora")


class Cita(Base):
    """Modelo de Cita - agendamiento de futuras visitas"""
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime, nullable=False)
    tipo_atencion = Column(String(100), nullable=False)  # Consulta, Vacunación, etc. o personalizado
    descripcion = Column(Text, nullable=True)
    tratamiento = Column(Text, nullable=True)
    medicamento = Column(Text, nullable=True)
    costo = Column(String(20), nullable=True)
    duracion_minutos = Column(Integer, nullable=False, default=60)
    
    # Estados: pendiente, confirmado, rechazado, en_espera, completado
    estado = Column(String(20), default="pendiente", nullable=False)

    # Token público para confirmación/rechazo por el cliente (sin JWT)
    confirmation_token = Column(String(36), unique=True, nullable=True, index=True,
                                default=lambda: str(uuid.uuid4()))

    # Recordatorios
    recordatorio_whatsapp_enviado = Column(Integer, default=0)  # 0=no, 1=sí
    recordatorio_email_enviado = Column(Integer, default=0)
    
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación con mascota
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("Mascota", back_populates="citas")

    # Veterinario asignado (nullable para citas existentes)
    veterinario_asignado_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    veterinario_asignado = relationship("Usuario", back_populates="citas_asignadas", foreign_keys=[veterinario_asignado_id])


class ListaEspera(Base):
    """Modelo de lista de espera para cubrir huecos por cancelaciones"""
    __tablename__ = "lista_espera"

    id = Column(Integer, primary_key=True, index=True)
    tipo_atencion = Column(String(100), nullable=False)
    duracion_minutos = Column(Integer, nullable=False, default=60)
    prioridad = Column(Integer, nullable=False, default=0)  # mayor = más urgente
    hora_inicio_preferida = Column(Integer, nullable=True)  # 0..23
    hora_fin_preferida = Column(Integer, nullable=True)  # 0..23
    notas = Column(Text, nullable=True)
    estado = Column(String(20), nullable=False, default="activa")  # activa, contactado, convertida, descartada
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)

    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    mascota = relationship("Mascota")

    veterinaria_id = Column(Integer, ForeignKey("veterinarias.id"), nullable=False)

    preferencia_veterinario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    preferencia_veterinario = relationship("Usuario")


class Notificacion(Base):
    """Modelo de Notificación interna para el admin"""
    __tablename__ = "notificaciones"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)  # recordatorio_cita, cita_proxima, etc.
    mensaje = Column(Text, nullable=False)
    leida = Column(Integer, default=0)  # 0=no leída, 1=leída
    fecha_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relación opcional con cita
    cita_id = Column(Integer, ForeignKey("citas.id"), nullable=True)
    cita = relationship("Cita", backref="notificaciones")

    # Usuario destino (opcional). Si es null, es notificación general de veterinaria.
    destinatario_usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    destinatario_usuario = relationship("Usuario")
    
    # Relación con veterinaria
    veterinaria_id = Column(Integer, ForeignKey("veterinarias.id"), nullable=False)
