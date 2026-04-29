const API_URL = window.location.origin;
let usuarioLogueado = ""; 
let editandoId = null;

async function enviarCorreo() {
    const email = document.getElementById('email').value;
    const btn = document.getElementById('btn-envio');
    const mensajeDiv = document.getElementById('mensaje');

    if (!email) return alert("Ingresa un correo");
    
    // 1. Mostrar estado de carga inmediatamente
    btn.innerText = "Enviando...";
    btn.disabled = true;
    mensajeDiv.innerText = "Procesando solicitud...";
    mensajeDiv.className = "mt-4 text-center text-sm text-teal-400";

    try {
        // 2. Intentar login
        let res = await fetch(`${API_URL}/usuarios/login?correo=${encodeURIComponent(email)}`, { method: 'POST' });

        // 3. Si el usuario no existe (404), lo registramos y reintentamos el login automáticamente
        if (res.status === 404) {
            mensajeDiv.innerText = "Creando cuenta nueva...";
            await fetch(`${API_URL}/usuarios/registrar?correo=${encodeURIComponent(email)}`, { method: 'POST' });
            // Reintento automático del login para generar el OTP
            res = await fetch(`${API_URL}/usuarios/login?correo=${encodeURIComponent(email)}`, { method: 'POST' });
        }

        if (res.ok) {
            // 4. Éxito: Pasamos al siguiente paso visual
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');
            mensajeDiv.innerText = "Código enviado con éxito";
        } else {
            mensajeDiv.innerText = "Error al obtener el código";
            mensajeDiv.className = "mt-4 text-center text-sm text-red-400";
            btn.disabled = false;
            btn.innerText = "Solicitar OTP";
        }
    } catch (err) {
        mensajeDiv.innerText = "Error de conexión con el servidor";
        mensajeDiv.className = "mt-4 text-center text-sm text-red-400";
        btn.disabled = false;
        btn.innerText = "Solicitar OTP";
    }
}
async function verificarCodigo() {
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;
    const res = await fetch(`${API_URL}/usuarios/verificar?correo=${encodeURIComponent(email)}&otp=${otp}`, { method: 'POST' });
    if (res.ok) {
        usuarioLogueado = email;
        document.getElementById('login-container').classList.add('hidden');
        document.getElementById('step-crud').classList.remove('hidden');
        cargarEstudiantes();
    } else { alert("Código incorrecto"); }
}

// --- CRUD ESTUDIANTES ---
async function cargarEstudiantes() {
    const res = await fetch(`${API_URL}/api/estudiantes?correo=${encodeURIComponent(usuarioLogueado)}`);
    const data = await res.json();
    const tabla = document.getElementById('tabla-estudiantes');
    tabla.innerHTML = "";
    data.forEach(est => {
        tabla.innerHTML += `
            <tr class="border-b border-slate-700 hover:bg-slate-800/40">
                <td class="px-6 py-4">${est.nombre}</td>
                <td class="px-6 py-4">${est.apellido}</td>
                <td class="px-6 py-4 text-teal-400">${est.carrera}</td>
                <td class="px-6 py-4 flex gap-4">
                    <button onclick="prepararEdicion('${encodeURIComponent(JSON.stringify(est))}')" class="text-yellow-500 hover:underline">Editar</button>
                    <button onclick="eliminarEstudiante(${est.id})" class="text-red-500 hover:underline">Eliminar</button>
                </td>
            </tr>`;
    });
}

function abrirModalNuevo() {
    editandoId = null;
    document.getElementById('form-estudiante').reset();
    document.getElementById('modal-title').innerText = "Nuevo Estudiante";
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

function prepararEdicion(estString) {
    const est = JSON.parse(decodeURIComponent(estString));
    editandoId = est.id;
    document.getElementById('form-nombre').value = est.nombre;
    document.getElementById('form-apellido').value = est.apellido;
    document.getElementById('form-carrera').value = est.carrera;
    document.getElementById('form-email').value = est.email;
    document.getElementById('modal-title').innerText = "Editar Estudiante";
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

async function guardarEstudiante() {
    const n = document.getElementById('form-nombre').value;
    const a = document.getElementById('form-apellido').value;
    const c = document.getElementById('form-carrera').value;
    const e = document.getElementById('form-email').value;

    const params = `nombre=${n}&apellido=${a}&carrera=${c}&email=${e}&admin_correo=${encodeURIComponent(usuarioLogueado)}`;
    const url = editandoId ? `${API_URL}/api/estudiantes/${editandoId}?${params}` : `${API_URL}/api/estudiantes?${params}`;
    const metodo = editandoId ? 'PUT' : 'POST';

    const res = await fetch(url, { method: metodo });
    if (res.ok) { cerrarModal(); cargarEstudiantes(); }
}

async function eliminarEstudiante(id) {
    if (confirm("¿Estás seguro?")) {
        await fetch(`${API_URL}/api/estudiantes/${id}?admin_correo=${encodeURIComponent(usuarioLogueado)}`, { method: 'DELETE' });
        cargarEstudiantes();
    }
}

function cerrarModal() { document.getElementById('modal-estudiante').classList.add('hidden'); }