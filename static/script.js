const API_URL = "http://127.0.0.1:8000";
let editandoId = null;

// --- AUTENTICACIÓN ---
async function enviarCorreo() {
    const email = document.getElementById('email').value;
    const btn = document.getElementById('btn-envio');
    if (!email) return alert("Ingresa un correo");
    
    btn.innerText = "Enviando..."; // Aquí es donde cambia el texto
    try {
        const res = await fetch(`${API_URL}/usuarios/login?correo=${encodeURIComponent(email)}`, { method: 'POST' });
        if (res.ok) {
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');
            mostrarMensaje("Código enviado con éxito", "text-teal-400");
        }
    } catch (err) { 
        mostrarMensaje("Error de conexión", "text-red-400"); 
        btn.innerText = "Solicitar OTP"; // Lo regresamos si falla
    }
}

async function verificarCodigo() {
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;
    try {
        const res = await fetch(`${API_URL}/usuarios/verificar?correo=${encodeURIComponent(email)}&otp=${otp}`, { method: 'POST' });
        if (res.ok) {
            document.getElementById('login-container').classList.add('hidden');
            document.getElementById('step-crud').classList.remove('hidden');
            cargarEstudiantes();
        } else { mostrarMensaje("Código inválido", "text-red-400"); }
    } catch (err) { mostrarMensaje("Error", "text-red-400"); }
}

// --- FUNCIÓN CERRAR SESIÓN (CORREGIDA) ---
function cerrarSesion() {
    document.getElementById('step-crud').classList.add('hidden');
    document.getElementById('login-container').classList.remove('hidden');
    document.getElementById('step-email').classList.remove('hidden');
    document.getElementById('step-otp').classList.add('hidden');
    
    // RESTABLECER EL BOTÓN Y CAMPOS
    document.getElementById('btn-envio').innerText = "Solicitar OTP"; // <--- ESTO ARREGLA TU PROBLEMA
    document.getElementById('email').value = "";
    document.getElementById('otp').value = "";
    document.getElementById('mensaje').innerText = "";
}

function mostrarMensaje(t, c) {
    const m = document.getElementById('mensaje');
    m.innerText = t; m.className = `mt-4 text-center text-sm font-medium ${c}`;
}

// --- CRUD ---
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
                            <button onclick="prepararEdicion(${est.id}, '${est.nombre}', '${est.apellido}', '${est.carrera}', '${est.email}')" 
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
    } catch (e) { console.error(e); }
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
    }
}

async function eliminarEstudiante(id) {
    if (confirm("¿Seguro que deseas eliminar este registro?")) {
        await fetch(`${API_URL}/api/estudiantes/${id}`, { method: 'DELETE' });
        cargarEstudiantes();
    }
}

// HELPERS UI
function abrirModal() { document.getElementById('modal-estudiante').classList.remove('hidden'); }
function cerrarModal() { 
    document.getElementById('modal-estudiante').classList.add('hidden');
    editandoId = null;
    document.getElementById('modal-titulo').innerText = "Registrar Estudiante";
    document.querySelectorAll('#modal-estudiante input').forEach(i => i.value = "");
}

function prepararEdicion(id, n, a, c, e) {
    editandoId = id;
    document.getElementById('modal-titulo').innerText = "Editar Estudiante";
    document.getElementById('form-nombre').value = n;
    document.getElementById('form-apellido').value = a;
    document.getElementById('form-carrera').value = c;
    document.getElementById('form-email').value = e;
    abrirModal();
}