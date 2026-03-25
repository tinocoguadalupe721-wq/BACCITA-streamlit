import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= COLORES =================
rojo = "#FAD4D4"
verde = "#D9F2D9"
color = verde if st.session_state.paso == 5 else rojo

# ================= ESTILOS =================
st.markdown(f"""
<style>
.stApp {{
    background-color: {color};
    text-align:center;
}}

h1,h2,h3 {{
    text-align:center;
}}

.big button {{
    width:100%;
    height:80px;
    font-size:22px;
    border-radius:12px;
}}

.card {{
    padding:20px;
    border-radius:12px;
    background:white;
    margin:10px;
}}

.arrow {{
    font-size:30px;
    animation: move 1s infinite alternate;
}}

@keyframes move {{
    from {{transform:translateX(0px);}}
    to {{transform:translateX(10px);}}
}}

.logo {{
    width:180px;
    margin:auto;
    display:block;
}}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/5/5a/BAC_Credomatic_logo.png' class='logo'>", unsafe_allow_html=True)

# ================= STEPS =================
def steps(p):
    html="<div style='display:flex;justify-content:center;'>"
    for i in range(1,6):
        color = "#66cc99" if i==p else "#ddd"
        html += f"<div style='padding:10px 20px;margin:5px;background:{color};border-radius:20px;'>Paso {i}</div>"
        if i<5:
            html += "<div class='arrow'>➜</div>"
    html+="</div>"
    st.markdown(html, unsafe_allow_html=True)

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas":["Ahorro","Corriente","Empresarial","Estudiantil"],
    "Solicitud de créditos":["Personal","Hipotecario","Vehículo","Empresarial"],
    "Consultas / Problemas":["Tarjetas","Transferencias","Intereses","Banca digital"],
    "Asesoría bancaria":["Plan ahorro","Estado cuenta","Créditos","Hipotecas"],
    "Actualización de información":["Datos","Cambio cuenta","Clausura"]
}

trabajadores = {
    "Apertura de cuentas":"SERVIDOR JUBELKYS",
    "Solicitud de créditos":"SERVIDOR MOISES",
    "Consultas / Problemas":"SERVIDOR ADRIANA",
    "Asesoría bancaria":"SERVIDOR STEFANY",
    "Actualización de información":"SERVIDOR ANA"
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

menu = st.sidebar.selectbox("Menú",["Cliente","Trabajador"])

# =================================================
# ================= CLIENTE ========================
# =================================================
if menu=="Cliente":

    st.title("BAC CITA TU ASESOR DE AGENDAS BANCARIAS")
    steps(st.session_state.paso)

    # ===== PASO 1 =====
    if st.session_state.paso==1:

        with st.form("datos"):
            st.header("Ingrese sus datos")

            n1 = st.text_input("Primer nombre")
            n2 = st.text_input("Segundo nombre")
            ced = st.text_input("Cédula")
            tel = st.text_input("Teléfono")
            mail = st.text_input("Correo")

            ok = st.form_submit_button("Continuar")

            if ok:
                if n1 and n2 and ced and tel and mail:
                    st.session_state.nombre = n1+" "+n2
                    st.session_state.cedula = ced
                    st.session_state.telefono = tel
                    st.session_state.mail = mail
                    st.session_state.paso = 2
                    st.rerun()
                else:
                    st.error("Complete todos los campos")

    # ===== PASO 2 =====
    elif st.session_state.paso==2:

        st.header("Seleccione servicio")

        for s in servicios:
            st.markdown("<div class='big'>", unsafe_allow_html=True)
            if st.button(f"📌 {s}"):
                st.session_state.servicio=s
                st.session_state.paso=3
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ===== PASO 3 =====
    elif st.session_state.paso==3:

        st.header("Seleccione subservicio")

        for d in servicios[st.session_state.servicio]:
            st.markdown("<div class='big'>", unsafe_allow_html=True)
            if st.button(f"➡ {d}"):
                st.session_state.detalle=d
                st.session_state.paso=4
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # ===== PASO 4 =====
    elif st.session_state.paso==4:

        servidor = trabajadores[st.session_state.servicio]

        st.markdown(f"<h2>Será atendido por:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1>{servidor}</h1>", unsafe_allow_html=True)

        fecha = st.date_input("Seleccione fecha")
        hora = st.selectbox("Seleccione hora", horas())

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
            st.session_state.paso=5
            st.rerun()

    # ===== PASO 5 =====
    elif st.session_state.paso==5:

        st.markdown("<h1>CITA AGENDADA EXITOSA</h1>", unsafe_allow_html=True)

        if st.button("AGENDAR OTRA"):
            st.session_state.paso=1
            st.rerun()

# =================================================
# ================= TRABAJADOR =====================
# =================================================
if menu=="Trabajador":

    st.header("Panel del trabajador")

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

        fecha = st.date_input("Seleccione día", datetime.today())

        citas = [c for c in st.session_state.citas if c["trabajador"]==servidor and c["fecha"]==str(fecha)]

        for i,c in enumerate(citas):
            st.markdown(f"""
            <div class='card'>
            <h3>{c['cliente']}</h3>
            Servicio: {c['servicio']}<br>
            Detalle: {c['detalle']}<br>
            Hora: {c['hora']}<br>
            Estado: {c['estado']}
            </div>
            """, unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"Iniciar {i}"):
                c["estado"]="En proceso"

            if col2.button(f"Finalizar {i}"):
                c["estado"]="Finalizada"
                st.success("Cita finalizada")

    else:
        st.warning("Ingrese credenciales válidas")
