import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do servidor SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send_email(to_email, subject, body):
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
    # Enviar o email
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:  # type: ignore
            server.starttls()  # Iniciar TLS (segurança)
            server.login(SMTP_USER, SMTP_PASSWORD)  # type: ignore # Fazer login
            server.sendmail(from_email, to_email, message.as_string())  # type: ignore # Enviar email
        # print("Email enviado com sucesso!")
        return True
    except Exception as e:
        # print(f"Ocorreu um erro: {e}")
        return False
