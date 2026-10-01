import os
import smtplib
from email.message import EmailMessage


def enviar_mail(asunto, texto, ruta_imagen):
    usuario = os.environ["EMAIL_USER"]
    clave = os.environ["EMAIL_APP_PASSWORD"]
    destino = os.environ.get("EMAIL_TO", usuario)

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = usuario
    msg["To"] = destino
    msg.set_content(texto)

    with open(ruta_imagen, "rb") as f:
        msg.add_attachment(f.read(), maintype="image",
                           subtype="png", filename="mi-semana-en-musica.png")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(usuario, clave)
        smtp.send_message(msg)