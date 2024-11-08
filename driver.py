from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from io import StringIO
from datetime import datetime, timedelta
import logging


# Inicializar Google Drive
def initialize_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)


# Inicialização do Logger em Memória
def initialize_memory_logger():
    log_stream = StringIO()  # Buffer em memória para os logs
    logger = logging.getLogger("memory_logger")
    logger.setLevel(logging.INFO)

    # Configuração do formato do log
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Criar manipulador de stream
    stream_handler = logging.StreamHandler(log_stream)
    stream_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(stream_handler)

    return logger, log_stream


# Função para enviar o conteúdo do log para o Google Drive
def upload_log_to_drive(drive, logger, log_content):
    try:
        file_name = f'Log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file = drive.CreateFile({"title": file_name})
        file.SetContentString(log_content)
        file.Upload()
        logger.info("Log enviado automaticamente para o Google Drive.")
        return datetime.now()
    except Exception as e:
        logger.error(f"Erro ao enviar o log: {e}")


import os


# Carregar o último upload registrado (usando um arquivo para persistência)
def get_last_upload_time(logger):
    try:
        if os.path.exists("last_upload.txt"):
            with open("last_upload.txt", "r") as file:
                last_upload_str = file.read().strip()
                return datetime.fromisoformat(last_upload_str)
        else:
            return None
    except Exception as e:
        logger.error(f"Erro ao carregar horário do último upload: {e}")
        return None


def should_upload_log(last_upload):
    if not last_upload:
        return True  # Se não houver registro anterior, faça o upload agora
    return datetime.now() >= last_upload + timedelta(minutes=2)


def send(st, drive, logger, log_stream):
    if should_upload_log(last_upload=st.session_state.get("last_upload")):
        last_update = upload_log_to_drive(drive, logger, log_stream.getvalue())
        st.session_state["last_upload"] = last_update
