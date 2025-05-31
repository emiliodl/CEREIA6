from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import logging
from datetime import datetime
import io
from models.filters import (
    filtrar_estudos_tipo_tumor,
    filtrar_estudos_estadiamento,
    filtrar_por_ecog,
    filtrar_estudos_por_biomarcadores
)
from models.email_sender import send_email

app = Flask(__name__)
CORS(app)  # Permitir requisições de origens diferentes

# Configurar logging
log_buffer = io.StringIO()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CEREIA-API")
handler = logging.StreamHandler(log_buffer)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Carregando dados
estudos_df = pd.read_csv("../df_final_matches_tipo_cancer_atualizado.csv")

@app.route('/api/tumor-types', methods=['GET'])
def get_tumor_types():
    # Corrigida a importação
    from dicionarios import biomarcadores_dict
    return jsonify(list(biomarcadores_dict.keys()))

@app.route('/api/biomarkers', methods=['GET'])
def get_biomarkers():
    # Corrigida a importação
    from dicionarios import biomarcadores_dict, opcoes_biomarcadores
    tumor_type = request.args.get('tumor_type')
    if tumor_type in biomarcadores_dict:
        result = {}
        for biomarcador in biomarcadores_dict[tumor_type]:
            if biomarcador == "Ki-67":
                result[biomarcador] = {"type": "input"}
            else:
                result[biomarcador] = {
                    "type": "select",
                    "options": opcoes_biomarcadores.get(biomarcador, [])
                }
        return jsonify(result)
    return jsonify({})

@app.route('/api/studies', methods=['POST'])
def get_studies():
    filters = request.json
    filtered_studies = estudos_df.copy()
    
    # Inicializar a coluna biomarcador_match como True para todos os registros
    filtered_studies['biomarcador_match'] = True
    
    # Aplicar filtros
    if filters.get('tipo_tumor'):
        filtered_studies = filtrar_estudos_tipo_tumor(filtered_studies, filters['tipo_tumor'])
    
    if filters.get('estadiamento'):
        filtered_studies = filtrar_estudos_estadiamento(filtered_studies, filters['estadiamento'])
    
    if filters.get('valor_ecog'):
        filtered_studies = filtrar_por_ecog(filtered_studies, filters['valor_ecog'])
    
    # Aplicar filtro de biomarcadores
    if filters.get('biomarcadores'):
        filtered_studies = filtrar_estudos_por_biomarcadores(filtered_studies, filters.get('biomarcadores', {}))
    
    # Ordenar estudos para que os correspondentes apareçam primeiro
    filtered_studies = filtered_studies.sort_values(by="biomarcador_match", ascending=False)
    
    # Preparar resultados
    studies_data = []
    for _, row in filtered_studies.iterrows():
        studies_data.append({
            'nctId': row['nctId'],
            'briefTitle': row['briefTitle'],
            'eligibilityCriteria': row['eligibilityCriteria'],
            'biomarcador_match': bool(row['biomarcador_match'])
        })
    
    return jsonify(studies_data)

@app.route('/api/send-email', methods=['POST'])
def send_email_endpoint():
    data = request.json
    carteirinha = data.get('carteirinha', '')
    medico = data.get('medico', '')
    filtros = data.get('filtros', {})
    ids_estudos = data.get('ids_estudos', [])
    
    logger.info(f"Email será enviado")
    logger.info(f"Tipo de tumor {filtros.get('tipo_tumor', '')}")
    logger.info(f"Carteirinha:{carteirinha} Medico:{medico}")
    
    # Gera os links simples dos estudos
    links_estudos = [f"https://clinicaltrials.gov/study/{id_estudo}" for id_estudo in ids_estudos]
    links_estudos_str = "\n".join(links_estudos)
    
    corpo_email = f"""
    Filtros Selecionados:
    - Tipo de Tumor: {filtros.get('tipo_tumor', '')}
    - Estadiamento: {filtros.get('estadiamento', '')}
    - ECOG: {filtros.get('valor_ecog', '')}
    - Biomarcadores Selecionados: {filtros.get('biomarcadores', {})}
    
    Informações do Paciente:
    - Carteirinha: {carteirinha}
    - Médico: {medico}
    
    Estudos Filtrados:
    {links_estudos_str}
    """
    
    # Emails fixos
    emails_fixos = "t_carlos.campos@hapvida.com.br,arnaldoshiomi@yahoo.com.br,t_joaquim.sousa@hapvida.com.br"
    
    result = send_email(emails_fixos, "Resultados dos Filtros de Estudos Clínicos", corpo_email)
    
    # Enviar logs por email
    log_buffer.seek(0)
    send_email(
        "Kelly.lima.88@gmail.com",
        "Logs de utilização",
        "Segue em anexo o arquivo de log",
        [
            {
                "name": f"{datetime.now()}.log",
                "content": log_buffer.read().encode("utf-8"),
            }
        ],
    )
    
    if result:
        return jsonify({"success": True, "message": "Email enviado com sucesso!"})
    else:
        return jsonify({"success": False, "message": "Falha ao enviar o email."}), 500

@app.route('/api/staging-options', methods=['GET'])
def get_staging_options():
    # Retorna os estadiamentos como valores romanos (I, II, III, IV)
    from dicionarios import equivalencia_estadiamento
    return jsonify(list(equivalencia_estadiamento.keys()))

if __name__ == '__main__':
    app.run(debug=True, port=5000)