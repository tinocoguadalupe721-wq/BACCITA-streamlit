import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTILO PRO =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0A2A66,#1E4DB7);
    color: white;
}

/* tarjetas */
.card {
    background:white;
    color:#0A2A66;
    padding:20px;
    border-radius:15px;
    height:130px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    box-shadow:0px 8px 20px rgba(0,0,0,0.2);
}

/* KPI */
.kpi {
    background:white;
    color:#0A2A66;
    padding:15px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 5px 15px rgba(0,0,0,0.2);
}

/* títulos */
.title {
    font-size:34px;
    font-weight:bold;
    text-align:center;
    margin-bottom:20px;
}

/* botones */
.stButton>button {
    background:#1E4DB7;
    color:white;
    border-radius:10px;
    height:45px;
    font-weight:bold;
}

/* inputs */
input, textarea {
    border-radius:8px !important;
}
</style>
""", unsafe_allow_html=True)

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []

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
    "Apertura":["Ahorro","Corriente","Empresarial","Estudiantil"],
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

    col1,col2 = st.columns(2)

    with col1:
        nombre = st.text_input("Nombre completo")
        cedula = st.text_input("Cédula")
        telefono = st.text_input("Teléfono")

    with col2:
        correo = st.text_input("Correo")
        direccion = st.text_input("Dirección")
        ocupacion = st.text_input("Ocupación")

    servicio = st.selectbox("Servicio", list(servicios.keys()))
    sub = st.selectbox("Tipo", servicios[servicio])

    col1,col2 = st.columns(2)
    with col1:
        fecha = st.date_input("Fecha")
    with col2:
        hora = st.selectbox("Hora", horas())

    if st.button("AGENDAR CITA"):
        st.session_state.citas.append({
            "cliente":nombre,
            "trabajador":"Jubelkys Morales",
            "fecha":str(fecha),
            "hora":hora,
            "estado":"Pendiente",
            "inicio":None,
            "fin":None,
            "duracion":None,
            "calificacion":None
        })
        st.success("Cita registrada correctamente")

# =================================================
# TRABAJADOR
# =================================================
if menu=="Trabajador":

    st.markdown("<div class='title'>Panel del Trabajador</div>", unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    with col1:
        user = st.selectbox("Trabajador", list(trabajadores.keys()))
    with col2:
        pw = st.text_input("Clave", type="password")

    if user in trabajadores and pw == trabajadores[user]:

        fecha = st.date_input("Filtrar por día")

        citas = [c for c in st.session_state.citas if c["trabajador"]==user and c["fecha"]==str(fecha)]

        st.subheader("Clientes asignados")

        tiempos=[]
        atendidas=0

        for i,c in enumerate(citas):

            st.markdown(f"<div class='card'>{c['cliente']}<br>{c['hora']}<br>{c['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"START {i}"):
                c["inicio"]=datetime.now()
                c["estado"]="En proceso"

            if col2.button(f"END {i}"):
                c["fin"]=datetime.now()
                c["estado"]="Finalizada"
                c["duracion"]=(c["fin"]-c["inicio"]).seconds/60

            if c["duracion"]:
                st.write(f"Duración: {c['duracion']:.2f} min")
                tiempos.append(c["duracion"])
                atendidas+=1

        # KPI VISUAL
        total=len(citas)
        cumplimiento=(atendidas/total*100) if total>0 else 0
        promedio=(sum(tiempos)/len(tiempos)) if tiempos else 0

        calidad = [c["calificacion"] for c in citas if c["calificacion"]]
        calidad_prom = sum(calidad)/len(calidad) if calidad else 0

        st.subheader("KPIs")

        k1,k2,k3 = st.columns(3)

        k1.metric("Cumplimiento", f"{cumplimiento:.1f}%")
        k2.metric("Tiempo Promedio", f"{promedio:.1f} min")
        k3.metric("Calidad", f"{calidad_prom:.1f}/5")

        if tiempos:
            st.line_chart(tiempos)

        if calidad:
            st.bar_chart(calidad)

# =================================================
# POST SERVICIO
# =================================================
if menu=="Postservicio":

    st.markdown("<div class='title'>Evaluación del Servicio</div>", unsafe_allow_html=True)

    for i,c in enumerate(st.session_state.citas):

        if c["estado"]=="Finalizada":

            st.markdown(f"<div class='card'>{c['cliente']} - {c['trabajador']}</div>", unsafe_allow_html=True)

            p1 = st.slider("Satisfacción",1,5)
            p2 = st.slider("Tiempo adecuado",1,5)
            p3 = st.slider("Recomendación",1,5)

            if st.button(f"Guardar {i}"):
                c["calificacion"]=(p1+p2+p3)/3
                st.success("Evaluación guardada")
