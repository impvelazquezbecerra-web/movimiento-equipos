# ==========================================
# LIBRERIAS
# ==========================================
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# CONFIGURACION
# ==========================================

FECHA_INICIO = "2026-01-01"
FECHA_FIN = "2029-12-31"

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

# -------------------------
# AÑO
# -------------------------

anio = st.sidebar.selectbox(

    "Año",

    ["TODOS"]

    +

    sorted(
        df["Inicio"]
        .dt.year
        .dropna()
        .unique()
        .tolist()
    )
)

# -------------------------
# CAMPO
# -------------------------

campos_disponibles = [

    "TODOS"

] + sorted(

    df["Campo"]
    .dropna()
    .unique()
    .tolist()

)

campo = st.sidebar.selectbox(
    "Campo",
    campos_disponibles
)

# -------------------------
# EQUIPO
# -------------------------

df_equipo = df.copy()

if campo != "TODOS":

    df_equipo = df_equipo[
        df_equipo["Campo"] == campo
    ]

equipos_disponibles = [

    "TODOS"

] + sorted(

    df_equipo["Equipo"]
    .dropna()
    .unique()
    .tolist()

)

equipo = st.sidebar.selectbox(
    "Equipo",
    equipos_disponibles
)

# -------------------------
# POZO
# -------------------------

df_pozo = df_equipo.copy()

if equipo != "TODOS":

    df_pozo = df_pozo[
        df_pozo["Equipo"] == equipo
    ]

pozos_disponibles = [

    "TODOS"

] + sorted(

    df_pozo["Pozo"]
    .dropna()
    .unique()
    .tolist()

)

pozo = st.sidebar.selectbox(
    "Pozo",
    pozos_disponibles
)

# -------------------------
# MOSTRAR ETIQUETAS
# -------------------------

mostrar_etiquetas = st.sidebar.toggle(
    "Mostrar etiquetas",
    value=True
)

# -------------------------
# APLICAR FILTROS
# -------------------------

df_filtrado = df.copy()

if anio != "TODOS":

    anio_int = int(anio)

    df_filtrado = df_filtrado[

        (
            df_filtrado["Inicio"].dt.year == anio_int
        )

        |

        (
            df_filtrado["Término"].dt.year == anio_int
        )

    ]

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
    def categoria(x):

        x = str(x).upper()

        if "MOV" in x:
            return "MOVIMIENTO"

        elif "PRE" in x:
            return "PREARRANQUE"

        elif "ACOPIO" in x:
            return "ACOPIO"

        elif "DESP" in x:
            return "DESPLAZAMIENTO"

        elif "INSP" in x:
            return "INSPECCIÓN"

        elif "MANT" in x:
            return "MTTO"

        elif "REPARACIÓN MENOR" in x or "RME" in x:
            return "RME"

        elif "REPARACIÓN MAYOR" in x or "RMA" in x:
            return "RMA"

        elif "PERF" in x:
            return "PERFORACIÓN"

        elif "TERM" in x:
            return "TERMINACIÓN"

        elif "FLEX" in x:
            return "FLEX"

        else:
            return "OTROS"


    df_filtrado["Categoría"] = (
        df_filtrado["Intervención"]
        .apply(categoria)
    )

# ------------------------------
# ETIQUETAS
# ------------------------------

    df_filtrado = df_filtrado.sort_values(
        ["Equipo", "Inicio"]
    )

    df_filtrado["Etiqueta"] = (
        df_filtrado["Pozo"]
    )

# ------------------------------
# ETIQUETAS
# ------------------------------

    colores = {

        "RME":"#92D050",

        "RMA":"#4472C4",

        "PERFORACIÓN":"#006100",

        "TERMINACIÓN":"#FFD966",

        "MOVIMIENTO":"#5B9BD5",

        "MTTO":"#8B5A2B",

        "INSPECCIÓN":"#ED7D31",

        "DESPLAZAMIENTO":"#BFBFBF",

        "ACOPIO":"#FFF2CC",

        "PREARRANQUE":"#D9D9D9",

        "FLEX":"#FFFFFF",

        "OTROS":"#C9C9C9"
    }

  
# ------------------------------
# GRAFICO
# ------------------------------

    fig = px.timeline(

        df_filtrado,

        x_start="Inicio",

        x_end="Término",

        y="Equipo",

        color="Categoría",

        text=(
            "Etiqueta"
            if mostrar_etiquetas
            else None
        ),

        hover_name="Pozo",

        hover_data={
            "Inicio":"|%d/%m/%Y",
            "Término":"|%d/%m/%Y",
            "Campo":True,
            "Intervención":True,
            "Días":True,
            "Beneficio":True,
            "Beneficio Gas":True
        },

        color_discrete_map=colores
    )

    fig.update_yaxes(
    autorange="reversed"
    )

    fig.update_traces(
        textfont_size=10,
        textposition="inside"
    )

    fig.update_xaxes(

        tickformat="%b-%Y",

        dtick="M1",

        range=[
            FECHA_INICIO,
            FECHA_FIN
        ]

    )

    if anio == "TODOS":

        fig.update_xaxes(

            range=[
                FECHA_INICIO,
                FECHA_FIN
            ]

        )

    else:

        fig.update_xaxes(

            range=[
                f"{anio}-01-01",
                f"{anio}-12-31"
            ]

        )

    fig.update_layout(
        height=1200
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
