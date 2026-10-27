import os
import sqlite3


def ensure_migrations() -> None:
    """Guard de startup: verifica que las migraciones necesarias existen."""
    # backend/auth.db (esta carpeta es backend/app/infrastructure/persistence)
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "auth.db")
    conn = sqlite3.connect(db_path)
    cita_cols = [r[1] for r in conn.execute("PRAGMA table_info(citas)").fetchall()]
    notif_cols = [r[1] for r in conn.execute("PRAGMA table_info(notificaciones)").fetchall()]
    lista_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='lista_espera'"
    ).fetchone() is not None
    lista_cols = [r[1] for r in conn.execute("PRAGMA table_info(lista_espera)").fetchall()] if lista_exists else []
    if cita_cols and "duracion_minutos" not in cita_cols:
        conn.execute("ALTER TABLE citas ADD COLUMN duracion_minutos INTEGER NOT NULL DEFAULT 60")
        conn.commit()
    if notif_cols and "destinatario_usuario_id" not in notif_cols:
        conn.execute("ALTER TABLE notificaciones ADD COLUMN destinatario_usuario_id INTEGER")
        conn.commit()
    if lista_cols and "hora_inicio_preferida" not in lista_cols:
        conn.execute("ALTER TABLE lista_espera ADD COLUMN hora_inicio_preferida INTEGER")
        conn.commit()
    if lista_cols and "hora_fin_preferida" not in lista_cols:
        conn.execute("ALTER TABLE lista_espera ADD COLUMN hora_fin_preferida INTEGER")
        conn.commit()
    conn.close()
    if cita_cols and "confirmation_token" not in cita_cols:
        raise RuntimeError(
            "Migración requerida. Ejecuta: python _backup_avances_futuros/migrate_confirmation_token.py"
        )

