import streamlit as st
from datetime import datetime, timedelta, time

st.set_page_config(layout="wide")
st.title("🏦 Sistema Bancario Inteligente")

# ======================
# BASE DE DATOS
# ======================
if "citas" not in st.session_state:
    st.session_state.citas = []

# ======================
# TRABAJADORES POR SERVICIO
# ======================
trabajadores = {
    "Apertura de cuentas": "cajero1",
    "Solicitud de créditos": "asesor1",
    "Consultas / Problemas": "soporte1",
    "Asesoría bancaria": "finanzas1",
    "Actualización de información": "servicio1"
}

# ======================
# HORARIOS
# ======================
def generar_horarios():
    horarios = []
    inicio = datetime.combine(datetime.today(), time(8, 0))
    fin = datetime.combine(datetime.today(), time(17, 0))

    while inicio + timedelta(minutes=35) <= fin:
        horarios.append(inicio.strftime("%H:%M"))
        inicio += timedelta(minutes=35)

    return horarios

menu = st.sidebar.selectbox("Menú", ["Cliente", "Trabajador"])

# ======================
# CLIENTE
# ======================
if menu == "Cliente":
    st.header("📱 App Cliente")

    nombre = st.text_input("Nombre")

    categoria = st.selectbox("Servicio principal", list(trabajadores.keys()))

    # DESGLOSE
    servicio = ""
    if categoria == "Apertura de cuentas":
        servicio = st.selectbox("Tipo", ["Ahorro", "Corriente", "Empresarial", "Estudiantil"])
    elif categoria == "Solicitud de créditos":
        servicio = st.selectbox("Tipo", ["Personal", "Hipotecario", "Vehículo", "Empresarial"])
    elif categoria == "Consultas / Problemas":
        servicio = st.selectbox("Tipo", ["Tarjetas", "Transferencias", "Intereses", "Banca digital"])
    elif categoria == "Asesoría bancaria":
        servicio = st.selectbox("Tipo", ["Ahorro", "Estado cuenta", "Créditos", "Hipotecas"])
    elif categoria == "Actualización de información":
        servicio = st.selectbox("Tipo", ["Datos", "Cambio cuenta", "Clausura"])

    # ASIGNACIÓN AUTOMÁTICA
    trabajador = trabajadores[categoria]
    st.info(f"👨‍💼 Te atenderá: {trabajador}")

    # FECHA Y HORA AL FINAL
    fecha = st.date_input("Selecciona fecha")

    todos = generar_horarios()
    ocupados = [
        c["hora"] for c in st.session_state.citas
        if c["fecha"] == str(fecha)
    ]
    disponibles = [h for h in todos if h not in ocupados]

    hora = st.selectbox("Horario disponible", disponibles)

    if st.button("Confirmar cita"):
        st.session_state.citas.append({
            "cliente": nombre,
            "categoria": categoria,
            "servicio": servicio,
            "trabajador": trabajador,
            "fecha": str(fecha),
            "hora": hora,
            "estado": "Pendiente",
            "evaluacion": None
        })
        st.success("Cita confirmada ✅")

    # ================= ENCUESTA =================
    st.subheader("📊 Evaluar servicio")

    for i, cita in enumerate(st.session_state.citas):
        if cita["cliente"] == nombre and cita["estado"] == "Finalizada" and cita["evaluacion"] is None:
            st.write(f"Servicio: {cita['categoria']} - {cita['servicio']}")
            calificacion = st.slider(f"Califica atención {i}", 1, 5)

            if st.button(f"Enviar evaluación {i}"):
                cita["evaluacion"] = calificacion
                st.success("Gracias por tu evaluación ⭐")

# ======================
# TRABAJADOR
# ======================
if menu == "Trabajador":
    st.header("💻 App Trabajador")

    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    usuarios = ["cajero1", "asesor1", "soporte1", "finanzas1", "servicio1"]

    if usuario in usuarios and password == "1234":
        st.success(f"Bienvenido {usuario}")

        citas_usuario = [c for c in st.session_state.citas if c["trabajador"] == usuario]

        # PROMEDIO
        evaluaciones = [c["evaluacion"] for c in citas_usuario if c["evaluacion"]]
        if evaluaciones:
            promedio = sum(evaluaciones) / len(evaluaciones)
            st.metric("⭐ Promedio atención", round(promedio, 2))

        for i, cita in enumerate(citas_usuario):
            st.markdown("---")
            st.write(f"👤 {cita['cliente']}")
            st.write(f"{cita['fecha']} - {cita['hora']}")
            st.write(f"{cita['categoria']} - {cita['servicio']}")
            st.write(f"Estado: {cita['estado']}")

            if cita["estado"] == "Pendiente":
                if st.button(f"Iniciar {i}"):
                    cita["estado"] = "En proceso"

            elif cita["estado"] == "En proceso":
                if st.button(f"Finalizar {i}"):
                    cita["estado"] = "Finalizada"
                    st.success("Se envió encuesta al cliente 📩")

            if cita["evaluacion"]:
                st.write(f"⭐ Evaluación: {cita['evaluacion']}")

    else:
        st.warning("Credenciales incorrectas")
