const VERSION = "1.2.0";

// 🔥 URL DEL BACKEND EN RENDER
const API_URL = "https://servicio-otp-21.onrender.com";

let usuarioLogueado = "";
let editandoId = null;

// 🔥 CONTROL OTP
let otpEnviado = false;

console.log(`Sistema OTP v${VERSION} iniciado`);

// =========================
// REGISTRO
// =========================
async function registrarNuevoUsuario() {
    const email = document.getElementById('reg-email').value.trim();
    if (!email) return alert("Por favor, ingresa un correo.");

    const params = new URLSearchParams({ correo: email });

    try {
        const res = await fetch(`${API_URL}/usuarios/registrar?${params}`, {
            method: 'POST'
        });

        if (res.ok) {
            document.getElementById('mensaje-registro').innerHTML =
                "<span class='text-teal-400'>¡Usuario registrado con éxito!</span>";

            document.getElementById('email').value = email;
        } else {
            const err = await res.json();
            alert(err.detail || "Error al registrar");
        }

    } catch (err) {
        console.error("Error registro:", err);
    }
}

// =========================
// LOGIN - SOLICITAR OTP
// =========================
async function enviarCorreo() {
    console.log("CLICK EN OTP 🔥");

    const email = document.getElementById('email').value.trim();
    if (!email) return alert("Ingresa tu correo.");

    // 🔒 Evitar múltiples OTP
    if (otpEnviado) {
        mostrarMensaje("Ya solicitaste un código. Revisa tu correo 📩", "error");
        return;
    }

    const btn = document.getElementById("btn-envio");
    btn.disabled = true;
    btn.innerText = "Enviando...";

    const params = new URLSearchParams({ correo: email });

    try {
        const res = await fetch(`${API_URL}/usuarios/login?${params}`, {
            method: 'POST'
        });

        if (res.ok) {
            usuarioLogueado = email;
            otpEnviado = true;

            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');

            mostrarMensaje("Código enviado a tu correo 📩", "success");

        } else {
            const err = await res.json();
            mostrarMensaje(err.detail || "Correo no registrado", "error");

            btn.disabled = false;
            btn.innerText = "Solicitar OTP";
        }

    } catch (err) {
        console.error("Error login:", err);
        mostrarMensaje("Error de conexión con el servidor", "error");

        btn.disabled = false;
        btn.innerText = "Solicitar OTP";
    }
}

// =========================
// REENVIAR OTP
// =========================
function reenviarOTP() {
    otpEnviado = false;

    const btn = document.getElementById("btn-envio");
    btn.disabled = false;
    btn.innerText = "Solicitar OTP";

    enviarCorreo();
}

// =========================
// VERIFICAR OTP
// =========================
async function verificarCodigo() {
    const otp = document.getElementById('otp').value.trim();
    if (otp.length < 4) return alert("Ingresa el código completo.");

    try {
        const res = await fetch(
            `${API_URL}/usuarios/verificar?correo=${encodeURIComponent(usuarioLogueado)}&otp=${encodeURIComponent(otp)}`,
            { method: 'POST' }
        );

        if (res.ok) {
            document.getElementById('auth-container').classList.add('hidden');
            document.getElementById('step-crud').classList.remove('hidden');
            document.getElementById('user-display').innerText = usuarioLogueado;

            cargarEstudiantes();

        } else {
            mostrarMensaje("Código incorrecto o expirado", "error");
        }

    } catch (err) {
        console.error("Error verificación:", err);
    }
}

// =========================
// CRUD ESTUDIANTES
// =========================
async function cargarEstudiantes() {
    try {
        const res = await fetch(`${API_URL}/api/estudiantes`);
        const estudiantes = await res.json();

        const tabla = document.getElementById('tabla-estudiantes');
        tabla.innerHTML = "";

        if (estudiantes.length === 0) {
            tabla.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center text-slate-500 py-4">
                        No hay estudiantes registrados
                    </td>
                </tr>`;
            return;
        }

        estudiantes.forEach(est => {
            tabla.innerHTML += `
                <tr>
                    <td>${est.nombre} ${est.apellido}<br><small>${est.email}</small></td>
                    <td>${est.carrera}</td>
                    <td>
                        <button onclick='prepararEdicion(${JSON.stringify(est)})'>✏️</button>
                        <button onclick="eliminarEstudiante(${est.id})">🗑️</button>
                    </td>
                </tr>`;
        });

    } catch (err) {
        console.error("Error cargando estudiantes:", err);
    }
}

async function guardarEstudiante() {
    const data = {
        nombre: document.getElementById('form-nombre').value.trim(),
        apellido: document.getElementById('form-apellido').value.trim(),
        carrera: document.getElementById('form-carrera').value.trim(),
        email: document.getElementById('form-email').value.trim()
    };

    if (!data.nombre || !data.email) {
        return alert("Nombre y email obligatorios");
    }

    const url = editandoId
        ? `${API_URL}/api/estudiantes/${editandoId}`
        : `${API_URL}/api/estudiantes`;

    const method = editandoId ? "PUT" : "POST";

    try {
        const res = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            cerrarModal();
            cargarEstudiantes();
        } else {
            alert("Error al guardar");
        }

    } catch (err) {
        console.error("Error guardar:", err);
    }
}

async function eliminarEstudiante(id) {
    if (!confirm("¿Eliminar estudiante?")) return;

    try {
        const res = await fetch(`${API_URL}/api/estudiantes/${id}`, {
            method: 'DELETE'
        });

        if (res.ok) cargarEstudiantes();

    } catch (err) {
        console.error("Error eliminar:", err);
    }
}

// =========================
// UI
// =========================
function abrirModal() {
    editandoId = null;
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-estudiante').classList.add('hidden');
}

function prepararEdicion(est) {
    editandoId = est.id;

    document.getElementById('form-nombre').value = est.nombre;
    document.getElementById('form-apellido').value = est.apellido;
    document.getElementById('form-carrera').value = est.carrera;
    document.getElementById('form-email').value = est.email;

    abrirModal();
}

function cerrarSesion() {
    location.reload();
}

function mostrarMensaje(texto, tipo) {
    const div = document.getElementById('mensaje');

    div.innerText = texto;
    div.className =
        tipo === "success"
            ? "text-teal-400 text-center mt-4"
            : "text-red-400 text-center mt-4";
}