import streamlit as st

# Função para aplicar CSS personalizado
def local_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Carregue o CSS personalizado
local_css("style.css")

# Layout da página
st.title("Interface de Estudos Clínicos")

col1, col2 = st.columns([1, 2])  # Ajusta as proporções das colunas

with col1:
    tipo_tumor = st.text_input("Tipo de Tumor:")
    estadiamento = st.text_input("Estadiamento:")
    ecog = st.text_input("ECOG:")
    biomarcador_a = st.text_input("Biomarcador A:")
    biomarcador_b = st.text_input("Biomarcador B:")
    biomarcador_c = st.text_input("Biomarcador C:")

with col2:
    st.header("Estudos:")
    st.text_area("Estudo compatíveis", height=150)
    st.header("Critérios de Inclusão/Exclusão")
    st.text_area("Critérios de inclusão e exclusão:", height=150)

# Parte inferior para a submissão de dados
st.header("Submissão de Dados")
carteirinha = st.text_input("Carteirinha:")
medico = st.text_input("Médico:")
enviar = st.button("Enviar")

if enviar:
    st.success("Informações enviadas com sucesso!")

