import streamlit as st
# import streamlit_analytics
st.set_page_config(layout="wide")
import pandas as pd
import ast
import logging
from pathlib import Path
from datetime import datetime
import urllib.parse
from sender import send_email
from dicionarios import (
    equivalencia_estadiamento,
    bio_to_column,
    biomarcadores_dict,
    opcoes_biomarcadores,
    mesh_dict,
)
# streamlit_analytics.start_tracking()
# or pass the same arg to `stop_tracking`
import logging, io

last_send_logger_email = None

log_buffer = io.StringIO()
# Criar um logger nomeado (opcional)
logger = logging.getLogger("CEREIA 06 - MVP")
handler = logging.StreamHandler(log_buffer)
# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,  # Nível mínimo de mensagens que serão registradas
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Formato da mensagem
)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# logger.info("Refresh page")
from streamlit.components.v1 import html

GA_ID = "google_analytics"
GA_TRACKING_CODE = f"""
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-R7SSHJPNRZ"></script>
<script id='{GA_ID}'>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());

  gtag('config', 'G-R7SSHJPNRZ');
</script>
"""

from bs4 import BeautifulSoup
import pathlib
import shutil


def inject_ga():
    
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    soup = BeautifulSoup(index_path.read_text(), features="html.parser")
    if not soup.find(id=GA_ID): 
        bck_index = index_path.with_suffix('.bck')
        if bck_index.exists():
            shutil.copy(bck_index, index_path)  
        else:
            shutil.copy(index_path, bck_index)  
        html = str(soup)
        new_html = html.replace('<head>', '<head>\n' + GA_TRACKING_CODE)
        index_path.write_text(new_html)

inject_ga()

def contar_envios():
    log_file = Path("email_send_log.log")
    if log_file.exists():
        with open(log_file, "r") as f:
            lines = f.readlines()
            return sum(1 for line in lines if "Email enviado" in line)
    return 0


def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")

file_path = "df_final_matches_tipo_cancer_atualizado.csv"
if "original_data" not in st.session_state:
    st.session_state["original_data"] = pd.read_csv(file_path)
estudos_df = st.session_state["original_data"]


def filtrar_estudos_tipo_tumor(df, tipo_tumor, termo_2=None):
    colunas_esperadas = ["term_1", "term_2", "term_3", "term_4", "term_5"]
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            raise KeyError(f"A coluna '{coluna}' não existe no DataFrame.")

    if tipo_tumor:
        mask = (
            df["term_1"].str.strip().eq(tipo_tumor)
            | df["term_2"].str.strip().eq(tipo_tumor)
            | df["term_3"].str.strip().eq(tipo_tumor)
            | df["term_4"].str.strip().eq(tipo_tumor)
            | df["term_5"].str.strip().eq(tipo_tumor)
        )
        if termo_2:
            mask &= (
                df["term_1"].str.strip().eq(termo_2)
                | df["term_2"].str.strip().eq(termo_2)
                | df["term_3"].str.strip().eq(termo_2)
                | df["term_4"].str.strip().eq(termo_2)
                | df["term_5"].str.strip().eq(termo_2)
            )
        filtered_df = df[mask]
        if filtered_df.empty:
            st.warning(
                "Nenhum registro encontrado para o tipo de câncer e termo selecionados."
            )
        return filtered_df
    else:
        return df


def converter_lista_string_para_lista(string_lista):
    try:
        return ast.literal_eval(string_lista)
    except (ValueError, SyntaxError):
        return []


def filtrar_estudos_estadiamento(df, estadiamento):
    if estadiamento:
        estadiamentos_reverso = {}

        for k, v in equivalencia_estadiamento.items():
            for x in v:
                estadiamentos_reverso[x] = k

        estadiamentos_equivalentes = equivalencia_estadiamento[
            estadiamentos_reverso[estadiamento]
        ]
        if not estadiamentos_equivalentes:
            print(
                f"Estadiamento '{estadiamento}' não encontrado no dicionário de equivalência."
            )
            return df

        estadiamentos_df = df["Tipo_stages"].apply(converter_lista_string_para_lista)
        filtrado = df[
            estadiamentos_df.apply(
                lambda x: any(item in estadiamentos_equivalentes for item in x)
            )
        ]

        if filtrado.empty:
            st.warning("Nenhum registro encontrado para o estadiamento selecionado.")
        return filtrado
    else:
        return df


def filtrar_por_ecog(df, valor_ecog):
    if valor_ecog:
        if "Tem ECOG" not in df.columns:
            raise KeyError("A coluna 'Tem ECOG' não existe no DataFrame.")

        df["ECOG_score"] = df["ECOG_score"].str.strip()
        df_filtrado = df[
            df["ECOG_score"].str.contains(valor_ecog, case=False, na=False)
        ]

        if df_filtrado.empty:
            st.warning("Nenhum registro encontrado para o valor do ECOG selecionado.")

        return df_filtrado
    else:
        return df


def filtrar_estudos_por_biomarcadores(df, selecoes_biomarcadores):
    df = df.copy()
    df["biomarcador_match"] = True  # Assume all studies match initially

    for biomarcador, valor in selecoes_biomarcadores.items():
        if valor:
            coluna = bio_to_column.get(biomarcador)
            if coluna:
                if coluna in df.columns:
                    df[coluna] = df[coluna].fillna("")
                    match = df[coluna] == valor
                    df["biomarcador_match"] &= match
                    print(f"Aplicando filtro: {coluna} == {valor}")
    # logger.info(
    #     f"Total de registros encontrados: {df['biomarcador_match'].sum()} de {len(df)}"
    # )
    return df


def exibir_biomarcadores_e_opcoes(tipo_tumor):
    biomarcadores = biomarcadores_dict.get(tipo_tumor, [])
    selecoes = {}

    for biomarcador in biomarcadores:
        if biomarcador == "Ki-67":
            # Caixa de texto para entrada numérica
            selecoes[biomarcador] = st.text_input(
                f"Insira o valor para {biomarcador} (%)"
            )
        else:
            # Selectbox para opções predefinidas
            opcoes = opcoes_biomarcadores.get(biomarcador, [])
            selecoes[biomarcador] = st.selectbox(
                f"Selecione a opção para {biomarcador}", options=opcoes, index=None
            )

    return selecoes


def gerar_link_email(filtros, carteirinha, ids_estudos):
    assunto = "Resultados dos Filtros de Estudos Clínicos"

    # Gera os links simples dos estudos
    links_estudos = [
        f"https://clinicaltrials.gov/study/{id_estudo}" for id_estudo in ids_estudos
    ]

    links_estudos_str = "\n".join(
        links_estudos
    )  # Junta todos os links em uma única string, separados por nova linha
    logger.info("Estudos finais")
    for i in links_estudos:
        logger.info(i)
    corpo_email = f"""
    Filtros Selecionados:
    - Tipo de Tumor: {filtros['tipo_tumor']}
    - Estadiamento: {filtros['estadiamento']}
    - ECOG: {filtros['valor_ecog']}
    - Biomarcadores Selecionados: {filtros['biomarcadores']}
    
    Informações do Paciente:
    - Carteirinha: {carteirinha}
    
    Estudos Filtrados:
    {links_estudos_str}
    """

    # Codifica o corpo do email e o assunto para serem usados em uma URL
    # corpo_email_encoded = urllib.parse.quote(corpo_email)
    # assunto_encoded = urllib.parse.quote(assunto)

    # Emails fixos
    emails_fixos = "t_carlos.campos@hapvida.com.br,arnaldoshiomi@yahoo.com.br,t_joaquim.sousa@hapvida.com.br"
    # emails_fixos = "jassonjcs11@gmail.com"

    output_result = send_email(emails_fixos, assunto, corpo_email)

    return output_result


if __name__ == "__main__":
    st.title("Interface de Estudos Clínicos")
    envio_count = contar_envios()
    isEmpyFilter = False
    col1, col2, col3 = st.columns([1, 2, 2])

    estudos_filtrados = estudos_df.copy()
    with col1:
        tipo_tumor = st.selectbox(
            "Tipo de tumor",
            options=list(biomarcadores_dict.keys()),
            placeholder="Escolha uma opção",
            index=None,
        )
        if tipo_tumor:
            estudos_filtrados = filtrar_estudos_tipo_tumor(
                estudos_filtrados, tipo_tumor
            )

        estadiamentos_restantes = set(
            estudos_filtrados["Tipo_stages"]
            .apply(converter_lista_string_para_lista)
            .sum()
        )
        estadiamento = None
        if len(estadiamentos_restantes) > 0:
            estadiamento = st.selectbox(
                "Estadiamento",
                options=list(equivalencia_estadiamento.keys()),
                placeholder="Escolha uma opção",
                index=None,
            )
            if estadiamento:
                estudos_filtrados = filtrar_estudos_estadiamento(
                    estudos_filtrados, estadiamento
                )

        valor_ecog = st.text_input(
            "Escala ECOG:", placeholder="Informe um valor da escala"
        )
        if valor_ecog:
            estudos_filtrados = filtrar_por_ecog(estudos_filtrados, valor_ecog)

        biomarcadores_restantes = {}
        if tipo_tumor:
            if biomarcadores_dict.get(tipo_tumor):
                biomarcadores_restantes = exibir_biomarcadores_e_opcoes(tipo_tumor)
            else:
                st.warning("Nenhum biomarcador disponível para seleção.")

        # Aplicar o filtro de biomarcadores com a coluna 'biomarcador_match'
        estudos_filtrados = filtrar_estudos_por_biomarcadores(
            estudos_filtrados, biomarcadores_restantes
        )

    with col2:
        st.header(f"Estudos compatíveis ({len(estudos_filtrados.index)}):")
        if not estudos_filtrados.empty:
            isEmpyFilter = True
            # Ordenar estudos para que os correspondentes apareçam primeiro
            estudos_filtrados = estudos_filtrados.sort_values(
                by="biomarcador_match", ascending=False
            )

            # Gerar a tabela HTML manualmente
            table_html = "<table>"
            # Adicionar cabeçalhos
            table_html += "<tr><th>NCT ID</th><th>Título</th></tr>"
            for idx, row in estudos_filtrados.iterrows():
                study_link = f"<a href='https://clinicaltrials.gov/study/{row['nctId']}' target='_blank'>{row['nctId']}</a>"
                title = row["briefTitle"]
                if not row["biomarcador_match"]:
                    # Estudo negativo, destacar em vermelho
                    table_html += f"<tr style='color:red;'><td>{study_link}</td><td>{title}</td></tr>"
                else:
                    table_html += f"<tr><td>{study_link}</td><td>{title}</td></tr>"
            table_html += "</table>"

            # Exibir a tabela
            st.markdown(
                f"<div class='scrollable-table'>" f"{table_html}" f"</div>",
                unsafe_allow_html=True,
            )

            # Filtrar apenas os estudos positivos para exibir os critérios
            estudos_positivos = estudos_filtrados[
                estudos_filtrados["biomarcador_match"]
            ]
    with col3:
        if isEmpyFilter:
            st.header("Critérios de Inclusão/Exclusão")
            # Iterar apenas sobre os estudos positivos
            table_inclusion_exclusion = "<table>"
            for idx, row in estudos_positivos.iterrows():
                criteria = row["eligibilityCriteria"]
                study_link = f"https://clinicaltrials.gov/study/{row['nctId']}\n"
                table_inclusion_exclusion += f'\
                    <tr>\
                        <td style="padding:10px; border-bottom:1px solid #ddd;">\
                            <a href="{study_link}" target="_blank">{row["nctId"]}</a>\
                            <p>{criteria}</p>\
                        </td>\
                    </tr>\
                '
                # st.markdown(f"{study_link}\n{criteria}", unsafe_allow_html=True)
            table_inclusion_exclusion += "</table>"
            st.markdown(
                f"<div class='scrollable-table'>"
                f"{table_inclusion_exclusion}"
                f"</div>",
                unsafe_allow_html=True,
            )
        else:
            st.warning("Nenhum estudo encontrado com os critérios selecionados.")

    st.header("Submissão de Dados")
    carteirinha = st.text_input("Carteirinha:")
    medico = st.text_input("Médico:")
    enviar = st.button("Enviar")

    if enviar:
        filtros = {
            "tipo_tumor": tipo_tumor,
            "estadiamento": estadiamento,
            "valor_ecog": valor_ecog,
            "biomarcadores": biomarcadores_restantes,
        }
        ids_estudos = estudos_filtrados["nctId"].tolist()
        logger.info(f"Email foi enviado")
        logger.info(f"Tipo de tumor {tipo_tumor}")
        logger.info(f"Carteirinha:{carteirinha} Medico:{medico}")
        mailto_link = gerar_link_email(filtros, carteirinha, ids_estudos)
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

        if mailto_link:
            st.success("Email enviado com sucesso!")
        else:
            st.error("Falha ao enviar o email.")

        # Atualizar a contagem de envios após o envio
        envio_count += 1
        st.write(f"Emails enviados: {envio_count}")
# streamlit_analytics.stop_tracking()
