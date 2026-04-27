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
if "fotos" not in st.session_state:
    st.session_state.fotos = {}

# ================= COLORES POR PROCESO =================
colores = {
    1:"#E3F2FD",
    2:"#E8F5E9",
    3:"#FFF3E0",
    4:"#FCE4EC",
    5:"#E0F7FA"
}

st.markdown(f"""
<style>
.stApp {{
    background:{colores[st.session_state.paso]};
}}

.card {{
    background:white;
    padding:20px;
    border-radius:12px;
    height:120px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    text-align:center;
    box-shadow:0px 3px 10px rgba(0,0,0,0.1);
}}

.title {{
    text-align:center;
    font-size:30px;
    font-weight:bold;
}}
</style>
""", unsafe_allow_html=True)

# ================= VOZ =================
def voz(txt):
    if st.session_state.no_vidente:
        st.markdown(f"""
        <script>
        var msg = new SpeechSynthesisUtterance("{txt}");
        msg.lang = "es-ES";
        window.speechSynthesis.speak(msg);
        </script>
        """, unsafe_allow_html=True)

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas":[
        "Cuenta de ahorro",
        "Cuenta corriente",
        "Cuenta empresarial",
        "Cuenta estudiantil"
    ],
    "Solicitud de créditos":[
        "Crédito personal",
        "Crédito hipotecario",
        "Crédito vehículo",
        "Crédito empresarial"
    ],
    "Consultas a problemas":[
        "Tarjetas",
        "Transferencias",
        "Intereses",
        "Banca digital"
    ],
    "Asesoría bancaria":[
        "Plan ahorro",
        "Estado de cuenta",
        "Créditos",
        "Hipotecas"
    ],
    "Actualización de información":[
        "Cambio de cuenta",
        "Clausura"
    ]
}

# ================= TRABAJADORES =================
trabajadores = {
    "Jubelkys Morales":"1111",
    "Adriana Navarro":"2222",
    "Ana Sandoval":"3333",
    "Eddy Cardoza":"4444",
    "Stefany Matamoros":"5555",
    "Badner Mendiola":"9999"
}

# ================= HORAS =================
def horas():
    h=[]
    t=datetime.combine(datetime.today(),time(8))
    fin=datetime.combine(datetime.today(),time(17))
    while t+timedelta(minutes=35)<=fin:
        h.append(t.strftime("%H:%M"))
        t+=timedelta(minutes=35)
    return h

menu = st.sidebar.selectbox("Modo",["Cliente","Trabajador"])

# =================================================
# ================= CLIENTE ========================
# =================================================
if menu=="Cliente":

    st.markdown("<div class='title'>BACCITA</div>", unsafe_allow_html=True)

    # PASO 1 DATOS
    if st.session_state.paso==1:

        st.session_state.no_vidente = st.checkbox("No vidente")

        voz("Bienvenido. Ingrese sus datos personales")

        nombre = st.text_input("Nombre completo")
        cedula = st.text_input("Cédula")
        telefono = st.text_input("Teléfono")
        correo = st.text_input("Correo")

        if st.button("Continuar"):
            if nombre and cedula and telefono:
                st.session_state.nombre = nombre
                st.session_state.paso=2
                st.rerun()

    # PASO 2 SERVICIO
    elif st.session_state.paso==2:

        cols = st.columns(2)
        i=0
        for s in servicios:
            with cols[i%2]:
                if st.button(s, use_container_width=True):
                    st.session_state.servicio=s
                    st.session_state.paso=3
                    st.rerun()
            i+=1

    # PASO 3 SUBSERVICIO
    elif st.session_state.paso==3:

        cols = st.columns(2)
        i=0
        for sub in servicios[st.session_state.servicio]:
            with cols[i%2]:
                if st.button(sub, use_container_width=True):
                    st.session_state.detalle=sub
                    st.session_state.paso=4
                    st.rerun()
            i+=1

    # PASO 4 CITA
    elif st.session_state.paso==4:

        servidor = "Badner Mendiola" if st.session_state.no_vidente else "Jubelkys Morales"

        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", horas())

        if st.button("Confirmar cita"):
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

    # PASO 5 CONFIRMACION
    elif st.session_state.paso==5:
        st.success("CITA AGENDADA")
        voz("Cita registrada correctamente")

# =================================================
# ================= TRABAJADOR =====================
# =================================================
if menu=="Trabajador":

    st.title("Panel del trabajador")

    col1,col2 = st.columns(2)

    with col1:
        user = st.selectbox("Selecciona tu nombre", list(trabajadores.keys()))
    with col2:
        pw = st.text_input("Clave", type="password")

    if user in trabajadores and pw == trabajadores[user]:

        st.success(user)

        hoy = str(datetime.today().date())
        citas = [c for c in st.session_state.citas if c["trabajador"]==user and c["fecha"]==hoy]

        tiempos=[]
        finalizadas=0

        for i,c in enumerate(citas):

            st.markdown(f"<div class='card'>{c['cliente']}<br>{c['hora']}<br>{c['estado']}</div>", unsafe_allow_html=True)

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
                finalizadas+=1

        # KPI
        total=len(citas)
        cumplimiento=(finalizadas/total*100) if total>0 else 0
        promedio=(sum(tiempos)/len(tiempos)) if tiempos else 0

        st.subheader("KPI")
        st.metric("Cumplimiento", f"{cumplimiento:.1f}%")
        st.metric("Tiempo promedio", f"{promedio:.1f} min")

        # POST SERVICIO
        st.subheader("Evaluar post servicio")

        for c in citas:
            if c["estado"]=="Finalizada":
                c["calificacion"]=st.slider(f"{c['cliente']}",1,5)
