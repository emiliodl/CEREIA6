import streamlit as st

# Define a estrutura de colunas
col1, col2 = st.columns(2)

# Coluna 1 - Inputs do usuário
with col1:
    st.header("Estudos:")
    tipo_tumor = st.text_input("Tipo de Tumor:")
    estadiamento = st.text_input("Estadiamento:")
    ecog = st.text_input("ECOG:")
    biomarcador_a = st.text_input("Biomarcador A:")
    biomarcador_b = st.text_input("Biomarcador B:")
    biomarcador_c = st.text_input("Biomarcador C:")

# Coluna 2 - Critérios de Inclusão/Exclusão
with col2:
    st.header("Critérios de Inclusão/Exclusão:")
    st.write("Insira aqui os critérios específicos. Podem ser em forma de texto, listas ou o que for necessário.")

# Seção para enviar informações
st.header("Informações Adicionais")
carteirinha = st.text_input("Carteirinha:")
medico = st.text_input("Médico:")
enviar = st.button("Enviar")

if enviar:
    st.success("Informações enviadas com sucesso!")
