import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= ESTILOS =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
}
html, body, [class*="css"] {
    color: #0A2A66 !important;
}
.card {
    background:white;
    color:#0A2A66;
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

            # asignación automática
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

        fecha = st.date_input("Filtrar por día")

        citas = [c for c in st.session_state.citas if c["trabajador"]==user and c["fecha"]==str(fecha)]

        st.subheader("Citas asignadas")

        tiempos=[]
        calificaciones=[]
        atendidas=0

        for i,c in enumerate(citas):

            st.markdown(f"<div class='card'>{c['cliente']}<br>{c['hora']}<br>{c['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            # START
            if col1.button(f"START {i}"):
                c["inicio"]=datetime.now()
                c["estado"]="En proceso"

            # END
            if col2.button(f"END {i}"):
                c["fin"]=datetime.now()
                c["estado"]="Finalizada"

                if c["inicio"]:
                    c["duracion"]=(c["fin"]-c["inicio"]).seconds/60

            # TIEMPO EN VIVO
            if c["estado"]=="En proceso" and c["inicio"]:
                tiempo_actual = (datetime.now() - c["inicio"]).seconds/60
                st.warning(f"⏱ En curso: {tiempo_actual:.1f} min")

            if c["duracion"]>0:
                st.success(f"Duración final: {c['duracion']:.1f} min")
                tiempos.append(c["duracion"])
                atendidas+=1

            if c["calificacion"]:
                calificaciones.append(c["calificacion"])

        # ================= KPI =================
        total=len(citas)
        cumplimiento=(atendidas/total*100) if total>0 else 0
        tiempo_prom = sum(tiempos)/len(tiempos) if tiempos else 0
        calidad = sum(calificaciones)/len(calificaciones) if calificaciones else 0

        st.subheader("KPIs")

        k1,k2,k3 = st.columns(3)
        k1.metric("Cumplimiento", f"{cumplimiento:.1f}%")
        k2.metric("Tiempo Promedio", f"{tiempo_prom:.1f} min")
        k3.metric("Calidad", f"{calidad:.1f}/5")

        # ================= GRAFICAS =================
        st.subheader("Gráficas de desempeño")

        if tiempos:
            st.line_chart(tiempos)

        if calificaciones:
            st.bar_chart(calificaciones)

# =================================================
# POST SERVICIO
# =================================================
if menu=="Postservicio":

    st.markdown("<div class='title'>Evaluación del Servicio</div>", unsafe_allow_html=True)

    evaluadas = 0

    for i,c in enumerate(st.session_state.citas):

        # SOLO SI NO HA SIDO EVALUADA
        if c["estado"]=="Finalizada" and c["calificacion"] is None:

            st.markdown(f"<div class='card'>{c['cliente']}<br>{c['trabajador']}</div>", unsafe_allow_html=True)

            st.subheader("Encuesta de calidad")

            p1 = st.slider("Atención del trabajador",1,5, key=f"p1{i}")
            p2 = st.slider("Tiempo de atención",1,5, key=f"p2{i}")
            p3 = st.slider("Resolución del problema",1,5, key=f"p3{i}")
            p4 = st.slider("Satisfacción general",1,5, key=f"p4{i}")
            p5 = st.slider("Recomendación",1,5, key=f"p5{i}")

            comentario = st.text_area("Comentario", key=f"c{i}")

            if st.button(f"Guardar evaluación {i}"):

                promedio = (p1+p2+p3+p4+p5)/5
                c["calificacion"] = promedio
                c["comentario"] = comentario

                st.success("Evaluación guardada ✔")
                evaluadas += 1

    if evaluadas == 0:
        st.info("No hay citas pendientes de evaluación")
