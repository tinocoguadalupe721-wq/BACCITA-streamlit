import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= COLORES =================
AZUL = "#EEF4FF"
VERDE = "#DFF5E1"
fondo = VERDE if st.session_state.paso == 5 else AZUL

# ================= ESTILOS =================
st.markdown(f"""
<style>
.stApp {{
    background-color: {fondo};
    font-family: 'Segoe UI', sans-serif;
}}

h1, h2, h3 {{
    text-align:center;
}}

.card {{
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
    margin:10px;
}}

.btn button {{
    width:100%;
    height:70px;
    font-size:18px;
    border-radius:10px;
}}

.step {{
    display:flex;
    justify-content:center;
    gap:10px;
    margin-bottom:20px;
}}

.step div {{
    padding:10px 20px;
    border-radius:20px;
    background:#ddd;
}}

.active {{
    background:#4A90E2;
    color:white;
}}

.float {{
    position:fixed;
    right:20px;
    bottom:20px;
    font-size:30px;
    animation: float 2s infinite alternate;
}}

@keyframes float {{
    from {{transform:translateY(0px);}}
    to {{transform:translateY(-10px);}}
}}

.logo {{
    width:180px;
    display:block;
    margin:auto;
}}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.markdown("<img src='https://upload.wikimedia.org/wikipedia/commons/5/5a/BAC_Credomatic_logo.png' class='logo'>", unsafe_allow_html=True)

# ================= PASOS =================
def pasos(p):
    html = "<div class='step'>"
    for i in range(1,6):
        clase = "active" if i==p else ""
        html += f"<div class='{clase}'>Paso {i}</div>"
    html += "</div>"
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

menu = st.sidebar.selectbox("Modo",["Cliente","Trabajador"])

# =================================================
# ================= CLIENTE ========================
# =================================================
if menu=="Cliente":

    st.title("BAC CITA – ASESOR DE AGENDAS")
    pasos(st.session_state.paso)

    # PASO 1
    if st.session_state.paso==1:
        with st.form("datos"):
            st.subheader("Datos personales")

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

    # PASO 2 (SERVICIOS BONITOS)
    elif st.session_state.paso==2:
        st.subheader("Seleccione el servicio")

        cols = st.columns(2)

        i = 0
        for s in servicios:
            with cols[i % 2]:
                if st.button(s, use_container_width=True):
                    st.session_state.servicio = s
                    st.session_state.paso = 3
                    st.rerun()
            i += 1

    # PASO 3 (SUBSERVICIO LIMPIO)
    elif st.session_state.paso==3:
        st.subheader(f"Servicio seleccionado: {st.session_state.servicio}")

        opcion = st.radio(
            "Seleccione el tipo de atención",
            servicios[st.session_state.servicio],
            index=None
        )

        if opcion:
            st.session_state.detalle = opcion
            st.success(f"Seleccionado: {opcion}")

            if st.button("Continuar"):
                st.session_state.paso = 4
                st.rerun()

    # PASO 4
    elif st.session_state.paso==4:

        servidor = trabajadores[st.session_state.servicio]

        st.markdown(f"""
        <div class='card'>
        <h2>Será atendido por</h2>
        <h1>{servidor}</h1>
        </div>
        """, unsafe_allow_html=True)

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
            st.markdown(f"""
            <div class='card'>
            <h3>{c['cliente']}</h3>
            <b>{c['servicio']}</b><br>
            {c['detalle']}<br>
            {c['hora']}<br>
            Estado: {c['estado']}
            </div>
            """, unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            if col1.button(f"Iniciar {i}"):
                c["estado"]="En proceso"

            if col2.button(f"Finalizar {i}"):
                c["estado"]="Finalizada"
                st.success("Finalizada")

    else:
        st.warning("Ingrese credenciales válidas")

# ================= ICONO FLOTANTE =================
st.markdown("<div class='float'>➤</div>", unsafe_allow_html=True)
