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

    # ------------------------------
    # FILTRO BASE
    # ------------------------------

    df = df[
        (df["Término"] >= FECHA_INICIO)
        &
        (df["Inicio"] <= FECHA_FIN)
    ].copy()

    # ------------------------------
    # INDICADORES
    # ------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Equipos",
        df["Equipo"].nunique()
    )

    c2.metric(
        "Pozos",
        df["Pozo"].nunique()
    )

    c3.metric(
        "Intervenciones",
        len(df)
    )

    c4.metric(
        "Campos",
        df["Campo"].nunique()
    )

    # ------------------------------
    # TABLA
    # ------------------------------

    st.subheader(
    "Archivo procesado correctamente"
    )

    st.write(
        f"Registros cargados: {len(df)}"
    )
