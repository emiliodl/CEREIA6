import streamlit as st
import pandas as pd
import ast
import urllib.parse
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
        estadiamentos_reverso = {}
        
        for k, v in equivalencia_estadiamento.items():
            for x in v:
                estadiamentos_reverso[x] = k
        
        estadiamentos_equivalentes = equivalencia_estadiamento[estadiamentos_reverso[estadiamento]]
        if not estadiamentos_equivalentes:
            print(f"Estadiamento '{estadiamento}' não encontrado no dicionário de equivalência.")
            return df

        estadiamentos_df = df['Tipo_stages'].apply(converter_lista_string_para_lista)
        filtrado = df[estadiamentos_df.apply(lambda x: any(item in estadiamentos_equivalentes for item in x))]

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
        if biomarcador == 'Ki-67':
            # Caixa de texto para entrada numérica
            selecoes[biomarcador] = st.text_input(f'Insira o valor para {biomarcador} (%)')
        else:
            # Selectbox para opções predefinidas
            opcoes = opcoes_biomarcadores.get(biomarcador, [])
            selecoes[biomarcador] = st.selectbox(f'Selecione a opção para {biomarcador}', options=opcoes, index=None)
    
    return selecoes

def gerar_link_email(filtros, email_destino, carteirinha, ids_estudos):
    assunto = "Resultados dos Filtros de Estudos Clínicos"
    
    # Gera os links simples dos estudos
    links_estudos = [f"https://clinicaltrials.gov/study/{id_estudo}" for id_estudo in ids_estudos]
    links_estudos_str = "\n".join(links_estudos)  # Junta todos os links em uma única string, separados por nova linha
    
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
    corpo_email_encoded = urllib.parse.quote(corpo_email)
    assunto_encoded = urllib.parse.quote(assunto)
    
    # Cria o link mailto
    mailto_link = f"mailto:{email_destino}?subject={assunto_encoded}&body={corpo_email_encoded}"
    
    return mailto_link

if __name__ == '__main__':
    st.title("Interface de Estudos Clínicos")

    col1, col2 = st.columns([1, 2])

    estudos_filtrados = estudos_df.copy()
    with col1:
        tipo_tumor = st.selectbox('Tipo de tumor', options=list(biomarcadores_dict.keys()), placeholder='Escolha uma opção', index=None)
        if tipo_tumor:
            estudos_filtrados = filtrar_estudos_tipo_tumor(estudos_filtrados, tipo_tumor)

        estadiamentos_restantes = set(estudos_filtrados['Tipo_stages'].apply(converter_lista_string_para_lista).sum())
        if len(estadiamentos_restantes) > 0:
            estadiamento = st.selectbox('Estadiamento', options=list(estadiamentos_restantes), placeholder='Escolha uma opção', index=None)
            if estadiamento:
                estudos_filtrados = filtrar_estudos_estadiamento(estudos_filtrados, estadiamento)

        valor_ecog = st.text_input('Escala ECOG:', placeholder='Informe um valor da escala')
        if valor_ecog:
            estudos_filtrados = filtrar_por_ecog(estudos_filtrados, valor_ecog)
        
        biomarcadores_restantes = {}
        if tipo_tumor:
            if biomarcadores_dict.get(tipo_tumor):
                biomarcadores_restantes = exibir_biomarcadores_e_opcoes(tipo_tumor)
            else:
                st.warning("Nenhum biomarcador disponível para seleção.")
        
        estudos_filtrados = filtrar_estudos_por_biomarcadores(estudos_filtrados, biomarcadores_restantes)
    with col2:
        st.header(f'Estudos compatíveis ({len(estudos_filtrados.index)}):')
        if not estudos_filtrados.empty:
            estudos_filtrados['nctId'] = estudos_filtrados['nctId'].apply(lambda x: f"<a href='https://clinicaltrials.gov/study/{x}' target='_blank'>{x}</a>")
            st.markdown(estudos_filtrados[['nctId', 'briefTitle']].to_html(escape=False, index=False), unsafe_allow_html=True)
            st.header("Critérios de Inclusão/Exclusão")
            criteria_text = "\n".join(estudos_filtrados['eligibilityCriteria'])
            st.text_area("Critérios de inclusão e exclusão:", value=criteria_text, height=150, disabled=True)
        else:
            st.warning("Nenhum estudo encontrado com os critérios selecionados.")

    st.header("Submissão de Dados")
    carteirinha = st.text_input("Carteirinha:")
    medico = st.text_input("Médico:")
    email_destino = st.text_input("Email para envio:")
    enviar = st.button("Enviar")

    if enviar:
        filtros = {
            'tipo_tumor': tipo_tumor,
            'estadiamento': estadiamento,
            'valor_ecog': valor_ecog,
            'biomarcadores': biomarcadores_restantes
        }
        ids_estudos = estudos_filtrados['nctId'].tolist()  # Obter a lista de IDs dos estudos filtrados
        mailto_link = gerar_link_email(filtros, email_destino, carteirinha, ids_estudos)
        
        # Usar uma tag <a> diretamente
        st.markdown(f'<a href="{mailto_link}" target="_blank">Clique aqui para enviar o email</a>', unsafe_allow_html=True)
