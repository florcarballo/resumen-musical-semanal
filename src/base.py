import sqlite3

RUTA = "data/escuchas.db"


def conectar():
    con = sqlite3.connect(RUTA)
    con.execute("""
        CREATE TABLE IF NOT EXISTS escuchas (
            fecha_utc INTEGER,
            artista   TEXT,
            cancion   TEXT,
            album     TEXT,
            PRIMARY KEY (fecha_utc, artista, cancion)
        )
    """)
    return con


def ultima_fecha(con):
    """Timestamp de la escucha más reciente guardada (0 si la base está vacía)."""
    fila = con.execute("SELECT MAX(fecha_utc) FROM escuchas").fetchone()
    return fila[0] or 0


def guardar(con, filas):
    """Inserta las escuchas, ignorando las que ya existen."""
    con.executemany(
        "INSERT OR IGNORE INTO escuchas VALUES (:fecha_utc, :artista, :cancion, :album)",
        filas,
    )
    con.commit()