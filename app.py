import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
def init():
    defaults = {
        "paso": 1,
        "citas": [],
        "no_vidente": False
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ================= COLORES PASTEL =================
colores = {
    1:"#FFF4CC",  # amarillo pastel
    2:"#D6E9FF",  # azul pastel
    3:"#E6D6FF",  # morado pastel
    4:"#FFE5CC",  # naranja pastel
    5:"#D9F2D9"   # verde pastel
}

st.markdown(f"""
<style>
.stApp {{
    background-color: {colores[st.session_state.paso]};
}}
h1,h2,h3 {{
    font-family: 'Segoe UI';
    font-weight: 600;
}}
.big-button button {{
    width: 100%;
    height: 70px;
    font-size: 20px;
    border-radius: 10px;
}}
.card {{
    padding:15px;
    border-radius:12px;
    background:#ffffff;
    margin-bottom:10px;
    box-shadow:0px 2px 6px rgba(0,0,0,0.1);
}}
</style>
""", unsafe_allow_html=True)

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas":{
        "servidor":"SERVIDOR JUBELKYS",
        "detalle":["Ahorro","Corriente","Empresarial","Estudiantil"]
    },
    "Solicitud de créditos":{
        "servidor":"SERVIDOR MOISES",
        "detalle":["Personal","Hipotecario","Vehículo","Empresarial"]
    },
    "Consultas / Problemas":{
        "servidor":"SERVIDOR ADRIANA",
        "detalle":["Tarjetas","Transferencias","Intereses","Banca digital"]
    },
    "Asesoría bancaria":{
        "servidor":"SERVIDOR STEFANY",
        "detalle":["Plan ahorro","Estado cuenta","Créditos","Hipotecas"]
    },
    "Actualización de información":{
        "servidor":"SERVIDOR ANA",
        "detalle":["Datos","Cambio cuenta","Clausura"]
    }
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

    # PASO 1
    if st.session_state.paso==1:
        st.header("Datos personales")

        col1,col2 = st.columns(2)
        with col1:
            n1=st.text_input("Primer nombre")
            ced=st.text_input("Cédula")
            tel=st.text_input("Teléfono")
        with col2:
            n2=st.text_input("Segundo nombre")
            mail=st.text_input("Correo")

        st.session_state.no_vidente=st.checkbox("Persona no vidente")

        if st.button("Continuar"):
            if not all([n1,n2,ced,tel,mail]):
                st.error("Complete todos los campos")
            else:
                st.session_state.nombre=n1+" "+n2
                st.session_state.cedula=ced
                st.session_state.telefono=tel
                st.session_state.mail=mail
                st.session_state.paso=2

    # PASO 2
    elif st.session_state.paso==2:
        st.header("Seleccione el servicio")

        for s in servicios:
            st.markdown("<div class='big-button'>", unsafe_allow_html=True)
            if st.button(s):
                st.session_state.servicio=s
                st.session_state.paso=3
            st.markdown("</div>", unsafe_allow_html=True)

    # PASO 3
    elif st.session_state.paso==3:
        st.header("Seleccione detalle del servicio")

        for d in servicios[st.session_state.servicio]["detalle"]:
            st.markdown("<div class='big-button'>", unsafe_allow_html=True)
            if st.button(d):
                st.session_state.detalle=d
                st.session_state.paso=4
            st.markdown("</div>", unsafe_allow_html=True)

    # PASO 4
    elif st.session_state.paso==4:
        st.header("Agendar cita")

        servidor = "SERVIDOR BADNER" if st.session_state.no_vidente else servicios[st.session_state.servicio]["servidor"]

        st.info(f"Asignado a {servidor}")

        fecha=st.date_input("Fecha")
        ocupados=[c["hora"] for c in st.session_state.citas if c["fecha"]==str(fecha)]
        disp=[h for h in horas() if h not in ocupados]

        hora=st.selectbox("Hora",disp)

        if st.button("Confirmar cita"):
            st.session_state.citas.append({
                "cliente":st.session_state.nombre,
                "cedula":st.session_state.cedula,
                "telefono":st.session_state.telefono,
                "correo":st.session_state.mail,
                "servicio":st.session_state.servicio,
                "detalle":st.session_state.detalle,
                "trabajador":servidor,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Agendada"
            })
            st.session_state.paso=5

    # PASO 5
    elif st.session_state.paso==5:
        st.success("Cita agendada correctamente")
        if st.button("Nueva cita"):
            st.session_state.paso=1

# =================================================
# ================= TRABAJADOR =====================
# =================================================
if menu=="Trabajador":

    st.header("Panel del trabajador")

    user=st.text_input("Usuario")
    pw=st.text_input("Contraseña",type="password")

    user=user.capitalize()

    usuarios={
        "Jubelkys":"1111",
        "Moises":"2222",
        "Adriana":"3333",
        "Stefany":"4444",
        "Ana":"5555",
        "Badner":"6666"
    }

    nombres={
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA",
        "Badner":"SERVIDOR BADNER"
    }

    if user in usuarios and pw==usuarios[user]:

        servidor=nombres[user]
        st.success(servidor)

        fecha=st.date_input("Seleccione día", datetime.today())

        citas=[c for c in st.session_state.citas if c["trabajador"]==servidor and c["fecha"]==str(fecha)]

        st.subheader("Citas asignadas")

        for i,c in enumerate(citas):
            st.markdown(f"""
            <div class='card'>
            <b>Cliente:</b> {c['cliente']}<br>
            <b>Cédula:</b> {c['cedula']}<br>
            <b>Teléfono:</b> {c['telefono']}<br>
            <b>Correo:</b> {c['correo']}<br>
            <b>Servicio:</b> {c['servicio']}<br>
            <b>Detalle:</b> {c['detalle']}<br>
            <b>Hora:</b> {c['hora']}<br>
            <b>Estado:</b> {c['estado']}
            </div>
            """, unsafe_allow_html=True)

            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"Iniciar {i}"):
                    c["estado"]="En proceso"

            with col2:
                if st.button(f"Finalizar {i}"):
                    c["estado"]="Finalizada"
                    st.success("Cita finalizada")

    else:
        st.warning("Credenciales inválidas")
