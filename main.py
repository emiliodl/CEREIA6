import streamlit as st
import pandas as pd
import ast
from dicionarios import equivalencia_estadiamento, bio_to_column, biomarcadores_dict, opcoes_biomarcadores, mesh_dict

def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

file_path = 'df_final_matches_tipo_cancer_atualizado.csv'  
estudos_df = pd.read_csv(file_path)

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
    mask = pd.Series([True] * len(df), index=df.index)  # Alinhar o índice do mask com o índice do DataFrame
    
    for biomarcador, valor in selecoes_biomarcadores.items():
        if valor:  # Aplica o filtro apenas se o valor não estiver vazio
            coluna = bio_to_column.get(biomarcador)
            if coluna:
                # Verifique se a coluna contém valores nulos e trate-os
                if coluna in df.columns:
                    df[coluna] = df[coluna].fillna('')
                    mask &= (df[coluna] == valor)
                    print(f"Aplicando filtro: {coluna} == {valor}")

    print(f"Total de registros após filtragem: {mask.sum()} de {len(df)}")
    return df[mask]

def exibir_biomarcadores_e_opcoes(tipo_tumor):
    biomarcadores = biomarcadores_dict.get(tipo_tumor, [])
    selecoes = {}
    for biomarcador in biomarcadores:
        opcoes = [""] + opcoes_biomarcadores.get(biomarcador, [])  # Adiciona uma opção vazia no início
        selecoes[biomarcador] = st.selectbox(f'Selecione a opção para {biomarcador}', options=opcoes)
    return selecoes

st.title("Interface de Estudos Clínicos")

col1, col2 = st.columns([1, 2])

with col1:
    tipo_tumor = st.selectbox("Selecione o tipo de tumor", options=list(biomarcadores_dict.keys()))
    estadiamento = st.selectbox("Selecione o estadiamento", options=[""] + list(equivalencia_estadiamento.keys()))
    valor_ecog = st.text_input('Selecione o ECOG:')
    
    # Exibe as opções de biomarcadores com base no tipo de tumor selecionado
    if biomarcadores_dict.get(tipo_tumor) != ['X']:
        biomarcadores_resultados = exibir_biomarcadores_e_opcoes(tipo_tumor)
    else:
        st.warning("Nenhum biomarcador disponível para seleção.")
    
with col2:
    # Filtra os estudos na ordem correta
    estudos_filtrados = filtrar_estudos_tipo_tumor(estudos_df, tipo_tumor)
    estudos_filtrados = filtrar_estudos_estadiamento(estudos_filtrados, estadiamento)
    estudos_filtrados = filtrar_por_ecog(estudos_filtrados, valor_ecog)
    estudos_filtrados = filtrar_estudos_por_biomarcadores(estudos_filtrados, biomarcadores_resultados)
    
    # Gerar links clicáveis para o clinicaltrials.gov
    if not estudos_filtrados.empty:
        estudos_filtrados['nctId'] = estudos_filtrados['nctId'].apply(lambda x: f"<a href='https://clinicaltrials.gov/study/{x}' target='_blank'>{x}</a>")
    
        st.header("Estudos:")
        st.markdown(estudos_filtrados[['nctId', 'briefTitle']].to_html(escape=False, index=False), unsafe_allow_html=True)
    
        st.header("Critérios de Inclusão/Exclusão")
        criteria_text = "\n".join(estudos_filtrados['eligibilityCriteria'])
        st.text_area("Critérios de inclusão e exclusão:", value=criteria_text, height=150, disabled=True)
    else:
        st.warning("Nenhum estudo encontrado com os critérios selecionados.")

st.header("Submissão de Dados")
carteirinha = st.text_input("Carteirinha:")
medico = st.text_input("Médico:")
enviar = st.button("Enviar")

if enviar:
    st.success("Informações enviadas com sucesso!")
    if tipo_tumor:
        st.write("Resultados dos Biomarcadores:", biomarcadores_resultados)
