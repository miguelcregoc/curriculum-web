// Pon aquí tu Invoke URL, seguida de /contacto (sin barra final)
const API_URL = "https://62eaubkycl.execute-api.eu-north-1.amazonaws.com/contacto";

const formulario = document.getElementById("form-contacto");
const estado = document.getElementById("estado");
const boton = formulario.querySelector('button[type="submit"]');

formulario.addEventListener("submit", async (evento) => {
    // Evita que el navegador recargue la página al enviar
    evento.preventDefault();

    const datos = {
        asunto: document.getElementById("asunto").value,
        email: document.getElementById("email").value,
        mensaje: document.getElementById("mensaje").value,
    };

    // Evita envíos duplicados mientras se espera la respuesta
    boton.disabled = true;
    estado.textContent = "Enviando...";

    try {
        const respuesta = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(datos),
        });

        if (respuesta.ok) {
            estado.textContent = "Mensaje enviado. ¡Gracias!";
            formulario.reset();
        } else if (respuesta.status === 400) {
            estado.textContent = "Revisa los campos e inténtalo de nuevo.";
        } else if (respuesta.status === 429) {
            estado.textContent = "Demasiados intentos. Espera un poco.";
        } else {
            estado.textContent = "No se pudo enviar. Inténtalo más tarde.";
        }
    } catch (error) {
        // Sin red, o el navegador bloqueó la petición (CORS)
        console.error(error);
        estado.textContent = "No se pudo conectar. Inténtalo más tarde.";
    } finally {
        // Se ejecuta siempre, haya ido bien o mal
        boton.disabled = false;
    }
});