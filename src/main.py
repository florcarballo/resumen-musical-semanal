import os
from traer import traer_escuchas
from base import conectar, ultima_fecha, guardar
from flyer import top_semana, generar_flyer
from avisos import enviar_mail

if __name__ == "__main__":
    con = conectar()

    nuevas = traer_escuchas(ultima_fecha(con) + 1)
    guardar(con, nuevas)
    total_base = con.execute("SELECT COUNT(*) FROM escuchas").fetchone()[0]
    print(f"Escuchas nuevas: {len(nuevas)} | Total en la base: {total_base}")

    filas, total_semana = top_semana(con)
    if not filas:
        print("No hay escuchas en los últimos 7 días: no se genera flyer.")
    else:
        ruta = generar_flyer(filas, total_semana)
        print(f"Flyer generado: {ruta}")

        if "EMAIL_USER" in os.environ and "EMAIL_APP_PASSWORD" in os.environ:
            destino = os.environ.get("EMAIL_TO", os.environ["EMAIL_USER"])
            print("Enviando a:", destino)
            enviar_mail(
                "¿Querés conocer tus canciones más escuchadas de la semana? 🎧",
                f"Esta semana escuchaste {total_semana} canciones. "
                f"La que más repetiste fue {filas[0][0]} de {filas[0][1]}. "
                f"Mirá tu top 5 acá abajo.",
                ruta,
            )
            print("Mail enviado.")
        else:
            print("Sin credenciales de mail: se omite el envío.")