import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from html import escape


def enviar_mail(asunto, texto, ruta_imagen):
    usuario = os.environ["EMAIL_USER"]
    clave = os.environ["EMAIL_APP_PASSWORD"]
    destino = os.environ.get("EMAIL_TO", usuario)

    cid = make_msgid(domain="resumen-musical")  # identificador de la imagen
    cid_html = cid[1:-1]                        # sin los < >

    # Texto del preview: lo que se ve en la bandeja antes de abrir el mail
    preview = "Tu flyer de la semana ya está listo."

    html = f"""\
<html>
  <body style="margin:0;padding:0;background:#f2f2f2;">
    <span style="display:none;max-height:0;overflow:hidden;opacity:0;">{escape(preview)}</span>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td align="center" style="padding:24px 12px;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                 style="max-width:560px;background:#ffffff;border-radius:12px;">
            <tr>
              <td style="padding:28px 28px 8px;font-family:Arial,sans-serif;">
                <h1 style="margin:0;font-size:24px;color:#111111;">Tu semana en música 🎧</h1>
                <p style="margin:12px 0 0;font-size:16px;line-height:1.5;color:#444444;">
                  {escape(texto)}
                </p>
              </td>
            </tr>
            <tr>
              <td style="padding:16px 28px 28px;">
                <img src="cid:{cid_html}" alt="Tus canciones más escuchadas de la semana"
                     width="504" style="display:block;width:100%;max-width:504px;height:auto;border-radius:8px;">
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""

    msg = EmailMessage()