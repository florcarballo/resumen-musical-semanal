from traer import traer_escuchas
from base import conectar, ultima_fecha, guardar

if __name__ == "__main__":
    con = conectar()

    desde = ultima_fecha(con) + 1
    nuevas = traer_escuchas(desde)
    guardar(con, nuevas)

    total = con.execute("SELECT COUNT(*) FROM escuchas").fetchone()[0]
    print(f"Escuchas nuevas traídas: {len(nuevas)}")
    print(f"Total en la base: {total}")