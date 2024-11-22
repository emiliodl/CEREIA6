import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do servidor SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email, subject, body, files=None):
    """
    Envia um email.

    :param to_email: Endereço de email do destinatário.
    :param subject: Assunto do email.
    :param body: Corpo do email.
    """
    from_email = SMTP_USER  # O email do remetente

    # Criação da mensagem
    message = MIMEMultipart()
    message["From"] = from_email  # type: ignore
    message["To"] = to_email
    message["Subject"] = subject

    # Adiciona o corpo do email
    message.attach(MIMEText(body, "plain"))

    if files:
        for file in files:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(file["content"])
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file['name']}",
            )
            message.attach(part)

    # Enviar o email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  # type: ignore
            server.starttls()  # Iniciar TLS (segurança)
            server.login(SMTP_USER, SMTP_PASSWORD)  # type: ignore # Fazer login
            for dest in to_email.split(","):
                try:
                    server.sendmail(from_email, dest, message.as_string())  # type: ignore # Enviar email
                except Exception as e:
                    print(f"Erro ao enviar email para {dest}: {e}")
                    continue
        print("Email enviado com sucesso!")
        return True
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return False
