import time
from PIL import Image, ImageDraw, ImageFont

ANCHO, ALTO = 1080, 1350
MARGEN = 80

FONDO = (16, 13, 13)
ROJO = (255, 72, 38)
BLANCO = (238, 232, 226)
APAGADO = (150, 140, 135)

FUENTE_BOLD = "assets/fuente-bold.ttf"   # títulos y números
FUENTE_REG = "assets/fuente-regular.ttf"  # artistas y textos chicos


def top_semana(con, dias=7, n=5):
    """Las n canciones más escuchadas de los últimos días y el total."""
    desde = int(time.time()) - dias * 86400
    filas = con.execute(
        """
        SELECT cancion, artista, COUNT(*) AS n
        FROM escuchas
        WHERE fecha_utc >= ?
        GROUP BY cancion, artista
        ORDER BY n DESC, MAX(fecha_utc) DESC
        LIMIT ?
        """,
        (desde, n),
    ).fetchall()
    total = con.execute(
        "SELECT COUNT(*) FROM escuchas WHERE fecha_utc >= ?", (desde,)
    ).fetchone()[0]
    return filas, total


def _fuente(ruta, tam):
    return ImageFont.truetype(ruta, tam)


def _cortar(d, texto, fuente, ancho_max):
    if d.textlength(texto, font=fuente) <= ancho_max:
        return texto
    while texto and d.textlength(texto + "…", font=fuente) > ancho_max:
        texto = texto[:-1]
    return texto.rstrip() + "…"


def _ajustar(d, texto, ruta, tam_max, tam_min, ancho_max):
    """Achica la fuente hasta que el texto entre en una línea."""
    for tam in range(tam_max, tam_min - 1, -4):
        f = _fuente(ruta, tam)
        if d.textlength(texto, font=f) <= ancho_max:
            return f
    return _fuente(ruta, tam_min)


def _asterisco(d, cx, cy, r, color, grosor=6):
    """Dibuja un asterisco de 8 puntas."""
    d.line([(cx - r, cy), (cx + r, cy)], fill=color, width=grosor)
    d.line([(cx, cy - r), (cx, cy + r)], fill=color, width=grosor)
    k = int(r * 0.72)
    d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=color, width=grosor)
    d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=color, width=grosor)


def _fondo_con_textura():
    base = Image.new("RGB", (ANCHO, ALTO), FONDO)
    ruido = Image.effect_noise((ANCHO, ALTO), 60).convert("RGB")
    return Image.blend(base, ruido, 0.07)


def _repro(n):
    return f"{n} reproducción" if n == 1 else f"{n} reproducciones"


def generar_flyer(filas, total, ruta="reports/flyer.png"):
    img = _fondo_con_textura()
    d = ImageDraw.Draw(img)
    util = ANCHO - 2 * MARGEN

    # Título
    f_tit = _ajustar(d, "TU SEMANA", FUENTE_BOLD, 190, 80, util)
    d.text((ANCHO // 2, 60), "TU SEMANA", font=f_tit, fill=ROJO, anchor="ma")

    f_sub = _fuente(FUENTE_BOLD, 84)
    d.text((ANCHO // 2, 245), "EN MÚSICA", font=f_sub, fill=ROJO, anchor="ma")
    ancho_sub = d.textlength("EN MÚSICA", font=f_sub)
    for lado in (-1, 1):
        _asterisco(d, int(ANCHO / 2 + lado * (ancho_sub / 2 + 55)), 290, 26, ROJO)

    d.text((ANCHO // 2, 350), "las canciones que más escuchaste",
           font=_fuente(FUENTE_REG, 32), fill=BLANCO, anchor="ma")

    # Canción número 1
    cancion, artista, n = filas[0]
    d.text((MARGEN, 430), "LA #1 DE LA SEMANA",
           font=_fuente(FUENTE_BOLD, 38), fill=APAGADO)
    f_c = _ajustar(d, cancion, FUENTE_BOLD, 130, 52, util)
    d.text((MARGEN, 478), cancion, font=f_c, fill=ROJO)
    f_a = _fuente(FUENTE_REG, 52)
    d.text((MARGEN, 635), _cortar(d, artista, f_a, util), font=f_a, fill=BLANCO)
    d.text((MARGEN, 705), _repro(n), font=_fuente(FUENTE_BOLD, 44), fill=ROJO)

    # Divisoria con asteriscos
    d.line([(MARGEN, 785), (ANCHO - MARGEN, 785)], fill=ROJO, width=3)
    for x in (MARGEN, ANCHO // 2, ANCHO - MARGEN):
        _asterisco(d, x, 785, 16, ROJO, 5)

    # Posiciones 2 a 6 (se muestran como 2, 3, 4, 5, 6)
    f_pos = _fuente(FUENTE_BOLD, 64)
    f_cancion = _fuente(FUENTE_BOLD, 42)
    f_artista = _fuente(FUENTE_REG, 28)
    ancho_texto = util - 220

    y = 830
    for pos, (c, a, k) in enumerate(filas[1:], start=2):
        d.text((MARGEN, y - 6), str(pos), font=f_pos, fill=ROJO)
        d.text((MARGEN + 90, y), _cortar(d, c, f_cancion, ancho_texto),
               font=f_cancion, fill=ROJO)
        d.text((MARGEN + 90, y + 48), _cortar(d, a, f_artista, ancho_texto),
               font=f_artista, fill=BLANCO)
        d.text((ANCHO - MARGEN, y + 8), f"{k}×", font=f_cancion,
               fill=APAGADO, anchor="ra")
        y += 105

    # Pie con asteriscos
    for x in range(MARGEN, ANCHO - MARGEN + 1, (ANCHO - 2 * MARGEN) // 7):
        _asterisco(d, x, ALTO - 55, 18, ROJO, 5)

    img.save(ruta)
    return ruta