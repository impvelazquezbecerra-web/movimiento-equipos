import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURACION
# ==========================================

FECHA_INICIO = "2026-01-01"
FECHA_FIN = "2030-12-31"

st.set_page_config(
    page_title="Movimiento de Equipos V6",
    layout="wide"
)

# ==========================================
# TITULO
# ==========================================

st.title("Movimiento de Equipos V6")

# ==========================================
# CARGA DE ARCHIVO
# ==========================================

archivo = st.file_uploader(
    "Seleccione archivo Excel",
    type=["xlsx"]
)

# ==========================================
# PROCESAMIENTO
# ==========================================

if archivo is not None:

    df = pd.read_excel(
        archivo,
        engine="openpyxl"
    )

    df.columns = df.columns.str.strip()

    # ------------------------------
    # VALIDACION
    # ------------------------------

    columnas_requeridas = [
        "Equipo",
        "Pozo",
        "Campo",
        "Intervención",
        "Inicio",
        "Término"
    ]

    faltantes = [
        col
        for col in columnas_requeridas
        if col not in df.columns
    ]

    if faltantes:

        st.error(
            f"Faltan columnas: {faltantes}"
        )

        st.stop()

    # ------------------------------
    # FECHAS
    # ------------------------------

    df["Inicio"] = pd.to_datetime(
        df["Inicio"],
        dayfirst=True
    )

    df["Término"] = pd.to_datetime(
        df["Término"],
        dayfirst=True
    )

    # =====================================
    # FILTROS
    # =====================================

    st.sidebar.header("Filtros")

    campo = st.sidebar.selectbox(

        "Campo",

        ["TODOS"] +

        sorted(
            df["Campo"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    equipo = st.sidebar.selectbox(

        "Equipo",

        ["TODOS"] +

        sorted(
            df["Equipo"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    pozo = st.sidebar.selectbox(

        "Pozo",

        ["TODOS"] +

        sorted(
            df["Pozo"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    df_filtrado = df.copy()

    if campo != "TODOS":

        df_filtrado = df_filtrado[
            df_filtrado["Campo"] == campo
        ]

    if equipo != "TODOS":

        df_filtrado = df_filtrado[
            df_filtrado["Equipo"] == equipo
        ]

    if pozo != "TODOS":

        df_filtrado = df_filtrado[
            df_filtrado["Pozo"] == pozo
        ]

    # =====================================
    # DASHBOARD
    # =====================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Equipos",
        df_filtrado["Equipo"].nunique()
    )

    c2.metric(
        "Pozos",
        df_filtrado["Pozo"].nunique()
    )

    c3.metric(
        "Intervenciones",
        len(df_filtrado)
    )

    c4.metric(
        "Campos",
        df_filtrado["Campo"].nunique()
    )

    # ------------------------------
    # TABLA
    # ------------------------------

    st.subheader(
        "Vista previa filtrada"
    )

    st.write(
        f"Registros encontrados: {len(df_filtrado)}"
    )

