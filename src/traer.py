import os
import requests

URL = "https://ws.audioscrobbler.com/2.0/"


def traer_escuchas(desde_ts=0):
    """Devuelve las escuchas posteriores a desde_ts (timestamp Unix)."""
    api_key = os.environ["LASTFM_API_KEY"]
    usuario = os.environ["LASTFM_USER"]

    filas, pagina = [], 1
    while True:
        params = {
            "method": "user.getrecenttracks",
            "user": usuario,
            "api_key": api_key,
            "format": "json",
            "limit": 200,
            "page": pagina,
            "from": desde_ts,
        }
        r = requests.get(URL, params=params, timeout=30)
        r.raise_for_status()
        datos = r.json()["recenttracks"]

        pistas = datos["track"]
        if isinstance(pistas, dict):  # cuando hay una sola, viene como dict
            pistas = [pistas]

        for t in pistas:
            if t.get("@attr", {}).get("nowplaying"):
                continue  # ignorar la que suena ahora
            filas.append({
                "fecha_utc": int(t["date"]["uts"]),
                "artista": t["artist"]["#text"],
                "cancion": t["name"],
                "album": t["album"]["#text"],
            })

        if pagina >= int(datos["@attr"]["totalPages"]):
            break
        pagina += 1
    return filas


if __name__ == "__main__":
    escuchas = traer_escuchas()
    print(f"Escuchas traídas: {len(escuchas)}")
    for e in escuchas[:5]:
        print(e)