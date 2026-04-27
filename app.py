import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "citas" not in st.session_state:
    st.session_state.citas = []
if "fotos" not in st.session_state:
    st.session_state.fotos = {}
if "logo" not in st.session_state:
    st.session_state.logo = None

# ================= COLORES =================
st.markdown("""
<style>
.stApp {background:#EEF4FF;}

.bloque {
    height:150px;
    border-radius:15px;
    background:#FFFFFF;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:20px;
    font-weight:bold;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}

.titulo {
    text-align:center;
    font-size:32px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.sidebar.title("Configuración")

logo = st.sidebar.file_uploader("Subir logo", type=["png","jpg"])
if logo:
    st.session_state.logo = logo

if st.session_state.logo:
    st.image(st.session_state.logo, width=150)

# ================= TRABAJADORES =================
trabajadores = {
    "Jubelkys Morales":"1111",
    "Adriana Navarro":"2222",
    "Ana Sandoval":"3333",
    "Eddy Cardoza":"4444",
    "Stefany Matamoros":"5555",
    "Badner Mendiola":"9999"
}

# subir foto
trab_sel = st.sidebar.selectbox("Trabajador", list(trabajadores.keys()))
foto = st.sidebar.file_uploader("Foto trabajador", type=["png","jpg"])
if foto:
    st.session_state.fotos[trab_sel] = foto

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas":[
        "Ahorro","Corriente","Empresarial","Estudiantil"
    ],
    "Créditos":[
        "Personal","Hipotecario","Vehículo","Empresarial"
    ],
    "Consultas":[
        "Tarjetas","Transferencias","Intereses","Banca digital"
    ],
    "Asesoría":[
        "Plan ahorro","Estado cuenta","Créditos","Hipotecas"
    ],
    "Actualización":[
        "Cambio cuenta","Clausura"
    ]
}

# ================= HORAS =================
def horas():
    h=[]
    t=datetime.combine(datetime.today(),time(8))
    while t+timedelta(minutes=35)<=datetime.combine(datetime.today(),time(17)):
        h.append(t.strftime("%H:%M"))
        t+=timedelta(minutes=35)
    return h

menu = st.sidebar.selectbox("Modo",["Cliente","Trabajador","Postservicio"])

# =================================================
# CLIENTE
# =================================================
if menu=="Cliente":

    st.markdown("<div class='titulo'>BACCITA</div>", unsafe_allow_html=True)

    nombre = st.text_input("Nombre")

    st.subheader("Servicio")

    cols = st.columns(2)
    i=0
    for s in servicios:
        with cols[i%2]:
            if st.button(s, use_container_width=True):
                st.session_state.servicio=s
        i+=1

    if "servicio" in st.session_state:
        st.subheader("Tipo de servicio")

        cols = st.columns(2)
        for sub in servicios[st.session_state.servicio]:
            if st.button(sub, use_container_width=True):
                st.session_state.detalle=sub

    if "detalle" in st.session_state:
        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", horas())

        if st.button("Agendar cita"):
            st.session_state.citas.append({
                "cliente":nombre,
                "trabajador":"Jubelkys Morales",
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Pendiente",
                "inicio":None,
                "fin":None,
                "calificacion":None
            })
            st.success("Cita agendada")

# =================================================
# TRABAJADOR
# =================================================
if menu=="Trabajador":

    st.title("Panel trabajador")

    col1,col2 = st.columns(2)

    with col1:
        user = st.selectbox("Nombre", list(trabajadores.keys()))
    with col2:
        pw = st.text_input("Clave", type="password")

    if user in trabajadores and pw == trabajadores[user]:

        if user in st.session_state.fotos:
            st.image(st.session_state.fotos[user], width=120)

        fecha = st.date_input("Filtrar por día")

        citas = [c for c in st.session_state.citas if c["trabajador"]==user and c["fecha"]==str(fecha)]

        st.subheader("Citas asignadas")

        tiempos=[]
        atendidas=0

        for i,c in enumerate(citas):

            st.markdown(f"<div class='bloque'>{c['cliente']} - {c['hora']} - {c['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"START {i}"):
                c["inicio"]=datetime.now()
                c["estado"]="En proceso"

            if col2.button(f"END {i}"):
                c["fin"]=datetime.now()
                c["estado"]="Finalizada"

            if c["inicio"] and c["fin"]:
                t=(c["fin"]-c["inicio"]).seconds/60
                tiempos.append(t)
                atendidas+=1

        # KPI
        total=len(citas)
        cumplimiento=(atendidas/total*100) if total>0 else 0
        promedio=(sum(tiempos)/len(tiempos)) if tiempos else 0

        calidad = [c["calificacion"] for c in citas if c["calificacion"]]
        calidad_prom = sum(calidad)/len(calidad) if calidad else 0

        st.subheader("KPIs")

        st.metric("Citas atendidas %", f"{cumplimiento:.1f}%")
        st.metric("Tiempo promedio", f"{promedio:.1f} min")
        st.metric("Calidad servicio", f"{calidad_prom:.1f}/5")

        # GRÁFICAS
        if tiempos:
            st.line_chart(tiempos)

        if calidad:
            st.bar_chart(calidad)

# =================================================
# POST SERVICIO
# =================================================
if menu=="Postservicio":

    st.title("Evaluación del servicio")

    for i,c in enumerate(st.session_state.citas):

        if c["estado"]=="Finalizada":

            st.write(f"{c['cliente']} - {c['trabajador']}")

            cal = st.slider(f"Calificación {i}",1,5)

            if st.button(f"Guardar {i}"):
                c["calificacion"]=cal
                st.success("Evaluación guardada")
