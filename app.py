import streamlit as st
from datetime import datetime, timedelta, time
import pandas as pd

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

# LOGO DINÁMICO
if "logo" not in st.session_state:
    st.session_state.logo = None

# ================= ESTILOS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
}

/* TEXTO BLANCO GLOBAL */
html, body, [class*="css"] {
    color: white !important;
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
}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.sidebar.subheader("Cargar logo")
logo_file = st.sidebar.file_uploader("Sube el logo", type=["png","jpg","jpeg"])

if logo_file:
    st.session_state.logo = logo_file

if st.session_state.logo:
    st.image(st.session_state.logo, width=180)

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

# ================= KPI INTELIGENTE =================
def evaluar_tiempo(minutos):
    if 30 <= minutos <= 35:
        return 100
    elif minutos > 35:
        return 60
    elif minutos < 5:
        return 40
    else:
        return 80

menu = st.sidebar.radio("Menú",["Cliente","Trabajador","Postservicio"])

# =================================================
# CLIENTE
# =================================================
if menu=="Cliente":

    st.markdown("<div class='title'>BACCITA</div>", unsafe_allow_html=True)

    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Cédula")
    telefono = st.text_input("Teléfono")
    correo = st.text_input("Correo")

    no_vidente = st.checkbox("¿Usuario no vidente?")

    servicio = st.selectbox("Servicio", list(servicios.keys()))
    sub = st.selectbox("Tipo de servicio", servicios[servicio])

    fecha = st.date_input("Fecha")
    hora = st.selectbox("Hora", horas())

    if st.button("AGENDAR CITA"):

        if nombre and cedula:

            if no_vidente:
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

        citas_dia = [c for c in st.session_state.citas 
                     if c["trabajador"]==user and c["fecha"]==str(fecha)]

        if citas_dia:

            nombres = [f"{c['cliente']} - {c['hora']}" for c in citas_dia]

            seleccion = st.selectbox("Selecciona la cita", nombres)

            idx = nombres.index(seleccion)
            cita = citas_dia[idx]

            st.markdown(f"<div class='card'>{cita['cliente']}<br>{cita['hora']}<br>{cita['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button("START CITA"):
                cita["inicio"]=datetime.now()
                cita["estado"]="En proceso"

            if col2.button("END CITA"):
                cita["fin"]=datetime.now()
                cita["estado"]="Finalizada"

                if cita["inicio"]:
                    cita["duracion"]=(cita["fin"]-cita["inicio"]).seconds/60

            if cita["estado"]=="En proceso" and cita["inicio"]:
                tiempo_actual = (datetime.now() - cita["inicio"]).seconds/60
                st.warning(f"⏱ En curso: {tiempo_actual:.1f} min")

            if cita["duracion"]>0:
                st.success(f"Duración final: {cita['duracion']:.1f} min")

        else:
            st.info("No hay citas para este día")

        # ================= KPI =================
        tiempos = [c["duracion"] for c in citas_dia if c["duracion"]>0]
        rendimiento = [evaluar_tiempo(t) for t in tiempos]
        calificaciones = [c["calificacion"] for c in citas_dia if c["calificacion"]]

        total=len(citas_dia)
        atendidas=len(tiempos)

        cumplimiento=(atendidas/total*100) if total>0 else 0
        uso = total
        satisfaccion=(sum(calificaciones)/len(calificaciones)) if calificaciones else 0

        st.subheader("KPIs del sistema")

        k1,k2,k3 = st.columns(3)
        k1.metric("Cumplimiento de citas", f"{cumplimiento:.1f}%")
        k2.metric("Citas gestionadas", uso)
        k3.metric("Satisfacción", f"{satisfaccion:.1f}%")

        # ================= GRAFICAS =================
        st.subheader("📊 Análisis de desempeño")

        if not tiempos:
            tiempos=[0]
        if not rendimiento:
            rendimiento=[0]
        if not calificaciones:
            calificaciones=[0]

        df_t = pd.DataFrame({"Cita":range(1,len(tiempos)+1),"Duración":tiempos})
        df_r = pd.DataFrame({"Cita":range(1,len(rendimiento)+1),"Rendimiento":rendimiento})
        df_c = pd.DataFrame({"Cita":range(1,len(calificaciones)+1),"Calidad":calificaciones})

        st.markdown("### ⏱ Duración de citas")
        st.line_chart(df_t.set_index("Cita"))

        st.markdown("### 🎯 Rendimiento según tiempo (%)")
        st.bar_chart(df_r.set_index("Cita"))

        st.markdown("### ⭐ Satisfacción del cliente")
        st.bar_chart(df_c.set_index("Cita"))

# =================================================
# POST SERVICIO
# =================================================
if menu=="Postservicio":

    st.markdown("<div class='title'>Evaluación del Servicio</div>", unsafe_allow_html=True)

    pendientes = [c for c in st.session_state.citas 
                  if c["estado"]=="Finalizada" and c["calificacion"] is None]

    if pendientes:

        nombres = [f"{c['cliente']} - {c['trabajador']}" for c in pendientes]

        seleccion = st.selectbox("Selecciona la cita", nombres)

        idx = nombres.index(seleccion)
        cita = pendientes[idx]

        st.markdown(f"<div class='card'>{cita['cliente']}<br>{cita['trabajador']}</div>", unsafe_allow_html=True)

        st.subheader("Evaluación (Sí / No)")

        p1 = st.checkbox("¿El trabajador fue amable?")
        p2 = st.checkbox("¿El tiempo fue adecuado?")
        p3 = st.checkbox("¿Se resolvió el problema?")
        p4 = st.checkbox("¿La información fue clara?")
        p5 = st.checkbox("¿Recomendaría el servicio?")

        if st.button("Guardar evaluación"):

            respuestas = [p1,p2,p3,p4,p5]
            puntaje = sum(respuestas)/5*100

            cita["calificacion"] = puntaje

            st.success("Evaluación guardada ✔")

    else:
        st.info("No hay evaluaciones pendientes")
