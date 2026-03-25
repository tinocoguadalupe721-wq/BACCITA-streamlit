import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTADO =================
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= COLORES POR STEP =================
colores = {
    1: "#FFD700",  # amarillo (datos)
    2: "#4da6ff",  # azul (servicio)
    3: "#cc99ff",  # morado (detalle)
    4: "#ff6666",  # rojo (agenda)
    5: "#66cc66"   # verde (confirmación)
}

color_actual = colores.get(st.session_state.paso, "#FFFFFF")

st.markdown(f"""
<style>
.stApp {{
    background-color: {color_actual};
}}
.boton {{
    padding:10px;
    border-radius:8px;
    margin:5px;
    font-weight:bold;
}}
</style>
""", unsafe_allow_html=True)

st.title("Bienvenido a BAC CITA TU ASESOR DE AGENDAS BANCARIAS")

# ================= VOZ =================
def hablar(texto):
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{texto}");
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

def sonido_click():
    st.markdown("""
    <script>
    var audio = new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3");
    audio.play();
    </script>
    """, unsafe_allow_html=True)

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas": "SERVIDOR JUBELKYS",
    "Solicitud de créditos": "SERVIDOR MOISES",
    "Consultas / Problemas": "SERVIDOR ADRIANA",
    "Asesoría bancaria": "SERVIDOR STEFANY",
    "Actualización de información": "SERVIDOR ANA"
}

# ================= HORARIOS =================
def generar_horas():
    horas = []
    h = datetime.combine(datetime.today(), time(8,0))
    fin = datetime.combine(datetime.today(), time(17,0))
    while h + timedelta(minutes=35) <= fin:
        horas.append(h.strftime("%H:%M"))
        h += timedelta(minutes=35)
    return horas

menu = st.sidebar.selectbox("Menú", ["Cliente","Trabajador"])

# ================= CLIENTE =================
if menu == "Cliente":

    # ================= PASO 1 =================
    if st.session_state.paso == 1:
        st.header("Datos personales")

        nombre1 = st.text_input("Primer nombre")
        nombre2 = st.text_input("Segundo nombre")
        cedula = st.text_input("Número de cédula")
        correo = st.text_input("Correo electrónico")
        telefono = st.text_input("Teléfono")

        no_vidente = st.checkbox("Persona no vidente")

        if no_vidente:
            hablar("Hola, soy tu asesor bancario")
            hablar("Por favor deletrea tu primer nombre")

        if st.button("Continuar"):
            if not all([nombre1, nombre2, cedula, correo, telefono]):
                st.error("Debe completar todos los campos para continuar")
            else:
                st.session_state.nombre = nombre1 + " " + nombre2
                st.session_state.cedula = cedula
                st.session_state.correo = correo
                st.session_state.telefono = telefono
                st.session_state.no_vidente = no_vidente
                st.session_state.paso = 2

    # ================= PASO 2 =================
    elif st.session_state.paso == 2:
        st.header("Seleccione el servicio")

        for s in servicios:
            if st.button(s):
                st.session_state.servicio = s
                st.session_state.paso = 3

    # ================= PASO 3 =================
    elif st.session_state.paso == 3:
        st.header("Seleccione el detalle del servicio")

        s = st.session_state.servicio

        if s == "Apertura de cuentas":
            opciones = ["Ahorro","Corriente","Empresarial","Estudiantil"]
        elif s == "Solicitud de créditos":
            opciones = ["Personal","Hipotecario","Vehículo","Empresarial"]
        elif s == "Consultas / Problemas":
            opciones = ["Tarjetas","Transferencias","Intereses","Banca digital"]
        elif s == "Asesoría bancaria":
            opciones = ["Ahorro","Estado de cuenta","Créditos","Hipotecas"]
        else:
            opciones = ["Datos","Cambio de cuenta","Clausura"]

        detalle = st.radio("Opciones", opciones)

        if st.button("Continuar"):
            st.session_state.detalle = detalle
            st.session_state.paso = 4

    # ================= PASO 4 =================
    elif st.session_state.paso == 4:
        st.header("Agendar cita")

        if st.session_state.no_vidente:
            servidor = "SERVIDOR BADNER"
        else:
            servidor = servicios[st.session_state.servicio]

        st.info(f"Atención asignada a: {servidor}")

        fecha = st.date_input("Fecha")

        ocupados = [c["hora"] for c in st.session_state.citas if c["fecha"] == str(fecha)]
        disponibles = [h for h in generar_horas() if h not in ocupados]

        hora = st.selectbox("Hora", disponibles)

        if st.button("Confirmar cita"):
            st.session_state.citas.append({
                "cliente": st.session_state.nombre,
                "cedula": st.session_state.cedula,
                "correo": st.session_state.correo,
                "telefono": st.session_state.telefono,
                "servicio": st.session_state.servicio,
                "detalle": st.session_state.detalle,
                "trabajador": servidor,
                "fecha": str(fecha),
                "hora": hora,
                "estado": "Agendada"
            })

            st.session_state.paso = 5

            if st.session_state.no_vidente:
                hablar("Tu cita está agendada para " + str(fecha) + " a las " + hora)
                hablar("Será agendado por servidor Badner")

    # ================= PASO 5 =================
    elif st.session_state.paso == 5:
        st.success("Cita agendada exitosa")
        sonido_click()

        st.markdown("""
        <h1 style='text-align:center;'>CONFIRMACIÓN COMPLETA</h1>
        """, unsafe_allow_html=True)

        if st.button("Agendar nueva cita"):
            st.session_state.paso = 1

# ================= TRABAJADOR =================
if menu == "Trabajador":

    st.header("Panel del trabajador")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    usuario = usuario.capitalize()

    usuarios = {
        "Jubelkys":"1234",
        "Moises":"1235",
        "Adriana":"1236",
        "Stefany":"1237",
        "Ana":"1238",
        "Badner":"1239"
    }

    nombres = {
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA",
        "Badner":"SERVIDOR BADNER"
    }

    if usuario in usuarios and password == "1234":
        st.success(f"Bienvenido {nombres[usuario]}")

        foto = st.file_uploader("Cargar fotografía")
        if foto:
            st.image(foto, width=150)

        citas = [c for c in st.session_state.citas if c["trabajador"] == nombres[usuario]]

        for i, c in enumerate(citas):
            st.markdown("---")
            st.write(c["cliente"], c["fecha"], c["hora"], c["servicio"])
            st.write("Estado:", c["estado"])

            if st.button(f"Iniciar {i}"):
                c["estado"] = "En proceso"

            if st.button(f"Finalizar {i}"):
                c["estado"] = "Finalizada"
                st.success("Atención finalizada")

    else:
        st.warning("Credenciales inválidas")
