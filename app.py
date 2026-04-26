import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "citas" not in st.session_state:
    st.session_state.citas = []
if "no_vidente" not in st.session_state:
    st.session_state.no_vidente = False
if "logo" not in st.session_state:
    st.session_state.logo = None

# ================= ESTILOS =================
st.markdown("""
<style>
.card {
    background:white;
    padding:20px;
    border-radius:12px;
    margin-bottom:10px;
}
.logo {
    width:160px;
    display:block;
    margin:auto;
}
.float {
    position:fixed;
    bottom:30px;
    right:30px;
    font-size:40px;
    animation: floaty 3s infinite ease-in-out;
}
@keyframes floaty {
    0% {transform:translateY(0);}
    50% {transform:translateY(-20px);}
    100% {transform:translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ================= VOZ =================
def voz(texto):
    if st.session_state.no_vidente:
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{texto}");
        msg.lang = "es-ES";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ================= LOGO =================
st.sidebar.subheader("Subir logo")
logo_file = st.sidebar.file_uploader("Logo", type=["png","jpg"])
if logo_file:
    st.session_state.logo = logo_file

if st.session_state.logo:
    st.image(st.session_state.logo, width=150)

# ================= SERVICIOS =================
servicios = {
    "Apertura":["Ahorro","Corriente"],
    "Consultas":["Tarjetas","Transferencias"]
}

trabajadores = {
    "Apertura":"SERVIDOR JUBELKYS",
    "Consultas":"SERVIDOR ADRIANA"
}

# SERVIDOR ESPECIAL
if st.session_state.no_vidente:
    trabajadores = {k:"SERVIDOR BADNER" for k in trabajadores}

# ================= HORAS =================
def horas():
    h=[]
    t=datetime.combine(datetime.today(),time(8))
    fin=datetime.combine(datetime.today(),time(17))
    while t+timedelta(minutes=35)<=fin:
        h.append(t.strftime("%H:%M"))
        t+=timedelta(minutes=35)
    return h

menu = st.sidebar.selectbox("Modo",["Cliente","Trabajador","Dashboard"])

# ================= CLIENTE =================
if menu=="Cliente":

    st.title("BACCITA")

    if st.session_state.paso==1:

        st.session_state.no_vidente = st.checkbox("No vidente")

        voz("Bienvenido. Ingresa tus datos")

        nombre = st.text_input("Nombre")

        if st.button("Continuar") and nombre:
            st.session_state.nombre = nombre
            st.session_state.paso=2
            st.rerun()

    elif st.session_state.paso==2:

        for s in servicios:
            if st.button(s):
                st.session_state.servicio=s
                st.session_state.paso=3
                st.rerun()

    elif st.session_state.paso==3:

        for sub in servicios[st.session_state.servicio]:
            if st.button(sub):
                st.session_state.detalle=sub
                st.session_state.paso=4
                st.rerun()

    elif st.session_state.paso==4:

        servidor = trabajadores[st.session_state.servicio]

        st.success(servidor)

        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", horas())

        if st.button("CONFIRMAR"):
            st.session_state.citas.append({
                "cliente":st.session_state.nombre,
                "trabajador":servidor,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Pendiente",
                "inicio":None,
                "fin":None,
                "calificacion":None
            })
            st.session_state.paso=5
            st.rerun()

    elif st.session_state.paso==5:
        st.success("CITA REGISTRADA 🎉")
        voz("Tu cita fue registrada exitosamente")

# ================= TRABAJADOR =================
if menu=="Trabajador":

    st.header("Panel trabajador")

    nombre = st.text_input("Nombre trabajador")

    for c in st.session_state.citas:
        if c["trabajador"]==nombre:

            st.markdown(f"<div class='card'>{c['cliente']} - {c['hora']}</div>", unsafe_allow_html=True)

            col1,col2,col3 = st.columns(3)

            if col1.button(f"Start {c['hora']}"):
                c["inicio"]=datetime.now()
                c["estado"]="En proceso"

            if col2.button(f"End {c['hora']}"):
                c["fin"]=datetime.now()
                c["estado"]="Finalizada"

            if col3.button(f"Calificar {c['hora']}"):
                c["calificacion"]=5

# ================= DASHBOARD =================
if menu=="Dashboard":

    st.title("KPIs")

    total = len(st.session_state.citas)
    finalizadas = len([c for c in st.session_state.citas if c["estado"]=="Finalizada"])

    if total>0:
        cumplimiento = (finalizadas/total)*100
        st.metric("Cumplimiento", f"{cumplimiento:.2f}%")

    tiempos = []
    for c in st.session_state.citas:
        if c["inicio"] and c["fin"]:
            t = (c["fin"]-c["inicio"]).seconds/60
            tiempos.append(t)

    if tiempos:
        st.line_chart(tiempos)

# ================= ICONO =================
st.markdown("<div class='float'>🎉</div>", unsafe_allow_html=True)
