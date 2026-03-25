import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= CONTROL DE PASOS =================
if "paso" not in st.session_state:
    st.session_state.paso = 1

if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= COLORES POR PASO =================
colores_pasos = {
    1: "#FFD700",   # amarillo
    2: "#4da6ff",   # azul
    3: "#cc99ff",   # morado
    4: "#66cc66"    # verde final
}

color_actual = colores_pasos.get(st.session_state.paso, "#FFFFFF")

st.markdown(f"""
<style>
body {{
    background-color: {color_actual};
}}
</style>
""", unsafe_allow_html=True)

st.title("Sistema Bancario de Gestión de Citas")

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas": "SERVIDOR JUBELKYS",
    "Solicitud de créditos": "SERVIDOR MOISES",
    "Consultas / Problemas": "SERVIDOR ADRIANA",
    "Asesoría bancaria": "SERVIDOR STEFANY",
    "Actualización de información": "SERVIDOR ANA"
}

# ================= VOZ =================
def hablar(texto):
    st.markdown(f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{texto}");
    window.speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)

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

    st.header("Proceso de Agendamiento")

    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Número de cédula")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Teléfono")

    accesibilidad = st.checkbox("Soy persona no vidente")

    if accesibilidad:
        hablar("Bienvenido. Seleccione el servicio que desea.")

    # ================= PASO 1 =================
    if st.session_state.paso == 1:
        st.subheader("Seleccione el servicio")

        for s in servicios:
            if st.button(s):
                st.session_state.servicio = s
                st.session_state.paso = 2

    # ================= PASO 2 =================
    elif st.session_state.paso == 2:
        st.subheader("Seleccione el tipo de servicio")

        servicio_sel = st.session_state.servicio

        if servicio_sel == "Apertura de cuentas":
            opciones = ["Ahorro","Corriente","Empresarial","Estudiantil"]
        elif servicio_sel == "Solicitud de créditos":
            opciones = ["Personal","Hipotecario","Vehículo","Empresarial"]
        elif servicio_sel == "Consultas / Problemas":
            opciones = ["Tarjetas","Transferencias","Intereses","Banca digital"]
        elif servicio_sel == "Asesoría bancaria":
            opciones = ["Ahorro","Estado de cuenta","Créditos","Hipotecas"]
        else:
            opciones = ["Datos","Cambio de cuenta","Clausura"]

        detalle = st.radio("Opciones disponibles", opciones)

        if st.button("Continuar"):
            st.session_state.detalle = detalle
            st.session_state.paso = 3

    # ================= PASO 3 =================
    elif st.session_state.paso == 3:
        st.subheader("Agendamiento de cita")

        servidor = servicios[st.session_state.servicio]
        st.info(f"Será atendido por: {servidor}")

        fecha = st.date_input("Seleccione fecha")

        ocupados = [c["hora"] for c in st.session_state.citas if c["fecha"] == str(fecha)]
        disponibles = [h for h in generar_horas() if h not in ocupados]

        hora = st.selectbox("Horario disponible", disponibles)

        if st.button("Confirmar cita"):
            st.session_state.citas.append({
                "cliente": nombre,
                "cedula": cedula,
                "correo": correo,
                "telefono": telefono,
                "servicio": st.session_state.servicio,
                "detalle": st.session_state.detalle,
                "trabajador": servidor,
                "fecha": str(fecha),
                "hora": hora,
                "estado": "Agendada",
                "evaluacion": None
            })
            st.session_state.paso = 4

    # ================= PASO 4 =================
    elif st.session_state.paso == 4:
        st.success("Cita confirmada correctamente")
        st.write("El proceso ha finalizado exitosamente")

        if accesibilidad:
            hablar("Su cita ha sido confirmada correctamente")

        if st.button("Nueva cita"):
            st.session_state.paso = 1

    # ================= ESTADO =================
    st.subheader("Estado de citas")

    for c in st.session_state.citas:
        if c["cliente"] == nombre:
            color = "green" if c["estado"] == "Agendada" else "red"
            st.markdown(f"<p style='color:{color}'>{c['servicio']} - {c['estado']}</p>", unsafe_allow_html=True)

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
        "Ana":"1238"
    }

    nombres = {
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA"
    }

    if usuario in usuarios and password == "1234":

        st.success(f"Bienvenido {nombres[usuario]}")

        # FOTO
        foto = st.file_uploader("subir fotografia")
        if foto:
            st.image(foto, width=150)

        citas = [c for c in st.session_state.citas if c["trabajador"] == nombres[usuario]]

        for i, c in enumerate(citas):
            st.markdown("---")
            st.write(c["cliente"], c["fecha"], c["hora"], c["servicio"])
            st.write("Estado:", c["estado"])

            if c["estado"] == "Agendada":
                if st.button(f"Iniciar {i}"):
                    c["estado"] = "En proceso"

            elif c["estado"] == "En proceso":
                if st.button(f"Finalizar {i}"):
                    c["estado"] = "Finalizada"
                    st.success("Encuesta enviada al cliente")

    else:
        st.warning("Credenciales incorrectas")
