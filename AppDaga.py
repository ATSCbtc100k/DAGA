
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configurar la página de la aplicación
st.set_page_config(page_title="Recolección de Datos Diarios", page_icon="📊", layout="centered")

conn = st.connection("gsheets", type=GSheetsConnection)



# Función para cargar el archivo de unidades
def load_unitats():
    # Cargar el archivo Excel 'unitats.xlsx' con las opciones de Regió, Àrea y Unitat
    return pd.read_excel("unitats.xlsx")

# Cargar los datos de unidades
unitats_df = load_unitats()

# Extraer las opciones únicas de las columnas
regio_options = unitats_df["regio"].dropna().unique()
area_options = unitats_df["area"].dropna().unique()
unitat_options = unitats_df["unitat"].dropna().unique()

# Inicializar el estado de la sesión para los campos
if 'regio' not in st.session_state:
    st.session_state.regio = ""
if 'area' not in st.session_state:
    st.session_state.area = ""
if 'unitat' not in st.session_state:
    st.session_state.unitat = ""
if 'num_armes' not in st.session_state:
    st.session_state.num_armes = 0
if 'num_det' not in st.session_state:
    st.session_state.num_det = 0
if 'dia' not in st.session_state:
    st.session_state.dia = datetime.today()

# Título de la aplicación
st.title("Dades diaries plà DAGA")

# Formulario para ingresar datos
with st.form("datos_form"):
    # Crear dos columnas
    col1, col2 = st.columns(2)

    # Primera columna con tres primeros campos (con opciones limitadas)
    with col1:
        st.session_state.regio = st.selectbox("Regió:", regio_options, index=0)
        st.session_state.area = st.selectbox("Àrea:", area_options, index=0)
        st.session_state.unitat = st.selectbox("Unitat:", unitat_options, index=0)

    # Segunda columna con el resto de los campos
    with col2:
        st.session_state.num_armes = st.number_input("Nombre d'armes blanques:", min_value=0, value=st.session_state.num_armes)
        st.session_state.num_det = st.number_input("Detinguts relacionats:", min_value=0, value=st.session_state.num_det)
        st.session_state.dia = st.date_input("Dia:", value=st.session_state.dia)

    # Botón de envío
    submitted = st.form_submit_button("Enviar datos")

    if submitted:
        # Guardar los datos
        nuevo_dato = [st.session_state.dia.strftime("%Y-%m-%d"), st.session_state.regio, st.session_state.area, st.session_state.unitat, st.session_state.num_armes, st.session_state.num_det]

        # Agregar los datos a la hoja de Google Sheets
        
        conn.update(worksheet="dadesdaga", data=nuevo_dato)

        # Limpiar el estado de la sesión después de enviar
        for key in st.session_state.keys():
            del st.session_state[key]

        st.success("Dades enviades, gràcies company. Sobretot no repeteixis l'operació per no duplicar. Fins demà.")
