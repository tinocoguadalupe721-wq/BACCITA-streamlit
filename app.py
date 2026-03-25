import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= COLORES =================
rojo_pastel = "#FAD4D4"
verde_final = "#D9F2D9"

color_actual = verde_final if st.session_state.paso == 5 else rojo_pastel

st.markdown(f"""
<style>
.stApp {{
    background-color: {color_actual};
}}

.big-button button {{
    width:100%;
    height:70px;
    font-size:20px;
    border-radius:10px;
}}

.card {{
    padding:15px;
    border-radius:12px;
    background:white;
    margin-bottom:10px;
}}
</style>
""", unsafe_allow_html=True)

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

    # ===== PASO 1 (FORM) =====
    if st.session_state.paso==1:

        with st.form("form_datos"):
            st.header("Datos personales")

            n1 = st.text_input("Primer nombre")
            n2 = st.text_input("Segundo nombre")
            ced = st.text_input("Cédula")
            tel = st.text_input("Teléfono")
            mail = st.text_input("Correo")

            submit = st.form_submit_button("Continuar")

            if submit:
                if n1 and n2 and ced and tel and mail:
                    st.session_state.nombre = n1+" "+n2
                    st.session_state.cedula = ced
                    st.session_state.telefono = tel
                    st.session_state.mail = mail
                    st.session_state.paso = 2
                    st.rerun()
                else:
                    st.error("Completa todos los campos")

    # ===== PASO 2 =====
    elif st.session_state.paso==2:
        st.header("Seleccione servicio")

        for s in servicios:
            if st.button(s):
                st.session_state.servicio=s
                st.session_state.paso=3
                st.rerun()

    # ===== PASO 3 =====
    elif st.session_state.paso==3:
        st.header("Seleccione detalle")

        for d in servicios[st.session_state.servicio]:
            if st.button(d):
                st.session_state.detalle=d
                st.session_state.paso=4
                st.rerun()

    # ===== PASO 4 =====
    elif st.session_state.paso==4:
        st.header("Agendar cita")

        fecha = st.date_input("Fecha")
        hora = st.selectbox("Hora", horas())

        if st.button("Confirmar cita"):
            st.session_state.citas.append({
                "cliente":st.session_state.nombre,
                "servicio":st.session_state.servicio,
                "detalle":st.session_state.detalle,
                "trabajador":trabajadores[st.session_state.servicio],
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Agendada"
            })

            st.session_state.paso=5
            st.rerun()

    # ===== PASO 5 =====
    elif st.session_state.paso==5:
        st.success("CITA AGENDADA EXITOSA")

        if st.button("Nueva cita"):
            st.session_state.paso=1
            st.rerun()

# =================================================
# ================= TRABAJADOR =====================
# =================================================
if menu=="Trabajador":

    st.header("Panel trabajador")

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

        fecha = st.date_input("Seleccionar día", datetime.today())

        citas = [c for c in st.session_state.citas if c["trabajador"]==servidor and c["fecha"]==str(fecha)]

        for i,c in enumerate(citas):
            st.markdown(f"<div class='card'><b>{c['cliente']}</b><br>{c['hora']}<br>{c['estado']}</div>", unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"Iniciar {i}"):
                c["estado"]="En proceso"

            if col2.button(f"Finalizar {i}"):
                c["estado"]="Finalizada"
