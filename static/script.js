/**
 * SISTEMA DE GESTIÓN OTP - CLIENTE JS
 * Versión: 1.0.4 - "Render Stable"
 * Última actualización: Mayo 2026
 */

const VERSION = "1.0.4";
let usuarioLogueado = "";
let editandoId = null;

console.log(`%c Sistema OTP v${VERSION} cargado correctamente `, "background: #0d9488; color: #fff; font-weight: bold;");

// --- GESTIÓN DE USUARIOS ---

/**
 * Registra un nuevo administrador en el sistema
 */
// --- REGISTRO ACTUALIZADO ---
async function registrarNuevoUsuario() {
    const email = document.getElementById('reg-email').value.trim();
    if (!email) return alert("Por favor, ingresa un correo.");

    // Usamos URLSearchParams para que el navegador codifique el @ correctamente una sola vez
    const params = new URLSearchParams({ correo: email });
    
    try {
        const res = await fetch(`/usuarios/registrar?${params.toString()}`, { method: 'POST' });
        
        if (res.ok) {
            // Mensaje limpio como pediste
            document.getElementById('mensaje-registro').innerHTML = "<span class='text-teal-400'>¡Usuario registrado con éxito!</span>";
            document.getElementById('email').value = email;
        } else {
            const err = await res.json();
            alert(err.detail || "Error al registrar");
        }
    } catch (err) { console.error(err); }
}

// --- LOGIN ACTUALIZADO ---
async function enviarCorreo() {
    const email = document.getElementById('email').value.trim();
    if (!email) return alert("Ingresa tu correo.");

    const params = new URLSearchParams({ correo: email });

    try {
        const res = await fetch(`/usuarios/login?${params.toString()}`, { method: 'POST' });
        if (res.ok) {
            usuarioLogueado = email;
            document.getElementById('step-email').classList.add('hidden');
            document.getElementById('step-otp').classList.remove('hidden');
            
            // Mensaje profesional sin menciones a Render
            mostrarMensaje("Código enviado con éxito a tu correo 📩", "success");
        } else {
            mostrarMensaje("El correo no está registrado", "error");
        }
    } catch (err) { console.error(err); }
}



/**
 * Verifica el OTP ingresado por el usuario
 */
async function verificarCodigo() {
    const otp = document.getElementById('otp').value.trim();
    if (otp.length < 4) return alert("Ingresa el código completo.");

    try {
        const res = await fetch(`/usuarios/verificar?correo=${encodeURIComponent(usuarioLogueado)}&otp=${encodeURIComponent(otp)}`, { 
            method: 'POST' 
        });

        if (res.ok) {
            document.getElementById('auth-container').classList.add('hidden');
            document.getElementById('step-crud').classList.remove('hidden');
            document.getElementById('user-display').innerText = usuarioLogueado;
            cargarEstudiantes();
        } else {
            alert("Código OTP incorrecto o expirado.");
        }
    } catch (err) {
        console.error("Error en verificación:", err);
    }
}

// --- CRUD DE ESTUDIANTES ---

/**
 * Obtiene y renderiza la lista de estudiantes
 */
async function cargarEstudiantes() {
    try {
        const res = await fetch(`/api/estudiantes`);
        const estudiantes = await res.json();
        const tabla = document.getElementById('tabla-estudiantes');
        
        tabla.innerHTML = estudiantes.length === 0 
            ? '<tr><td colspan="3" class="px-6 py-4 text-center text-slate-500">No hay estudiantes registrados.</td></tr>' 
            : "";

        estudiantes.forEach(est => {
            tabla.innerHTML += `
                <tr class="hover:bg-slate-800/50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="text-white font-medium">${est.nombre} ${est.apellido}</div>
                        <div class="text-xs text-slate-500">${est.email}</div>
                    </td>
                    <td class="px-6 py-4 text-slate-400">${est.carrera}</td>
                    <td class="px-6 py-4 text-center">
                        <button onclick='prepararEdicion(${JSON.stringify(est)})' class="text-teal-500 hover:text-teal-400 p-2">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="eliminarEstudiante(${est.id})" class="text-red-500 hover:text-red-400 p-2">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>`;
        });
    } catch (e) {
        console.error("Error cargando estudiantes:", e);
    }
}

/**
 * Crea o actualiza un estudiante
 */
async function guardarEstudiante() {
    const data = {
        nombre: document.getElementById('form-nombre').value.trim(),
        apellido: document.getElementById('form-apellido').value.trim(),
        carrera: document.getElementById('form-carrera').value.trim(),
        email: document.getElementById('form-email').value.trim()
    };

    if (!data.nombre || !data.email) return alert("Nombre y Email son obligatorios.");

    const url = editandoId ? `/api/estudiantes/${editandoId}` : `/api/estudiantes`;
    const method = editandoId ? 'PUT' : 'POST';

    try {
        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (res.ok) {
            cerrarModal();
            cargarEstudiantes();
        } else {
            alert("Error al procesar la solicitud. Verifica los datos.");
        }
    } catch (err) {
        console.error("Error al guardar:", err);
    }
}

/**
 * Elimina un estudiante por ID
 */
async function eliminarEstudiante(id) {
    if (confirm("¿Estás seguro de eliminar este registro?")) {
        try {
            const res = await fetch(`/api/estudiantes/${id}`, { method: 'DELETE' });
            if (res.ok) cargarEstudiantes();
        } catch (err) {
            console.error("Error al eliminar:", err);
        }
    }
}

// --- INTERFAZ DE USUARIO (UI) ---

function abrirModal() {
    editandoId = null;
    document.getElementById('modal-titulo').innerText = "Nuevo Estudiante";
    document.getElementById('form-nombre').value = "";
    document.getElementById('form-apellido').value = "";
    document.getElementById('form-carrera').value = "";
    document.getElementById('form-email').value = "";
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

function cerrarModal() { 
    document.getElementById('modal-estudiante').classList.add('hidden'); 
}

function prepararEdicion(est) {
    editandoId = est.id;
    document.getElementById('modal-titulo').innerText = "Editar Estudiante";
    document.getElementById('form-nombre').value = est.nombre;
    document.getElementById('form-apellido').value = est.apellido;
    document.getElementById('form-carrera').value = est.carrera;
    document.getElementById('form-email').value = est.email;
    document.getElementById('modal-estudiante').classList.remove('hidden');
}

function cerrarSesion() { 
    if(confirm("¿Cerrar sesión?")) window.location.reload(); 
}

function mostrarMensaje(texto, tipo) {
    const div = document.getElementById('mensaje');
    div.innerText = texto;
    div.className = `mt-4 text-center text-sm font-medium ${tipo === 'success' ? 'text-teal-400' : 'text-red-400'}`;
}