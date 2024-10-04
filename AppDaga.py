import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# Configurar la página de la aplicación
st.set_page_config(page_title="Recolección de Datos Diarios", page_icon="📊", layout="centered")

# Conectar a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer los datos existentes de Google Sheets
existing_data = conn.read(worksheet="dadesdaga", usecols=list(range(6)))
existing_data = existing_data.dropna(how="all")

# Función para cargar el archivo de unidades
@st.cache_data
def load_unitats():
    return pd.read_excel("unitats.xlsx")

# Cargar los datos de unidades
unitats_df = load_unitats()

# Extraer las opciones únicas de las columnas
regio_options = unitats_df["regio"].dropna().unique()
area_options = unitats_df["area"].dropna().unique()
unitat_options = unitats_df["unitat"].dropna().unique()

# Inicializar el estado de la sesión
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
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.regio = st.selectbox("Regió:", regio_options, index=0)
        st.session_state.area = st.selectbox("Àrea:", area_options, index=0)
        st.session_state.unitat = st.selectbox("Unitat:", unitat_options, index=0)

    with col2:
        st.session_state.num_armes = st.number_input("Nombre d'armes blanques:", min_value=0, value=st.session_state.num_armes)
        st.session_state.num_det = st.number_input("Detinguts relacionats:", min_value=0, value=st.session_state.num_det)
        st.session_state.dia = st.date_input("Dia:", value=st.session_state.dia)

    submitted = st.form_submit_button("Enviar datos")

    if submitted:
        # Crear un nuevo dato
        nuevo_dato = pd.DataFrame([{"dia":st.session_state.dia.strftime("%Y-%m-%d"), 
                                    "regio":st.session_state.regio, 
                                    "area":st.session_state.area, 
                                    "unitat":st.session_state.unitat, 
                                    "num_armes":st.session_state.num_armes, 
                                    "num_det":st.session_state.num_det}])
        

        updated_df = pd.concat([existing_data, nuevo_dato], ignore_index=True)

        conn.update(worksheet="dadesdaga", data=updated_df)
        st.cache_data.clear()
        st.rerun()
        
        # Limpiar el estado de la sesión
        for key in st.session_state.keys():
            del st.session_state[key]

        st.success("Dades enviades, gràcies company. Sobretot no repeteixis l'operació per no duplicar. Fins demà.")
