# SOLUCIÓN:
# Streamlit Cloud no soporta pyttsx3, por eso sale ModuleNotFoundError.
# Se reemplaza por JavaScript SpeechSynthesis (funciona en navegador, sin instalar librerías).
# PEGA ESTE CÓDIGO COMPLETO AL INICIO DE TU APP Y SUSTITUYE pyttsx3.

import streamlit as st
from datetime import datetime, timedelta, time
import pandas as pd

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

if "logo" not in st.session_state:
    st.session_state.logo = None

if "voz_activada" not in st.session_state:
    st.session_state.voz_activada = False

if "modo_accesible" not in st.session_state:
    st.session_state.modo_accesible = False


# ================= FUNCIÓN DE VOZ WEB =================
def hablar(texto):
    st.markdown(
        f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texto}");
        msg.lang = "es-ES";
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
        </script>
        """,
        unsafe_allow_html=True
    )


# ================= ESTILOS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
}

html, body, [class*="css"], label, p, span, div {
    color: white !important;
}

h1,h2,h3,h4 {
    color:white !important;
}

.card {
    background:white;
    color:#0A2A66 !important;
    padding:20px;
    border-radius:15px;
    height:150px;
    display:flex;
    justify-content:center;
    align-items:center;
    text-align:center;
    font-weight:bold;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
}

.title {
    font-size:34px;
    font-weight:bold;
    text-align:center;
    color:white;
}

.stButton>button {
    background:#1E4DB7;
    color:white;
    border-radius:10px;
    font-weight:bold;
    width:100%;
}

section[data-testid="stSidebar"] * {
    color:white !important;
}
</style>
""", unsafe_allow_html=True)


# ================= LOGO =================
st.sidebar.subheader("Cargar logo")
logo_file = st.sidebar.file_uploader("Sube el logo", type=["png","jpg","jpeg"])

if logo_file:
    st.session_state.logo = logo_file

if st.session_state.logo:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(st.session_state.logo, width=250)


# ================= ASISTENTE DE ACCESIBILIDAD =================
st.markdown("<div class='title'>Bienvenido a BACCITA</div>", unsafe_allow_html=True)

if not st.session_state.voz_activada:
    hablar("Bienvenido a BACCITA. Si es una persona con capacidades diferentes seleccione sí o no.")
    st.session_state.voz_activada = True

capacidades = st.radio(
    "¿Es usted una persona con capacidades diferentes?",
    ["No", "Sí"]
)

if capacidades == "Sí":
    no_vidente = st.radio(
        "¿Es una persona no vidente?",
        ["No", "Sí"]
    )

    if no_vidente == "Sí":
        st.session_state.modo_accesible = True
        hablar("Modo accesible activado. Todo el proceso será guiado por voz.")
    else:
        st.session_state.modo_accesible = False
        hablar("Puede continuar el proceso de agendamiento normalmente.")
else:
    st.session_state.modo_accesible = False


# ================= DATOS =================
trabajadores = {
    "Jubelkys Morales":"1111",
    "Adriana Navarro":"2222",
    "Ana Sandoval":"3333",
    "Eddy Cardoza":"4444",
    "Stefany Matamoros":"5555",
    "Badner Mendiola":"9999"
}

servicios = {
    "Apertura de cuentas":["Ahorro","Corriente","Empresarial","Estudiantil"],
    "Créditos":["Personal","Hipotecario","Vehículo","Empresarial"],
    "Consultas":["Tarjetas","Transferencias","Intereses","Banca digital"],
    "Asesoría":["Plan ahorro","Estado cuenta","Créditos","Hipotecas"],
    "Actualización":["Cambio cuenta","Clausura"]
}


def horas():
    h=[]
    t=datetime.combine(datetime.today(),time(8))
    while t+timedelta(minutes=35)<=datetime.combine(datetime.today(),time(17)):
        h.append(t.strftime("%H:%M"))
        t+=timedelta(minutes=35)
    return h


menu = st.sidebar.radio("Menú",["Cliente","Trabajador","Postservicio"])


# =================================================
# CLIENTE
# =================================================
if menu=="Cliente":

    st.markdown("<div class='title'>Agendamiento de Citas</div>", unsafe_allow_html=True)

    if st.session_state.modo_accesible:
        hablar("Indique su nombre completo.")

    nombre = st.text_input("Nombre completo")

    if st.session_state.modo_accesible and nombre:
        hablar("Ingrese su número de cédula.")

    cedula = st.text_input("Cédula")

    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

    discapacidad = st.checkbox("Usuario con capacidades diferentes")

    servicio = st.selectbox("Servicio", list(servicios.keys()))
    sub = st.selectbox("Tipo de servicio", servicios[servicio])

    fecha = st.date_input("Fecha")
    hora = st.selectbox("Hora", horas())

    if st.button("AGENDAR CITA"):

        if nombre and cedula:

            if discapacidad:
                trabajador_asignado = "Badner Mendiola"
            else:
                trabajador_asignado = list(trabajadores.keys())[len(st.session_state.citas) % 5]

            st.session_state.citas.append({
                "cliente":nombre,
                "cedula":cedula,
                "trabajador":trabajador_asignado,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Pendiente",
                "inicio":None,
                "fin":None,
                "duracion":0,
                "calificacion":None
            })

            st.success(f"Cita asignada a {trabajador_asignado}")

            if st.session_state.modo_accesible:
                hablar(f"Su cita fue registrada correctamente con {trabajador_asignado}")

        else:
            st.error("Completa los datos requeridos.")
