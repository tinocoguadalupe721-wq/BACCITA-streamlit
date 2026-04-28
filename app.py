# ================= IMPORTACIONES =================
import streamlit as st
from datetime import datetime, timedelta, time
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

if "logo" not in st.session_state:
    st.session_state.logo = None

# ================= FUNCIONES DE VOZ =================
def hablar(texto):
    components.html(f"""
    <script>
        function hablarTexto() {{
            var mensaje = new SpeechSynthesisUtterance("{texto}");
            mensaje.lang = "es-ES";
            mensaje.rate = 1;
            window.speechSynthesis.cancel();
            window.speechSynthesis.speak(mensaje);
        }}
        hablarTexto();
    </script>
    """, height=0)

def reconocimiento_voz():
    components.html("""
    <script>
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = "es-ES";
            recognition.continuous = false;
            recognition.interimResults = false;

            recognition.start();

            recognition.onresult = function(event) {
                const texto = event.results[0][0].transcript;
                const input = window.parent.document.querySelector('input[aria-label="Respuesta por voz"]');
                if (input) {
                    const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype,
                        "value"
                    ).set;
                    nativeInputValueSetter.call(input, texto);
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                }
            };
        }
    </script>
    """, height=0)

# ================= ESTILOS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
}

/* TEXTO GENERAL */
html, body, [class*="css"], label, p, span, div, h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* INPUTS */
input, textarea {
    color: #0A2A66 !important;
    background-color: white !important;
}

/* SELECTBOX */
div[data-baseweb="select"] * {
    color: #0A2A66 !important;
}

/* DATE INPUT */
[data-testid="stDateInput"] * {
    color: #0A2A66 !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #081F4D;
}

/* CARD */
.card {
    background:white;
    color:#0A2A66 !important;
    padding:20px;
    border-radius:15px;
    height:180px;
    display:flex;
    justify-content:center;
    align-items:center;
    text-align:center;
    font-weight:bold;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
    font-size:20px;
}

/* TITULOS */
.title {
    font-size:34px;
    font-weight:bold;
    text-align:center;
    color:white;
    margin-bottom:20px;
}

/* BOTONES */
.stButton>button {
    background:#1E4DB7;
    color:white !important;
    border-radius:10px;
    font-weight:bold;
    width:100%;
}

/* LOGO */
.logo-container {
    display:flex;
    justify-content:center;
    margin-top:10px;
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.sidebar.subheader("Cargar logo")
logo_file = st.sidebar.file_uploader("Sube el logo", type=["png", "jpg", "jpeg"])

if logo_file:
    st.session_state.logo = logo_file

if st.session_state.logo:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(st.session_state.logo, width=250)

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

# ================= HORARIOS =================
def horas():
    h = []
    t = datetime.combine(datetime.today(), time(8))
    while t + timedelta(minutes=35) <= datetime.combine(datetime.today(), time(17)):
        h.append(t.strftime("%H:%M"))
        t += timedelta(minutes=35)
    return h

# ================= KPI =================
def evaluar_tiempo(minutos):
    if 30 <= minutos <= 35:
        return 100
    elif minutos > 35:
        return 60
    elif minutos < 5:
        return 40
    else:
        return 80

# ================= MENU =================
menu = st.sidebar.radio("Menú", ["Cliente","Trabajador","Postservicio"])

# =================================================
# CLIENTE
# =================================================
if menu == "Cliente":

    st.markdown("<div class='title'>BACCITA</div>", unsafe_allow_html=True)

    hablar("Bienvenido a BACCITA. Si usted es una persona con capacidades diferentes, responda sí o no.")

    respuesta_voz = st.text_input("Respuesta por voz")

    if st.button("Activar micrófono"):
        reconocimiento_voz()

    discapacidad = False
    no_vidente = False

    if respuesta_voz.lower() == "sí" or respuesta_voz.lower() == "si":
        discapacidad = True
        hablar("¿Es una persona no vidente? Responda sí o no.")

        respuesta_no_vidente = st.text_input("Respuesta discapacidad visual")

        if st.button("Responder discapacidad visual"):
            reconocimiento_voz()

        if respuesta_no_vidente.lower() == "sí" or respuesta_no_vidente.lower() == "si":
            no_vidente = True
            hablar("Sistema de asistencia por voz activado. Proceda a dictar sus datos.")
        else:
            hablar("Puede continuar el proceso de agendamiento.")
    elif respuesta_voz.lower() == "no":
        hablar("Puede registrar su cita autónomamente. Gracias.")

    # FORMULARIO
    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

    discapacidad_check = st.checkbox("¿Usuario con capacidades diferentes?")

    servicio = st.selectbox("Servicio", list(servicios.keys()))
    sub = st.selectbox("Tipo de servicio", servicios[servicio])

    fecha = st.date_input("Fecha")
    hora = st.selectbox("Hora", horas())

    if st.button("AGENDAR CITA"):

        if nombre and cedula:

            if no_vidente or discapacidad_check:
                trabajador_asignado = "Badner Mendiola"
            else:
                trabajador_asignado = list(trabajadores.keys())[len(st.session_state.citas) % 5]

            st.session_state.citas.append({
                "cliente": nombre,
                "cedula": cedula,
                "telefono": telefono,
                "correo": correo,
                "trabajador": trabajador_asignado,
                "fecha": str(fecha),
                "hora": hora,
                "servicio": servicio,
                "subservicio": sub,
                "estado": "Pendiente",
                "inicio": None,
                "fin": None,
                "duracion": 0,
                "calificacion": None,
                "comentario": ""
            })

            st.success(f"Cita asignada a {trabajador_asignado}")
            hablar("Su cita ha sido agendada exitosamente.")

        else:
            st.error("Completa los datos")
            hablar("Faltan datos por completar.")

# =================================================
# TRABAJADOR
# =================================================
if menu == "Trabajador":

    st.markdown("<div class='title'>Panel del Trabajador</div>", unsafe_allow_html=True)

    hablar("Bienvenido al panel del trabajador.")

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
                f"""
                <div class='card'>
                    {cita['cliente']}<br>
                    {cita['hora']}<br>
                    {cita['estado']}
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            if col1.button("START CITA"):
                cita["inicio"] = datetime.now()
                cita["estado"] = "En proceso"
                hablar("La cita ha iniciado.")

            if col2.button("END CITA"):
                cita["fin"] = datetime.now()
                cita["estado"] = "Finalizada"

                if cita["inicio"]:
                    cita["duracion"] = (cita["fin"] - cita["inicio"]).seconds / 60

                hablar("La cita ha finalizado correctamente.")

            if cita["estado"] == "En proceso" and cita["inicio"]:
                tiempo_actual = (datetime.now() - cita["inicio"]).seconds / 60
                st.warning(f"En curso: {tiempo_actual:.1f} min")

            if cita["duracion"] > 0:
                st.success(f"Duración final: {cita['duracion']:.1f} min")

        else:
            st.info("No hay citas para este día")

        # KPIs
        tiempos = [c["duracion"] for c in citas_dia if c["duracion"] > 0]
        rendimiento = [evaluar_tiempo(t) for t in tiempos]
        calificaciones = [c["calificacion"] for c in citas_dia if c["calificacion"]]

        total = len(citas_dia)
        atendidas = len(tiempos)

        cumplimiento = (atendidas / total * 100) if total > 0 else 0
        uso = total
        satisfaccion = (sum(calificaciones) / len(calificaciones)) if calificaciones else 0

        st.subheader("KPIs del sistema")

        k1, k2, k3 = st.columns(3)
        k1.metric("Cumplimiento de citas", f"{cumplimiento:.1f}%")
        k2.metric("Citas gestionadas", uso)
        k3.metric("Satisfacción", f"{satisfaccion:.1f}%")

        # GRAFICAS
        st.subheader("Análisis de desempeño")

        if not tiempos:
            tiempos = [0]
        if not rendimiento:
            rendimiento = [0]
        if not calificaciones:
            calificaciones = [0]

        df_t = pd.DataFrame({"Cita": range(1, len(tiempos)+1), "Duración": tiempos})
        df_r = pd.DataFrame({"Cita": range(1, len(rendimiento)+1), "Rendimiento": rendimiento})
        df_c = pd.DataFrame({"Cita": range(1, len(calificaciones)+1), "Calidad": calificaciones})

        st.markdown("### Duración de citas")
        st.line_chart(df_t.set_index("Cita"))

        st.markdown("### Rendimiento según tiempo (%)")
        st.bar_chart(df_r.set_index("Cita"))

        st.markdown("### Satisfacción del cliente")
        st.bar_chart(df_c.set_index("Cita"))

# =================================================
# POST SERVICIO
# =================================================
if menu == "Postservicio":

    st.markdown("<div class='title'>Evaluación del Servicio</div>", unsafe_allow_html=True)

    hablar("Bienvenido al módulo de evaluación del servicio.")

    pendientes = [
        c for c in st.session_state.citas
        if c["estado"] == "Finalizada" and c["calificacion"] is None
    ]

    if pendientes:

        nombres = [f"{c['cliente']} - {c['trabajador']}" for c in pendientes]

        seleccion = st.selectbox("Selecciona la cita", nombres)

        idx = nombres.index(seleccion)
        cita = pendientes[idx]

        st.markdown(
            f"""
            <div class='card'>
                {cita['cliente']}<br>
                {cita['trabajador']}<br>
                {cita['servicio']} - {cita['subservicio']}
            </div>
            """,
            unsafe_allow_html=True
        )

        hablar(
            f"Está evaluando la atención brindada por {cita['trabajador']}. Por favor responda las preguntas."
        )

        st.subheader("Evaluación del Servicio (Sí / No)")

        p1 = st.checkbox("¿El trabajador fue amable?")
        p2 = st.checkbox("¿El tiempo fue adecuado?")
        p3 = st.checkbox("¿Se resolvió el problema?")
        p4 = st.checkbox("¿La información fue clara?")
        p5 = st.checkbox("¿Recomendaría el servicio?")
        p6 = st.checkbox("¿El sistema fue accesible?")
        p7 = st.checkbox("¿Volvería a utilizar este sistema?")

        comentario = st.text_area("Comentarios adicionales (opcional)")

        if st.button("Guardar evaluación"):

            respuestas = [p1, p2, p3, p4, p5, p6, p7]

            puntaje = sum(respuestas) / len(respuestas) * 100

            cita["calificacion"] = puntaje
            cita["comentario"] = comentario

            st.success("Evaluación guardada correctamente")

            if puntaje >= 80:
                hablar("Gracias. Su nivel de satisfacción es alto.")
            elif puntaje >= 50:
                hablar("Gracias. Su nivel de satisfacción es medio.")
            else:
                hablar("Gracias. Trabajaremos para mejorar su experiencia.")

            st.subheader("Resultado de satisfacción")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Calificación obtenida", f"{puntaje:.1f}%")

            with col2:
                if puntaje >= 80:
                    st.success("Nivel de satisfacción: Alto")
                elif puntaje >= 50:
                    st.warning("Nivel de satisfacción: Medio")
                else:
                    st.error("Nivel de satisfacción: Bajo")

    else:
        st.info("No hay evaluaciones pendientes")
        hablar("Actualmente no hay evaluaciones pendientes.")
