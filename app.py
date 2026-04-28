# ================= LIBRERÍAS =================
import streamlit as st
from datetime import datetime, timedelta, time
import pandas as pd
import pyttsx3
import speech_recognition as sr

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

if "logo" not in st.session_state:
    st.session_state.logo = None

if "bienvenida_voz" not in st.session_state:
    st.session_state.bienvenida_voz = False

if "modo_accesible" not in st.session_state:
    st.session_state.modo_accesible = False


# ================= FUNCIONES DE VOZ =================
def hablar(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 165)
        voices = engine.getProperty("voices")
        if voices:
            engine.setProperty("voice", voices[0].id)
        engine.say(texto)
        engine.runAndWait()
    except:
        pass

def escuchar():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        texto = recognizer.recognize_google(audio, language="es-ES")
        return texto.lower()
    except:
        return ""

# ================= BIENVENIDA AUTOMÁTICA =================
if not st.session_state.bienvenida_voz:
    hablar("Bienvenido a BACCITA")
    hablar("Si usted posee capacidades diferentes diga si o no")

    respuesta = escuchar()

    if "si" in respuesta:
        hablar("Es una persona no vidente? diga si o no")
        respuesta2 = escuchar()

        if "si" in respuesta2:
            st.session_state.modo_accesible = True
            hablar("Modo accesible activado. Todo el proceso será guiado por voz.")
        else:
            hablar("Puede continuar el proceso de agendamiento.")
    else:
        hablar("Puede continuar el proceso de agendamiento.")

    st.session_state.bienvenida_voz = True


# ================= ESTILOS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
}

/* TEXTO GENERAL */
html, body, [class*="css"], label, p, span, div {
    color: white !important;
}

/* Sidebar */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Inputs */
input, textarea {
    color: #0A2A66 !important;
}

/* Selectbox */
div[data-baseweb="select"] * {
    color: #0A2A66 !important;
}

/* Tarjetas */
.card {
    background:white;
    color:#0A2A66 !important;
    padding:20px;
    border-radius:15px;
    height:170px;
    display:flex;
    justify-content:center;
    align-items:center;
    text-align:center;
    font-weight:bold;
    font-size:20px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
}

/* Títulos */
.title {
    font-size:38px;
    font-weight:bold;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

/* Botones */
.stButton>button {
    background:#1E4DB7;
    color:white !important;
    border-radius:12px;
    font-weight:bold;
    width:100%;
    height:3em;
    font-size:16px;
}
</style>
""", unsafe_allow_html=True)


# ================= LOGO =================
st.sidebar.subheader("Cargar logo")
logo_file = st.sidebar.file_uploader("Sube el logo", type=["png","jpg","jpeg"])

if logo_file:
    st.session_state.logo = logo_file

# LOGO CENTRADO SIEMPRE
if st.session_state.logo:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(st.session_state.logo, width=260)


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


# ================= FUNCIONES =================
def horas():
    h=[]
    t=datetime.combine(datetime.today(),time(8))
    while t+timedelta(minutes=35)<=datetime.combine(datetime.today(),time(17)):
        h.append(t.strftime("%H:%M"))
        t+=timedelta(minutes=35)
    return h

def evaluar_tiempo(minutos):
    if 30 <= minutos <= 35:
        return 100
    elif minutos > 35:
        return 60
    elif minutos < 5:
        return 40
    else:
        return 80


# ================= MENÚ =================
menu = st.sidebar.radio("Menú",["Cliente","Trabajador","Postservicio"])


# =================================================
# CLIENTE
# =================================================
if menu=="Cliente":

    st.markdown("<div class='title'>BACCITA</div>", unsafe_allow_html=True)

    nombre_auto = ""
    cedula_auto = ""
    telefono_auto = ""
    correo_auto = ""

    # ================= REGISTRO POR VOZ =================
    if st.session_state.modo_accesible:
        st.subheader("Modo de asistencia por voz")

        if st.button("Iniciar asistencia por voz"):
            hablar("Diga su nombre completo")
            nombre_auto = escuchar()

            hablar("Diga su número de cédula")
            cedula_auto = escuchar()

            hablar("Diga su teléfono")
            telefono_auto = escuchar()

            hablar("Diga su correo electrónico")
            correo_auto = escuchar()

            hablar("Datos capturados correctamente")

    nombre = st.text_input("Nombre completo", value=nombre_auto)
    cedula = st.text_input("Cédula", value=cedula_auto)
    telefono = st.text_input("Teléfono", value=telefono_auto)
    correo = st.text_input("Correo", value=correo_auto)

    capacidades_diferentes = st.checkbox("¿Usuario con capacidades diferentes?")

    servicio = st.selectbox("Servicio", list(servicios.keys()))
    sub = st.selectbox("Tipo de servicio", servicios[servicio])

    fecha = st.date_input("Fecha")
    hora = st.selectbox("Hora", horas())

    if st.button("AGENDAR CITA"):

        if nombre and cedula:

            if capacidades_diferentes:
                trabajador_asignado = "Badner Mendiola"
            else:
                trabajador_asignado = list(trabajadores.keys())[len(st.session_state.citas) % 5]

            st.session_state.citas.append({
                "cliente":nombre,
                "cedula":cedula,
                "telefono":telefono,
                "correo":correo,
                "servicio":servicio,
                "subservicio":sub,
                "trabajador":trabajador_asignado,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Pendiente",
                "inicio":None,
                "fin":None,
                "duracion":0,
                "calificacion":None,
                "comentario":""
            })

            hablar("Su cita ha sido registrada exitosamente")

            st.success(f"Cita asignada a {trabajador_asignado}")

        else:
            st.error("Completa los datos")


# =================================================
# TRABAJADOR
# =================================================
if menu=="Trabajador":

    st.markdown("<div class='title'>Panel del Trabajador</div>", unsafe_allow_html=True)

    user = st.selectbox("Trabajador", list(trabajadores.keys()))
    pw = st.text_input("Clave", type="password")

    if user in trabajadores and pw == trabajadores[user]:

        fecha = st.date_input("Selecciona el día")

        citas_dia = [
            c for c in st.session_state.citas
            if c["trabajador"] == user and c["fecha"] == str(fecha)
        ]

        if citas_dia:

            nombres = [f"{c['cliente']} - {c['hora']}" for c in citas_dia]

            seleccion = st.selectbox("Selecciona la cita", nombres)

            idx = nombres.index(seleccion)
            cita = citas_dia[idx]

            st.markdown(
                f"<div class='card'>{cita['cliente']}<br>{cita['hora']}<br>{cita['estado']}</div>",
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            if col1.button("START CITA"):
                cita["inicio"] = datetime.now()
                cita["estado"] = "En proceso"

            if col2.button("END CITA"):
                cita["fin"] = datetime.now()
                cita["estado"] = "Finalizada"

                if cita["inicio"]:
                    cita["duracion"] = (cita["fin"] - cita["inicio"]).seconds / 60

            if cita["estado"] == "En proceso" and cita["inicio"]:
                tiempo_actual = (datetime.now() - cita["inicio"]).seconds / 60
                st.warning(f"Tiempo en curso: {tiempo_actual:.1f} min")

            if cita["duracion"] > 0:
                st.success(f"Duración final: {cita['duracion']:.1f} min")

        else:
            st.info("No hay citas para este día")
