const API_URL = "http://127.0.0.1:8000";
let editandoId = null;

// ================= AUTENTICACIÓN =================

async function enviarCorreo() {
    const email = document.getElementById('email').value;
    const btn = document.getElementById('btn-envio');

    if (!email) return alert("Ingresa un correo");

    btn.innerText = "Enviando...";
    btn.disabled = true;

    try {
        const res = await fetch(`${API_URL}/usuarios/login?correo=${encodeURIComponent(email)}`, { method: 'POST' });

        if (res.ok) {
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');

            mostrarMensaje("Código enviado con éxito 📩", "success");

            btn.innerText = "Código enviado ✔";
        } else {
            mostrarMensaje("No se pudo enviar el código", "error");
            btn.innerText = "Solicitar OTP";
            btn.disabled = false;
        }

    } catch (err) {
        mostrarMensaje("Error de conexión", "error");
        btn.innerText = "Solicitar OTP";
        btn.disabled = false;
    }
}

async function verificarCodigo() {
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;

    try {
        const res = await fetch(`${API_URL}/usuarios/verificar?correo=${encodeURIComponent(email)}&otp=${otp}`, { method: 'POST' });

        if (res.ok) {
            document.getElementById('login-container').classList.add('hidden');

            const crud = document.getElementById('step-crud');
            crud.classList.remove('hidden');
            crud.classList.add('fade-in');

            cargarEstudiantes();
        } else {
            mostrarMensaje("Código inválido", "error");
        }

    } catch (err) {
        mostrarMensaje("Error al verificar", "error");
    }
}

// ================= SESIÓN =================

function cerrarSesion() {
    document.getElementById('step-crud').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
    document.getElementById('step-email').classList.remove('hidden');
    document.getElementById('step-otp').classList.add('hidden');

    document.getElementById('btn-envio').innerText = "Solicitar OTP";
    document.getElementById('btn-envio').disabled = false;

    document.getElementById('email').value = "";
    document.getElementById('otp').value = "";
    document.getElementById('mensaje').innerText = "";
}

// ================= MENSAJES =================

function mostrarMensaje(texto, tipo) {
    const m = document.getElementById('mensaje');

    m.innerText = texto;
    m.className = "mt-4 text-center text-sm font-medium";

    if (tipo === "success") {
        m.classList.add("success");
    } else {
        m.classList.add("error");
    }
}

// ================= CRUD =================

async function cargarEstudiantes() {
    const tabla = document.getElementById('tabla-estudiantes');

    try {
        const res = await fetch(`${API_URL}/api/estudiantes`);
        const data = await res.json();

        tabla.innerHTML = "";

        data.forEach(est => {
            tabla.innerHTML += `
                <tr class="hover:bg-slate-800/40 transition-colors">
                    <td class="px-6 py-4">${est.nombre}</td>
                    <td class="px-6 py-4">${est.apellido}</td>
                    <td class="px-6 py-4 font-semibold text-[#14b8a6]">${est.carrera}</td>
                    <td class="px-6 py-4">
                        <div class="flex justify-center gap-4">
                            <button onclick='prepararEdicion(${est.id}, ${JSON.stringify(est.nombre)}, ${JSON.stringify(est.apellido)}, ${JSON.stringify(est.carrera)}, ${JSON.stringify(est.email)})' 
                                class="flex items-center gap-2 text-blue-400 hover:text-blue-300 font-bold text-xs transition-all">
                                ✏️ Editar
                            </button>
                            <button onclick="eliminarEstudiante(${est.id})" 
                                class="flex items-center gap-2 text-red-400 hover:text-red-300 font-bold text-xs transition-all">
                                🗑️ Eliminar
                            </button>
                        </div>
                    </td>
                </tr>`;
        });

    } catch (e) {
        console.error(e);
    }
}

async function guardarEstudiante() {
    const nombre = document.getElementById('form-nombre').value;
    const apellido = document.getElementById('form-apellido').value;
    const carrera = document.getElementById('form-carrera').value;
    const email = document.getElementById('form-email').value;

    let url = `${API_URL}/api/estudiantes?nombre=${nombre}&apellido=${apellido}&carrera=${carrera}&email=${email}`;
    let metodo = 'POST';

    if (editandoId) {
        url = `${API_URL}/api/estudiantes/${editandoId}?nombre=${nombre}&apellido=${apellido}&carrera=${carrera}&email=${email}`;
        metodo = 'PUT';
    }

    const res = await fetch(url, { method: metodo });

    if (res.ok) {
        cerrarModal();
        cargarEstudiantes();
    } else {
        mostrarMensaje("Error al guardar", "error");
    }
}

async function eliminarEstudiante(id) {
    if (confirm("¿Seguro que deseas eliminar este registro?")) {
        await fetch(`${API_URL}/api/estudiantes/${id}`, { method: 'DELETE' });
        cargarEstudiantes();
    }
}

// ================= UI =================

function abrirModal() {
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal-estudiante').classList.add('hidden');
    editandoId = null;

    document.getElementById('modal-titulo').innerText = "Registrar Estudiante";

    document.querySelectorAll('#modal-estudiante input').forEach(i => i.value = "");
}

function prepararEdicion(id, nombre, apellido, carrera, email) {
    editandoId = id;

    document.getElementById('modal-titulo').innerText = "Editar Estudiante";

    document.getElementById('form-nombre').value = nombre;
    document.getElementById('form-apellido').value = apellido;
    document.getElementById('form-carrera').value = carrera;
    document.getElementById('form-email').value = email;

    abrirModal();
}