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

# ================= COLORES =================
AZUL = "#F4F8FF"
VERDE = "#DFF5E1"
fondo = VERDE if st.session_state.paso == 5 else AZUL

# ================= ESTILOS =================
st.markdown(f"""
<style>
.stApp {{
    background: {fondo};
    font-family: 'Segoe UI';
}}

.grid {{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:15px;
}}

.card-btn button {{
    width:100%;
    height:90px;
    font-size:18px;
    border-radius:12px;
}}

.card {{
    background:white;
    padding:25px;
    border-radius:15px;
    text-align:center;
    box-shadow:0px 5px 15px rgba(0,0,0,0.1);
}}

.float {{
    position:fixed;
    bottom:30px;
    right:30px;
    font-size:40px;
    animation: fly 3s linear infinite;
}}

@keyframes fly {{
    0% {{transform:translateX(0);}}
    100% {{transform:translateX(-300px);}}
}}

.logo {{
    width:160px;
    display:block;
    margin:auto;
}}
</style>
""", unsafe_allow_html=True)

# ================= VOZ REAL =================
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
st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/5/5a/BAC_Credomatic_logo.png' class='logo'>", unsafe_allow_html=True)

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas":["Ahorro","Corriente","Empresarial","Estudiantil"],
    "Solicitud de créditos":["Personal","Hipotecario","Vehículo","Empresarial"],
    "Consultas":["Tarjetas","Transferencias","Intereses","Banca digital"],
    "Asesoría":["Plan ahorro","Estado cuenta","Créditos","Hipotecas"],
    "Actualización":["Datos","Cambio cuenta","Clausura"]
}

trabajadores = {
    "Apertura de cuentas":"SERVIDOR JUBELKYS",
    "Solicitud de créditos":"SERVIDOR MOISES",
    "Consultas":"SERVIDOR ADRIANA",
    "Asesoría":"SERVIDOR STEFANY",
    "Actualización":"SERVIDOR ANA"
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

    st.title("BAC CITA – ASESOR BANCARIO")

    # PASO 1
    if st.session_state.paso==1:

        st.session_state.no_vidente = st.checkbox("No vidente")

        voz("Hola soy tu asesor bancario. Por favor deletrea tu primer nombre")

        with st.form("datos"):
            n1 = st.text_input("Primer nombre")
            n2 = st.text_input("Segundo nombre")
            ced = st.text_input("Cédula")
            tel = st.text_input("Teléfono")
            mail = st.text_input("Correo")

            ok = st.form_submit_button("Continuar")

            if ok:
                if n1 and n2 and ced and tel and mail:
                    st.session_state.nombre = n1+" "+n2
                    st.session_state.paso=2
                    st.rerun()
                else:
                    st.error("Complete todos los campos")

    # PASO 2
    elif st.session_state.paso==2:

        st.subheader("Seleccione servicio")

        cols = st.columns(2)
        i=0
        for s in servicios:
            with cols[i%2]:
                if st.button(s, key=s, use_container_width=True):
                    st.session_state.servicio=s
                    st.session_state.paso=3
                    st.rerun()
            i+=1

    # PASO 3
    elif st.session_state.paso==3:

        st.subheader("Seleccione subservicio")

        cols = st.columns(2)
        i=0
        for sub in servicios[st.session_state.servicio]:
            with cols[i%2]:
                if st.button(sub, key=sub, use_container_width=True):
                    st.session_state.detalle=sub
                    st.session_state.paso=4
                    st.rerun()
            i+=1

    # PASO 4
    elif st.session_state.paso==4:

        servidor = trabajadores[st.session_state.servicio]

        voz(f"Tu cita será atendida por {servidor}")

        st.markdown(f"<div class='card'><h2>{servidor}</h2></div>", unsafe_allow_html=True)

        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", horas())

        if st.button("CONFIRMAR CITA"):
            st.session_state.citas.append({
                "cliente":st.session_state.nombre,
                "servicio":st.session_state.servicio,
                "detalle":st.session_state.detalle,
                "trabajador":servidor,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Agendada"
            })

            voz(f"Tu cita está agendada para {fecha} a las {hora}")

            st.session_state.paso=5
            st.rerun()

    # PASO 5
    elif st.session_state.paso==5:
        st.success("CITA AGENDADA EXITOSA")

        if st.button("Nueva cita"):
            st.session_state.paso=1
            st.rerun()

# =================================================
# ================= TRABAJADOR =====================
# =================================================
if menu=="Trabajador":

    st.header("Panel de atención")

    usuarios = {
        "Jubelkys":"1111",
        "Moises":"2222",
        "Adriana":"3333",
        "Stefany":"4444",
        "Ana":"5555"
    }

    nombres = {
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA"
    }

    user = st.text_input("Usuario")
    pw = st.text_input("Contraseña", type="password")

    if user in usuarios and pw == usuarios[user]:

        servidor = nombres[user]
        st.success(servidor)

        fecha = st.date_input("Día", datetime.today())

        citas = [c for c in st.session_state.citas if c["trabajador"]==servidor and c["fecha"]==str(fecha)]

        for i,c in enumerate(citas):
            st.markdown(f"<div class='card'>{c['cliente']}<br>{c['hora']}<br>{c['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"Iniciar {i}"):
                c["estado"]="En proceso"

            if col2.button(f"Finalizar {i}"):
                c["estado"]="Finalizada"

# ================= ICONO ANIMADO =================
st.markdown("<div class='float'>✈</div>", unsafe_allow_html=True)
