import streamlit as st

st.set_page_config(
    page_title="Movimiento de Equipos",
    layout="wide"
)

st.title("Movimiento de Equipos")

archivo = st.file_uploader(
    "Seleccione archivo Excel",
    type=["xlsx"]
)

if archivo:
    st.success("Archivo cargado correctamente")
