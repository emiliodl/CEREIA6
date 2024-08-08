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
file_path = 'df_final_matches_tipo_cancer_atualizado.csv'  # Substitua pelo caminho do seu arquivo
estudos_df = pd.read_csv(file_path)

# Equivalência entre algarismos romanos e os valores no dataset
equivalencia_estadiamento = {
    'I': 'I',
    'II': 'II',
    'III': 'III'
}

# Dicionários de dados
# Dicionários de dados
biomarcadores_dict = {
    'Lung Neoplasms': ['BRAF', 'EGFR', 'ALK', 'ROS1', 'PD-L1', 'KRAS'],
    'Breast Neoplasms': ['HER', 'Estrogen', 'Progesterone', 'Ki-67', 'ALK', 'BRCA1', 'BRCA2'],
    'Biliary Tract Neoplasms': ['X'],
    'Neoplasms': ['Ki-67', 'MSI', 'BRAF', 'EGFR', 'ALK', 'ROS1', 'HER', 'PD-L1'],
    'Carcinoma': ['MSI', 'BRAF', 'EGFR', 'ALK', 'ROS1'],
    'Leukemia': ['X'],
    'Neoplasm Metastasis': ['X'],
    'Multiple Myeloma': ['PD-L1'],
    'Anus Neoplasms': ['X'],
    'Urinary Bladder Neoplasms': ['PD-L1'],
    'Carcinoma, Non-Small-Cell Lung': ['BRAF', 'EGFR', 'ALK', 'ROS1', 'PD-L1', 'KRAS'],
    'Other': ['MSI', 'PD-L1'],
    'Uterine Cervical Neoplasms': ['ALK', 'PD-L1'],
    'Adenocarcinoma': ['PD-L1'],
    'Head and Neck Neoplasms': ['EGFR'],
    'Carcinoma, Merkel Cell': ['PD-L1'],
    'Preleukemia': ['X'],
    'Endometrial Neoplasms': ['X'],
    'Esophageal Neoplasms': ['PD-L1'],
    'Colorectal Neoplasms': ['MSI', 'HER'],
    'Sarcoma': ['X'],
    'Myasthenia Gravis': ['X'],
    'Mesothelioma': ['X'],
    'Esophageal Squamous Cell Carcinoma': ['BRAF', 'ALK', 'EGFR', 'ROS1', 'PD-L1'],
    'Squamous Cell Carcinoma of Head and Neck': ['MSI', 'BRAF', 'EGFR', 'PD-L1'],
    'Kidney Neoplasms': ['X'],
    'Glioblastoma': ['BRAF'],
    'Rectal Neoplasms': ['X'],
    'Gastrointestinal Stromal Tumors': ['X'],
    'Thyroid Neoplasms': ['BRAF', 'EGFR'],
    'Melanoma': ['BRAF', 'ALK', 'PD-L1'],
    'Cholangiocarcinoma': ['X'],
    'Hemangioma': ['X'],
    'Sarcoma, Kaposi': ['X'],
    'Osteosarcoma': ['X'],
    'Thyroid Nodule': ['X'],
    'Colonic Neoplasms': ['X']
}

mesh_dict = {'Lung Neoplasms': ['Carcinoma, Non-Small-Cell Lung'],
             'Biliary Tract Neoplasms': [],
             'Esophageal Neoplasms': ['Esophageal Squamous Cell Carcinoma'], 
             'Lymphoma': ['Lymphoma, Non-Hodgkin', 'Lymphoma, B-Cell'], 
             'Neoplasms': [], 
             'Breast Neoplasms': [], 
             'Carcinoma': ['Carcinoma, Squamous Cell', 'Squamous Cell Carcinoma of Head and Neck'], 
             'Anxiety Disorders': [], 
             'Primary Ovarian Insufficiency': ['Menopause, Premature'], 
             'Neoplasm Metastasis': ['Sarcoma'], 
             'Leukemia': ['Leukemia, Lymphoid', 'Leukemia, Lymphocytic, Chronic, B-Cell'], 
             'Carcinoma, Squamous Cell': ['Squamous Cell Carcinoma of Head and Neck', 'Head and Neck Neoplasms'], 
             'Multiple Myeloma': ['Neoplasms, Plasma Cell'], 
             'Carcinoma, Non-Small-Cell Lung': [], 
             'Melanoma': [],
             'Uterine Cervical Neoplasms': [], 
             'Urinary Bladder Neoplasms': ['Non-Muscle Invasive Bladder Neoplasms'], 
             'Prostatic Neoplasms': ['Hypersensitivity'], 
             'Sarcoma, Kaposi': ['Sarcoma'], 
             'Adenocarcinoma': ['Stomach Neoplasms'], 
             'Head and Neck Neoplasms': [], 
             'Carcinoma, Merkel Cell': ['Carcinoma'], 
             'Preleukemia': ['Anemia', 'Myelodysplastic Syndromes', 'Syndrome'], 
             'Endometrial Neoplasms': [], 
             'Cholangiocarcinoma': [], 
             'Thromboembolism': ['Venous Thromboembolism'], 
             'Polycythemia Vera': ['Primary Myelofibrosis', 'Polycythemia', 'Thrombocytosis', 'Thrombocythemia, Essential'], 
             'Colorectal Neoplasms': [], 
             'Papillomavirus Infections': ['Uterine Cervical Neoplasms'], 
             'Mucositis': ['Xerostomia'], 
             'Sarcoma': [], 
             'Infections': ['Communicable Diseases', 'Papillomavirus Infections', 'Squamous Cell Carcinoma of Head and Neck'], 
             'Hematologic Neoplasms': ['Graft vs Host Disease'], 
             'Osteosarcoma': ['Mucositis', 'Stomatitis'], 
             'Virus Diseases': ['Neoplasms', 'Hematologic Neoplasms', 'Graft vs Host Disease'], 
             'Stomach Neoplasms': [], 
             'Glioblastoma': [], 
             'Thyroid Diseases': [], 
             'Thyroid Nodule': ['Thyroid Diseases'], 
             'Myasthenia Gravis': ['Muscle Weakness'], 
             'Epstein-Barr Virus Infections': ['Lymphoma', 'Lymphoproliferative Disorders'], 
             'Mouth Neoplasms': ['Head and Neck Neoplasms', 'Mucositis', 'Stomatitis'], 
             'Cardiovascular Diseases': ['Cardiotoxicity'], 
             'Mesothelioma': ['Mesothelioma, Malignant'], 
             'Epilepsy': [], 
             'Esophageal Squamous Cell Carcinoma': [], 
             'Anus Neoplasms': [], 
             'Cardiotoxicity': [], 
             'Colonic Neoplasms': ['Thrombosis', 'Venous Thrombosis'], 
             'Thyroid Neoplasms': ['Thyroid Diseases'], 
             'Postoperative Complications': ['Postoperative Nausea and Vomiting'], 
             'Kidney Neoplasms': ['Carcinoma, Renal Cell'], 
             'Ventricular Dysfunction': ['Ventricular Dysfunction, Left'], 
             'Primary Myelofibrosis': [], 
             'Hemangioma': ['Arteriovenous Malformations', 'Congenital Abnormalities'], 
             'Cancer Pain': [], 
             'Squamous Cell Carcinoma of Head and Neck': [], 
             'Rectal Neoplasms': [], 
             'Gastrointestinal Stromal Tumors': []}


opcoes_biomarcadores = {
    'HER': ['Positivo', 'Negativo', 'Neutro'],
    'Estrogen': ['Positivo', 'Negativo'],
    'Progesterone': ['Positivo', 'Negativo'],
    'KRAS': ['Mutado', 'Não mutado'],
    'PD-L1': ['Positivo', 'Negativo'],
    'MSI': ['Alto', 'Baixo'],
    'ALK': ['Mutado', 'Não mutado'],
    'BRCA1': ['Mutado', 'Não mutado'],
    'BRCA2': ['Mutado', 'Não mutado'],
    'BRAF': ['Mutado', 'Não mutado'],
    'ROS1': ['Mutado', 'Não mutado'],

}

stages_list = [
    ' ', 'I', 'IA', 'IB', 'IC', 'II', 'IIA', 'IIB', 'IIC', 'III', 'IIIA', 'IIIB', 'IIIC', 'IV', 'IVA', 'IVB', 'IVC',
    'Tx', 'T0', 'Ta', 'Tis', 'Tis(DCIS)', 'Tis(LAMN)', 'Tis(Paget)', 'T1', 'T1mi', 'T1a', 'T1a1', 'T1a2', 'T1b', 'T1b1', 'T1b2', 'T1b3', 'T1c', 'T1c1', 'T1c2', 'T1c3', 'T1d',
    'T2', 'T2a', 'T2a1', 'T2a2', 'T2b', 'T2c', 'T2d', 'T3', 'T3a', 'T3b', 'T3c', 'T3d', 'T3e', 'T4', 'T4a', 'T4b', 'T4c', 'T4d', 'T4e',
    'Nx', 'N0', 'N0(sn)', 'N0a', 'N0a(sn)', 'N0b', 'N0b(sn)', 'N0(i+)', 'N0(mol+)', 'N1', 'N1(sn)', 'N1mi', 'N1mi(sn)', 'N1a', 'N1a(sn)', 'N1b', 'N1b(sn)', 'N1c', 'N1c(sn)',
    'N2', 'N2mi', 'N2a', 'N2b', 'N2c', 'N3', 'N3a', 'N3b', 'N3c', 'Mx', 'M0', 'M0(i+)', 'M1', 'M1a', 'M1a(0)', 'M1a(1)', 'M1b', 'M1b(0)', 'M1b(1)', 'M1c', 'M1c(0)', 'M1c(1)', 'M1d', 'M1d(0)', 'M1d(1)',
    'ypT2-4a', 'ypN+', 'pT2-4a', 'pN+'
]

# Funções de filtragem
def filtrar_estudos_tipo_tumor(df, tipo_tumor, termo_2=None):
    colunas_esperadas = ['term_1', 'term_2', 'term_3', 'term_4', 'term_5']
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            raise KeyError(f"A coluna '{coluna}' não existe no DataFrame.")
    
    if tipo_tumor:
        mask = (df['term_1'].str.strip().eq(tipo_tumor) | 
                df['term_2'].str.strip().eq(tipo_tumor) |
                df['term_3'].str.strip().eq(tipo_tumor) |
                df['term_4'].str.strip().eq(tipo_tumor) |
                df['term_5'].str.strip().eq(tipo_tumor))
        if termo_2:
            mask &= (df['term_1'].str.strip().eq(termo_2) | 
                     df['term_2'].str.strip().eq(termo_2) |
                     df['term_3'].str.strip().eq(termo_2) |
                     df['term_4'].str.strip().eq(termo_2) |
                     df['term_5'].str.strip().eq(termo_2))
        filtered_df = df[mask]
        if filtered_df.empty:
            st.warning("Nenhum registro encontrado para o tipo de câncer e termo selecionados.")
        return filtered_df
    else:
        return df

def converter_lista_string_para_lista(string_lista):
    try:
        return ast.literal_eval(string_lista)
    except (ValueError, SyntaxError):
        return []

# Função para filtrar os estudos clínicos com base no estadiamento
def filtrar_estudos_estadiamento(df, estadiamento):
    if estadiamento:
        estadiamento_valor = equivalencia_estadiamento.get(estadiamento, '')
        if not estadiamento_valor:
            print(f"Estadiamento '{estadiamento}' não encontrado no dicionário de equivalência.")
            return df

        df['Tipo_stages_lista'] = df['Tipo_stages'].apply(converter_lista_string_para_lista)

        filtrado = df[df['Tipo_stages_lista'].apply(lambda x: estadiamento_valor in x)]
        return filtrado
    else:
        return df

def filtrar_por_ecog(df, valor_ecog):
    if valor_ecog:
        if 'Tem ECOG' not in df.columns:
            raise KeyError("A coluna 'Tem ECOG' não existe no DataFrame.")
        
        df['ECOG_score'] = df['ECOG_score'].str.strip()
        df_filtrado = df[df['ECOG_score'].str.contains(valor_ecog, case=False, na=False)]
        
        if df_filtrado.empty:
            st.warning("Nenhum registro encontrado para o valor do ECOG selecionado.")
        
        return df_filtrado
    else:
        return df

# Função para exibir biomarcadores com base no tipo de tumor
def exibir_biomarcadores_e_opcoes(tipo_tumor):
    biomarcadores = biomarcadores_dict.get(tipo_tumor, [])
    selecoes = {}
    for biomarcador in biomarcadores:
        opcoes = opcoes_biomarcadores.get(biomarcador, [])
        selecoes[biomarcador] = st.selectbox(f'Selecione a opção para {biomarcador}', options=opcoes)
    return selecoes

st.title("Interface de Estudos Clínicos")

col1, col2 = st.columns([1, 2])

with col1:
    tipo_tumor = st.selectbox("Selecione o tipo de tumor", options=list(biomarcadores_dict.keys()))
    estadiamento = st.selectbox("Selecione o estadiamento", options=stages_list)
    valor_ecog = st.text_input('Selecione o ECOG:')
    
    if tipo_tumor:
        biomarcadores_resultados = exibir_biomarcadores_e_opcoes(tipo_tumor)

with col2:
    estudos_filtrados = filtrar_estudos_tipo_tumor(estudos_df, tipo_tumor)
    estudos_filtrados = filtrar_estudos_estadiamento(estudos_filtrados, estadiamento)
    estudos_filtrados = filtrar_por_ecog(estudos_filtrados, valor_ecog)
    
    # Gerar links clicáveis para o clinicaltrials.gov
    estudos_filtrados['nctId'] = estudos_filtrados['nctId'].apply(lambda x: f"<a href='https://clinicaltrials.gov/study/{x}' target='_blank'>{x}</a>")
    
    st.header("Estudos:")
    print('>verificando:', estudos_filtrados, estudos_filtrados.columns)

    if 'nctId' in estudos_filtrados.columns and 'briefTitle' in estudos_filtrados.columns:
        # Criar uma tabela HTML
        tabela_html = estudos_filtrados[['nctId', 'briefTitle']].to_html(escape=False, index=False)
        st.markdown(tabela_html, unsafe_allow_html=True)

    st.header("Critérios de Inclusão/Exclusão")
    st.markdown("""
                <style>
                div[data-testid="stTextArea"] textarea {
                background-color: #add8e6;
                color: black;
                }
                </style>
                """, unsafe_allow_html=True)
    
    criteria_text = "\n".join(estudos_filtrados['eligibilityCriteria'])
    st.text_area("Critérios de inclusão e exclusão:", value=criteria_text, height=150, disabled=True)

# Parte inferior para a submissão de dados
st.header("Submissão de Dados")
carteirinha = st.text_input("Carteirinha:")
medico = st.text_input("Médico:")
enviar = st.button("Enviar")

if enviar:
    st.success("Informações enviadas com sucesso!")
    if tipo_tumor:
        st.write("Resultados dos Biomarcadores:", biomarcadores_resultados)
