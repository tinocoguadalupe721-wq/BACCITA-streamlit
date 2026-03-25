import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")

# ================= ESTILOS =================
st.markdown("""
<style>
.servicio {padding:12px; border-radius:8px; margin:6px; font-weight:bold; color:black;}
.amarillo {background-color:#FFD700;}
.azul {background-color:#4da6ff;}
.verde {background-color:#66cc66;}
.rojo {background-color:#ff6666;}
.morado {background-color:#cc99ff;}
.estado_ok {background-color:#66cc66; padding:8px; border-radius:6px;}
.estado_fail {background-color:#ff6666; padding:8px; border-radius:6px;}
</style>
""", unsafe_allow_html=True)

st.title("Sistema Bancario de Gestión de Citas")

# ================= BASE =================
if "citas" not in st.session_state:
    st.session_state.citas = []

# ================= SERVICIOS =================
servicios = {
    "Apertura de cuentas": {"color":"amarillo","servidor":"SERVIDOR JUBELKYS"},
    "Solicitud de créditos": {"color":"azul","servidor":"SERVIDOR MOISES"},
    "Consultas / Problemas": {"color":"rojo","servidor":"SERVIDOR ADRIANA"},
    "Asesoría bancaria": {"color":"verde","servidor":"SERVIDOR STEFANY"},
    "Actualización de información": {"color":"morado","servidor":"SERVIDOR ANA"}
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
    st.header("Registro y Agendamiento")

    nombre = st.text_input("Nombre completo")
    cedula = st.text_input("Número de cédula")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Número telefónico")

    st.subheader("Selección de servicio")

    for s in servicios:
        st.markdown(
            f"<div class='servicio {servicios[s]['color']}'>{s}</div>",
            unsafe_allow_html=True
        )

    servicio_sel = st.radio("Seleccione un servicio principal", list(servicios.keys()))

    # ================= DESGLOSE =================
    detalle = ""

    if servicio_sel == "Apertura de cuentas":
        detalle = st.selectbox("Tipo de cuenta", [
            "Cuenta de ahorro",
            "Cuenta corriente",
            "Cuenta empresarial",
            "Cuenta estudiantil"
        ])

    elif servicio_sel == "Solicitud de créditos":
        detalle = st.selectbox("Tipo de crédito", [
            "Crédito personal",
            "Crédito hipotecario",
            "Crédito de vehículo",
            "Crédito empresarial"
        ])

    elif servicio_sel == "Consultas / Problemas":
        detalle = st.selectbox("Tipo de consulta", [
            "Tarjetas",
            "Transferencias",
            "Intereses",
            "Banca digital"
        ])

    elif servicio_sel == "Asesoría bancaria":
        detalle = st.selectbox("Tipo de asesoría", [
            "Ahorro",
            "Estado de cuenta",
            "Créditos",
            "Hipotecas"
        ])

    elif servicio_sel == "Actualización de información":
        detalle = st.selectbox("Tipo de actualización", [
            "Datos personales",
            "Cambio de cuenta",
            "Clausura"
        ])

    servidor = servicios[servicio_sel]["servidor"]
    st.info(f"Asignación automática: {servidor}")

    fecha = st.date_input("Seleccione fecha")

    ocupados = [c["hora"] for c in st.session_state.citas if c["fecha"] == str(fecha)]
    disponibles = [h for h in generar_horas() if h not in ocupados]

    hora = st.selectbox("Seleccione horario disponible", disponibles)

    if st.button("Confirmar cita"):
        st.session_state.citas.append({
            "cliente": nombre,
            "cedula": cedula,
            "correo": correo,
            "telefono": telefono,
            "servicio": servicio_sel,
            "detalle": detalle,
            "trabajador": servidor,
            "fecha": str(fecha),
            "hora": hora,
            "estado": "Agendada",
            "evaluacion": None
        })
        st.success("La cita ha sido registrada correctamente")

    # ================= ESTADO =================
    st.subheader("Estado de citas")
    for c in st.session_state.citas:
        if c["cliente"] == nombre:
            if c["estado"] == "Agendada":
                st.markdown(f"<div class='estado_ok'>{c['servicio']} - {c['estado']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='estado_fail'>{c['servicio']} - {c['estado']}</div>", unsafe_allow_html=True)

    # ================= ENCUESTA =================
    st.subheader("Evaluación del servicio")

    for i, c in enumerate(st.session_state.citas):
        if c["cliente"] == nombre and c["estado"] == "Finalizada" and c["evaluacion"] is None:
            valor = st.slider(f"Califique el servicio recibido ({c['servicio']})", 1, 5)
            if st.button(f"Enviar evaluación {i}"):
                c["evaluacion"] = valor
                st.success("Evaluación registrada")

# ================= TRABAJADOR =================
if menu == "Trabajador":
    st.header("Panel del trabajador")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # NORMALIZA MAYÚSCULA INICIAL
    usuario = usuario.capitalize()

    usuarios = {
        "Jubelkys":"1234",
        "Moises":"1234",
        "Adriana":"1234",
        "Stefany":"1234",
        "Ana":"1234"
    }

    nombres = {
        "Jubelkys":"SERVIDOR JUBELKYS",
        "Moises":"SERVIDOR MOISES",
        "Adriana":"SERVIDOR ADRIANA",
        "Stefany":"SERVIDOR STEFANY",
        "Ana":"SERVIDOR ANA"
    }

    if usuario in usuarios and password == "1234":
        st.success(f"Acceso concedido: {nombres[usuario]}")

        foto = st.file_uploader("Cargar fotografía del trabajador")
        if foto:
            st.image(foto, width=150)

        citas = [c for c in st.session_state.citas if c["trabajador"] == nombres[usuario]]

        evaluaciones = [c["evaluacion"] for c in citas if c["evaluacion"]]
        if evaluaciones:
            promedio = sum(evaluaciones) / len(evaluaciones)
            st.metric("Promedio de evaluación", round(promedio, 2))

        for i, c in enumerate(citas):
            st.markdown("---")
            st.write("Cliente:", c["cliente"])
            st.write("Fecha:", c["fecha"], "Hora:", c["hora"])
            st.write("Servicio:", c["servicio"], "-", c["detalle"])
            st.write("Estado:", c["estado"])

            if c["estado"] == "Agendada":
                if st.button(f"Iniciar atención {i}"):
                    c["estado"] = "En proceso"

            elif c["estado"] == "En proceso":
                if st.button(f"Finalizar atención {i}"):
                    c["estado"] = "Finalizada"
                    st.success("Se ha enviado la solicitud de evaluación al cliente")

            if c["evaluacion"]:
                st.write("Evaluación recibida:", c["evaluacion"])

    else:
        st.warning("Credenciales inválidas")
