import streamlit as st
import pandas as pd
import ast
from dicionarios import equivalencia_estadiamento, bio_to_column, biomarcadores_dict, opcoes_biomarcadores, mesh_dict

# Função para aplicar CSS personalizado
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregue o CSS personalizado
local_css("style.css")

# Carregar o dataset dos estudos clínicos
file_path = 'df_final_matches_tipo_cancer_atualizado.csv'  # Substitua pelo caminho do seu arquivo
estudos_df = pd.read_csv(file_path)

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

def filtrar_estudos_estadiamento(df, estadiamento):
    if estadiamento:
        estadiamento_valor = equivalencia_estadiamento.get(estadiamento, [])
        if not estadiamento_valor:
            print(f"Estadiamento '{estadiamento}' não encontrado no dicionário de equivalência.")
            return df

        df['Tipo_stages_lista'] = df['Tipo_stages'].apply(converter_lista_string_para_lista)
        filtrado = df[df['Tipo_stages_lista'].apply(lambda x: any(item in estadiamento_valor for item in x))]

        # Verificar conteúdo do filtrado
        print(f"Total de registros encontrados: {len(filtrado)}")

        if filtrado.empty:
            st.warning("Nenhum registro encontrado para o estadiamento selecionado.")
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

def filtrar_estudos_por_biomarcadores(df, selecoes_biomarcadores):
    mask = pd.Series([True] * len(df))
    
    for biomarcador, valor in selecoes_biomarcadores.items():
        if valor:  # Certifique-se de que o valor não está vazio
            if biomarcador == 'HER':
                mask &= df['Tipo_Her'] == valor
            elif biomarcador == 'Estrogen':
                mask &= df['tipo_estrogen'] == valor
            elif biomarcador == 'Progesterone':
                mask &= df['tipo_progesterone'] == valor
            elif biomarcador == 'KRAS':
                mask &= df['BiomarkKRAS'] == valor
            elif biomarcador == 'PD-L1':
                mask &= df['Tipo_PD_L1'] == valor
            elif biomarcador == 'MSI':
                mask &= df['Tipo_MSI'] == valor
            elif biomarcador == 'ALK':
                mask &= df['Tipo_ALK'] == valor
            elif biomarcador == 'BRCA1':
                mask &= df['Tipo_BRCA1_BRCA2'].str.contains('BRCA1', na=False) & (df['Tipo_BRCA1_BRCA2'] == valor)
            elif biomarcador == 'BRCA2':
                mask &= df['Tipo_BRCA1_BRCA2'].str.contains('BRCA2', na=False) & (df['Tipo_BRCA1_BRCA2'] == valor)
            elif biomarcador == 'BRAF':
                mask &= df['Tipo_BRAF'] == valor
            elif biomarcador == 'ROS1':
                mask &= df['Tipo_ROS1'] == valor
            elif biomarcador == 'Ki-67':
                mask &= df['Tipo_de_resultado_Ki67'] == valor
            elif biomarcador == 'EGFR':
                mask &= df['Tipo_EGFR'] == valor
    
    return df[mask]

# Função para exibir biomarcadores com base no tipo de tumor
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
    estadiamento = st.selectbox("Selecione o estadiamento", options=equivalencia_estadiamento)
    valor_ecog = st.text_input('Selecione o ECOG:')
    if biomarcadores_dict.get(tipo_tumor) != ['X']:
         biomarcadores_resultados = exibir_biomarcadores_e_opcoes(tipo_tumor)
    else:
         st.warning("Nenhum biomarcador disponível para seleção.")
    selecoes = {}

    if selecoes:
        mask = pd.Series([True] * len(estudos_df))
        
        for biomarcador, opcoes_selecionadas in selecoes.items():
            if opcoes_selecionadas:
                biomarcador_mask = (estudos_df['Biomarcador'] == biomarcador) & (estudos_df['Opção'].isin(opcoes_selecionadas))
                mask &= biomarcador_mask
        
        estudo_filtrado = estudos_df[mask]
        st.write("Dados filtrados:")
        st.write(estudo_filtrado)
    else:
        st.write("Nenhum filtro aplicado.")
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