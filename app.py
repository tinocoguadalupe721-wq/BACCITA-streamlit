import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO GLOBAL =================
def init():
    defaults = {
        "paso": 1,
        "citas": [],
        "no_vidente": False,
        "evaluaciones": [],
        "evaluar_cita": None
    }
    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()

# ================= COLORES =================
colores = {
    1:"#FFD700",   # amarillo
    2:"#4da6ff",   # azul
    3:"#b366ff",   # morado
    4:"#ffb84d",   # naranja
    5:"#66cc66"    # verde
}

st.markdown(f"<style>.stApp{{background:{colores[st.session_state.paso]};}}</style>", unsafe_allow_html=True)

# ================= VOZ =================
def hablar(texto):
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{texto}");
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

# ================= SONIDO =================
def sonido():
    st.markdown("""
    <script>
    new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3").play();
    </script>
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

# =========================================================
# ======================= CLIENTE ==========================
# =========================================================
if menu=="Cliente":

    st.title("BAC CITA TU ASESOR DE AGENDAS BANCARIAS")

    # ===== PASO 1 =====
    if st.session_state.paso==1:
        st.header("Datos personales")

        n1=st.text_input("Primer nombre")
        n2=st.text_input("Segundo nombre")
        ced=st.text_input("Cédula")
        tel=st.text_input("Teléfono")
        mail=st.text_input("Correo")

        st.session_state.no_vidente=st.checkbox("Persona no vidente")

        if st.session_state.no_vidente:
            hablar("Hola soy tu asesor bancario")
            hablar("Por favor deletrea tu primer nombre")

        if st.button("Continuar"):
            if not all([n1,n2,ced,tel,mail]):
                st.error("Debe completar todos los campos")
            else:
                st.session_state.nombre=n1+" "+n2
                st.session_state.cedula=ced
                st.session_state.telefono=tel
                st.session_state.mail=mail
                st.session_state.paso=2

    # ===== PASO 2 =====
    elif st.session_state.paso==2:
        st.header("Seleccione el servicio")

        for s in servicios:
            if st.button(s):
                st.session_state.servicio=s
                st.session_state.paso=3

    # ===== PASO 3 =====
    elif st.session_state.paso==3:
        st.header("Detalle del servicio")

        opciones=servicios[st.session_state.servicio]["detalle"]
        d=st.radio("Opciones",opciones)

        if st.button("Continuar"):
            st.session_state.detalle=d
            st.session_state.paso=4

    # ===== PASO 4 =====
    elif st.session_state.paso==4:
        st.header("Agenda")

        if st.session_state.no_vidente:
            servidor="SERVIDOR BADNER"
        else:
            servidor=servicios[st.session_state.servicio]["servidor"]

        st.info(f"Asignado a {servidor}")

        fecha=st.date_input("Fecha")

        ocupados=[c["hora"] for c in st.session_state.citas if c["fecha"]==str(fecha)]
        disponibles=[h for h in horas() if h not in ocupados]

        hora=st.selectbox("Hora disponible",disponibles)

        if st.button("Confirmar cita"):
            cita = {
                "cliente":st.session_state.nombre,
                "servicio":st.session_state.servicio,
                "detalle":st.session_state.detalle,
                "trabajador":servidor,
                "fecha":str(fecha),
                "hora":hora,
                "estado":"Agendada",
                "evaluada":False,
                "calificacion":None
            }

            st.session_state.citas.append(cita)
            st.session_state.paso=5

            if st.session_state.no_vidente:
                hablar(f"Tu cita está agendada para {fecha} a las {hora}")
                hablar("Será atendido por servidor Badner")

    # ===== PASO 5 =====
    elif st.session_state.paso==5:
        st.success("Cita agendada correctamente")
        sonido()

        st.header("Evaluación del servicio")

        # Mostrar evaluación SOLO si existe una cita finalizada sin evaluar
        citas_pendientes = [c for c in st.session_state.citas if c["estado"]=="Finalizada" and not c["evaluada"]]

        if citas_pendientes:
            cita_eval = citas_pendientes[-1]
            cal = st.slider("Califique el servicio",1,5)

            if st.button("Enviar evaluación"):
                cita_eval["evaluada"] = True
                cita_eval["calificacion"] = cal
                st.success("Evaluación registrada")

        if st.button("Nueva cita"):
            st.session_state.paso=1

# =========================================================
# ===================== TRABAJADOR =========================
# =========================================================
if menu=="Trabajador":

    st.header("Panel del trabajador")

    user=st.text_input("Usuario")
    pw=st.text_input("Contraseña",type="password")

    user=user.capitalize()

    usuarios={
        "Jubelkys":"1234",
        "Moises":"1234",
        "Adriana":"1234",
        "Stefany":"1234",
        "Ana":"1234",
        "Badner":"1234"
    }

    nombres={
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA",
        "Badner":"SERVIDOR BADNER"
    }

    if user in usuarios and pw=="1234":
        servidor=nombres[user]
        st.success(f"Bienvenido {servidor}")

        foto=st.file_uploader("Subir fotografía")
        if foto:
            st.image(foto,width=120)

        hoy=str(datetime.today().date())

        # 📌 SOLO CITAS DEL DÍA
        citas_hoy=[c for c in st.session_state.citas if c["trabajador"]==servidor and c["fecha"]==hoy]

        st.subheader("Agenda del día")

        if not citas_hoy:
            st.info("No tienes citas hoy")

        for i,c in enumerate(citas_hoy):
            st.markdown("---")
            st.write(f"Cliente: {c['cliente']}")
            st.write(f"Hora: {c['hora']}")
            st.write(f"Servicio: {c['servicio']}")
            st.write(f"Estado: {c['estado']}")

            if c["estado"]=="Agendada":
                if st.button(f"Iniciar atención {i}"):
                    c["estado"]="En proceso"

            elif c["estado"]=="En proceso":
                if st.button(f"Finalizar atención {i}"):
                    c["estado"]="Finalizada"
                    st.success("Cita finalizada - cliente puede evaluar")

        # 📊 PROMEDIO
        evaluadas=[c["calificacion"] for c in st.session_state.citas if c["trabajador"]==servidor and c["calificacion"]]
        if evaluadas:
            promedio=sum(evaluadas)/len(evaluadas)
            st.subheader(f"Promedio de evaluación: {round(promedio,2)}")

    else:
        st.warning("Credenciales inválidas")
