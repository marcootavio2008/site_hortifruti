import smtplib
from email.message import EmailMessage
import os

def enviar_email(registro):
    msg = EmailMessage()
    msg["Subject"] = f"Relatório: {registro.tipo.upper()}"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_DESTINO")

    msg.set_content(
        f"""
Tipo: {registro.tipo}
Produto: {registro.produto}
Quantidade: {registro.quantidade}
Data: {registro.data_registro}
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(
            os.getenv("EMAIL_USER"),
            os.getenv("EMAIL_PASS")
        )
        smtp.send_message(msg)
