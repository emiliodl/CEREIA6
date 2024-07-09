import streamlit as st
import pandas as pd
import ast

# Função para aplicar CSS personalizado
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregue o CSS personalizado
local_css("style.css")

# Carregar o dataset dos estudos clínicos
file_path = 'df_final_matches_tipo_cancer.csv'  # Substitua pelo caminho do seu arquivo
estudos_df = pd.read_csv(file_path)

# Exibir os primeiros registros do DataFrame para verificar a estrutura
#st.write("Primeiros registros do DataFrame:", estudos_df.head())

# Equivalência entre algarismos romanos e os valores no dataset
equivalencia_estadiamento = {
    'I': 'I',
    'II': 'II',
    'III': 'III'
}

biomarcadores_dict = {
    'Câncer de Pulmão': ['BRAF', 'EGFR', 'ALK', 'ROS1', 'PD-L1', 'KRAS'],
    'Câncer de mama': ['HER', 'Estrogen', 'Progesterone', 'Ki-67', 'ALK', 'BRCA1', 'BRCA2'],
    'Câncer de trato biliar': ['X'],
    'Câncer': ['Ki-67', 'MSI', 'BRAF', 'EGFR', 'ALK', 'ROS1', 'HER', 'PD-L1'],
    'Carcinoma': ['MSI', 'BRAF', 'EGFR', 'ALK', 'ROS1'],
    'Leucemia': ['X'],
    'Metástase': ['X'],
    'Doença de kahler': ['PD-L1'],
    'Câncer anal': ['X'],
    'Câncer de bexiga': ['PD-L1'],
    'Carcinoma de Pulmão de Células Não Pequenas': ['BRAF', 'EGFR', 'ALK', 'ROS1', 'PD-L1', 'KRAS'],
    'Outro': ['MSI', 'PD-L1'],
    'Câncer de colo de útero': ['ALK', 'PD-L1'],
    'Adenocarcinoma': ['PD-L1'],
    'Câncer de Cabeça e Pescoço': ['EGFR'],
    'Câncer de células de Merkel': ['PD-L1'],
    'Pré-leucemia': ['X'],
    'Câncer de Endométrio': ['X'],
    'Câncer de Esôfago': ['PD-L1'],
    'Câncer colorretal': ['MSI', 'HER'],
    'Sarcoma': ['X'],
    'Miastenia grave': ['X'],
    'Mesotelioma': ['X'],
    'Carcinoma de células escamosas do esôfago': ['BRAF', 'ALK', 'EGFR', 'ROS1', 'PD-L1'],
    'Carcinoma de Células escamosas de cabeça e pescoço': ['MSI', 'BRAF', 'EGFR', 'PD-L1'],
    'Câncer de rim': ['X'],
    'Glioblastoma': ['BRAF'],
    'Câncer do reto': ['X'],
    'Tumores estromais gastrointestinais': ['X'],
    'Cancêr de tireóide': ['BRAF', 'EGFR'],
    'Melanoma': ['BRAF', 'ALK', 'PD-L1'],
    'Colangiocarnoma': ['x'],
    'Hemangioma': ['x'],
    'Sarcoma de Kaposi': ['x'],
    'Osteossarcoma': ['x'],
    'Nódulo da tireóide': ['x'],
    'Câncer de cólon': ['x'],
}

opcoes_biomarcadores = {
    'Her 2': ['Positivo', 'Negativo', 'Neutro'],
    'Progesterone': ['Positivo', 'Negativo'],
    'Estrogen': ['Positivo', 'Negativo'],
    'KRAS': ['Mutado', 'Não mutado'],
    'PD-L1': ['Positivo', 'Negativo'],
    'MSI': ['Alto', 'Baixo'],
    'ALK': ['Mutado', 'Não mutado'],
    'BRCA1': ['Mutado', 'Não mutado'],
    'BRCA2': ['Mutado', 'Não mutado'],
    'BRAF': ['Mutado', 'Não mutado'],
    'ROS1': ['Mutado', 'Não mutado'],
    'NRAS': ['Mutado', 'Não mutado'],
    'Ki-67': ['Mutado', 'Não mutado'],
    'EGFR': ['Mutado', 'Não mutado'],
}

biomarcadores_numericos = {
    'Ki-67': 'Valor numérico',
}

# Função para exibir opções de biomarcadores
def exibir_biomarcadores(tipo_tumor):
    biomarcadores = biomarcadores_dict.get(tipo_tumor, [])
    resultados = {}
    for biomarcador in biomarcadores:
        if biomarcador in biomarcadores_numericos:
            resultado = st.number_input(
                f"{biomarcador}: {biomarcadores_numericos[biomarcador]}", format="%f")
        else:
            opcoes = opcoes_biomarcadores.get(
                biomarcador, ['Positivo', 'Negativo', 'Inconclusivo'])
            resultado = st.selectbox(f"{biomarcador}:", options=opcoes)
        resultados[biomarcador] = resultado
    return resultados

# Função para filtrar os estudos clínicos com base no tipo de câncer
def filtrar_estudos_tipo_tumor(df, tipo_tumor):
    if tipo_tumor:
        # Debug: Exibir os tipos de câncer disponíveis no DataFrame
        #st.write("Tipos de câncer disponíveis no DataFrame:", df['Tipo_cancer'].unique())
        return df[df['Tipo_cancer'] == tipo_tumor]
    else:
        return df

# Função para converter strings de listas em listas reais
def converter_lista_string_para_lista(string_lista):
    try:
        return ast.literal_eval(string_lista)
    except (ValueError, SyntaxError):
        return []

# Função para filtrar os estudos clínicos com base no estadiamento
def filtrar_estudos_estadiamento(df, estadiamento):
    if estadiamento:
        estadiamento_valor = equivalencia_estadiamento.get(estadiamento, '')
        df['Tipo_stages_lista'] = df['Tipo_stages'].apply(converter_lista_string_para_lista)
        # Verificar o bug
        #st.write("Tipos de câncer disponíveis no DataFrame:",df['Tipo_stages_lista'].head())
        return df[df['Tipo_stages_lista'].apply(lambda x: estadiamento_valor in x)]
    else:
        return df

# Layout da página
st.title("Interface de Estudos Clínicos")

col1, col2 = st.columns([1, 2])  # Ajusta as proporções das colunas

with col1:
    tipo_tumor = st.selectbox(
        "Tipo de Tumor:", options=[None] + list(biomarcadores_dict.keys()), format_func=lambda x: '' if x is None else x)
    estadiamento = st.selectbox("Estadiamento:", options=[None, 'I', 'II', 'III'], format_func=lambda x: '' if x is None else x)
    if tipo_tumor:
        # Exibir biomarcadores com base no tipo de tumor selecionado
        biomarcadores_resultados = exibir_biomarcadores(tipo_tumor)

with col2:
    # Filtrar estudos com base no tipo de tumor e estadiamento selecionado
    estudos_filtrados = filtrar_estudos_tipo_tumor(estudos_df, tipo_tumor)
    estudos_filtrados = filtrar_estudos_estadiamento(estudos_filtrados, estadiamento)
    st.header("Estudos:")
    st.dataframe(estudos_filtrados[['nctId','briefTitle','conditions','studyType','phases','interventions','eligibilityCriteria','ECOG_score','KPS_scores','metastasis','Estagio_final','Estagio_Inicial','Extensao_tumor_locally_advanced','Extensao_tumor_unresectable','Extensao_tumor_metastatic','Extensao_tumor_Lesions','Extensao_tumor_metastases','Câncer de Mama Triplo Negativo']], height=400)  # Ajusta a altura da tabela
    st.header("Critérios de Inclusão/Exclusão")
    st.text_area("Critérios de inclusão e exclusão:", height=150)
# Parte inferior para a submissão de dados
st.header("Submissão de Dados")
carteirinha = st.text_input("Carteirinha:")
medico = st.text_input("Médico:")
enviar = st.button("Enviar")

if enviar:
    st.success("Informações enviadas com sucesso!")
    if tipo_tumor:
        st.write("Resultados dos Biomarcadores:", biomarcadores_resultados)

