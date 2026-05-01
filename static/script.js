const API_URL = ""; // Al estar en el mismo servidor, podemos usar rutas relativas
let usuarioLogueado = "";
let editandoId = null;

// --- GESTIÓN DE USUARIOS ---
async function registrarNuevoUsuario() {
    const email = document.getElementById('reg-email').value.trim();
    if (!email) return alert("Ingresa un correo");

    try {
        const res = await fetch(`/usuarios/registrar?correo=${encodeURIComponent(email)}`, { method: 'POST' });
        if (res.ok) {
            document.getElementById('mensaje-registro').innerHTML = "<span class='text-teal-400'>¡Registrado! Ya puedes ingresar.</span>";
            document.getElementById('email').value = email;
        } else {
            alert("El correo ya existe o es inválido.");
        }
    } catch (err) { console.error(err); }
}

async function enviarCorreo() {
    const email = document.getElementById('email').value.trim();
    if (!email) return alert("Ingresa tu correo");

    try {
        const res = await fetch(`/usuarios/login?correo=${encodeURIComponent(email)}`, { method: 'POST' });
        if (res.ok) {
            usuarioLogueado = email;
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');
            mostrarMensaje("Código enviado 📩", "success");
        } else { mostrarMensaje("Correo no registrado", "error"); }
    } catch (err) { console.error(err); }
}

async function verificarCodigo() {
    const otp = document.getElementById('otp').value.trim();
    try {
        const res = await fetch(`/usuarios/verificar?correo=${encodeURIComponent(usuarioLogueado)}&otp=${otp}`, { method: 'POST' });
        if (res.ok) {
            document.getElementById('auth-container').classList.add('hidden');
            document.getElementById('step-crud').classList.remove('hidden');
            document.getElementById('user-display').innerText = usuarioLogueado;
            cargarEstudiantes();
        } else { alert("Código incorrecto"); }
    } catch (err) { console.error(err); }
}

// --- CRUD ---
async function cargarEstudiantes() {
    try {
        const res = await fetch(`/api/estudiantes`);
        const estudiantes = await res.json();
        const tabla = document.getElementById('tabla-estudiantes');
        tabla.innerHTML = "";
        estudiantes.forEach(est => {
            tabla.innerHTML += `
                <tr class="hover:bg-slate-800/50">
                    <td class="px-6 py-4 text-white">${est.nombre} ${est.apellido}</td>
                    <td class="px-6 py-4 text-slate-400">${est.carrera}</td>
                    <td class="px-6 py-4 text-center">
                        <button onclick='prepararEdicion(${JSON.stringify(est)})' class="text-teal-500 mr-2"><i class="fas fa-edit"></i></button>
                        <button onclick="eliminarEstudiante(${est.id})" class="text-red-500"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { console.error(e); }
}

async function guardarEstudiante() {
    const data = {
        nombre: document.getElementById('form-nombre').value,
        apellido: document.getElementById('form-apellido').value,
        carrera: document.getElementById('form-carrera').value,
        email: document.getElementById('form-email').value
    };

    const url = editandoId ? `/api/estudiantes/${editandoId}` : `/api/estudiantes`;
    const method = editandoId ? 'PUT' : 'POST';

    const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (res.ok) {
        cerrarModal();
        cargarEstudiantes();
    } else {
        alert("Error al guardar. Revisa los datos.");
    }
}

async function eliminarEstudiante(id) {
    if (confirm("¿Eliminar?")) {
        await fetch(`/api/estudiantes/${id}`, { method: 'DELETE' });
        cargarEstudiantes();
    }
}

// --- UI ---
function abrirModal() {
    editandoId = null;
    document.getElementById('modal-titulo').innerText = "Nuevo Estudiante";
    document.getElementById('modal-estudiante').classList.remove('hidden');
}
function cerrarModal() { document.getElementById('modal-estudiante').classList.add('hidden'); }
function prepararEdicion(est) {
    editandoId = est.id;
    document.getElementById('modal-titulo').innerText = "Editar Estudiante";
    document.getElementById('form-nombre').value = est.nombre;
    document.getElementById('form-apellido').value = est.apellido;
    document.getElementById('form-carrera').value = est.carrera;
    document.getElementById('form-email').value = est.email;
    document.getElementById('modal-estudiante').classList.remove('hidden');
}
function cerrarSesion() { window.location.reload(); }
function mostrarMensaje(texto, tipo) {
    const div = document.getElementById('mensaje');
    div.innerText = texto;
    div.className = `mt-4 text-center ${tipo === 'success' ? 'text-teal-400' : 'text-red-400'}`;
}