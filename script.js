let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
let total = parseFloat(localStorage.getItem("total")) || 0;

function agregarAlCarrito(producto, precio) {
    carrito.push({ producto, precio });
    total += precio;
    actualizarCarrito();
    guardarCarrito();
}

function actualizarCarrito() {
    let listaCarrito = document.getElementById("lista-carrito");
    let totalElemento = document.getElementById("total");

    listaCarrito.innerHTML = "";
    carrito.forEach((item, index) => {
        let li = document.createElement("li");
        
        // Botón con un ícono de "X"
        let eliminarBtn = document.createElement("button");
        eliminarBtn.innerHTML = "X"; // Ícono de eliminar
        eliminarBtn.classList.add("eliminar-btn"); // Agregar clase para CSS
        eliminarBtn.onclick = function() {
            eliminarDelCarrito(index);
        };

        li.innerHTML = `${item.producto} - $${item.precio.toFixed(2)} `;
        li.appendChild(eliminarBtn);
        listaCarrito.appendChild(li);
    });

    totalElemento.textContent = total.toFixed(2);
}


function eliminarDelCarrito(index) {
    if (index > -1) {
        total -= carrito[index].precio;
        carrito.splice(index, 1);
    }
    actualizarCarrito();
    guardarCarrito();
}

function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
    localStorage.setItem("total", total.toFixed(2));
}

window.onload = function () {
    carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    total = parseFloat(localStorage.getItem("total")) || 0;
    actualizarCarrito();
};

function vaciarCarrito() {
    carrito = [];
    total = 0;
    actualizarCarrito();
    guardarCarrito();
}

// Enviar pedido a Flask cuando el usuario presione "Comprar"
function enviarPedido() {
    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    let pedido = {
        usuario_id: 1, // Aquí puedes asignar el ID del usuario si usas sesiones
        productos: carrito.map(item => ({
            id: obtenerIdProducto(item.producto), // Obtener el ID del producto
            nombre: item.producto,
            precio: item.precio,
            cantidad: 1
        }))
    };

    console.log("Enviando pedido a la API:", pedido); // DEBUG: Ver pedido en consola

    fetch("http://127.0.0.1:5000/pedidos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(pedido)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Respuesta del servidor:", data); // DEBUG: Ver respuesta de Flask
        alert("Pedido enviado con éxito.");
        vaciarCarrito();
    })
    .catch(error => console.error("Error enviando pedido:", error));
}

// Obtener el ID del producto según su nombre (esto es importante)
function obtenerIdProducto(nombreProducto) {
    let productosDisponibles = {
        "Blusa damaia atelier manga larga para mujer": 1,
        "Vestido midi casual para mujer": 2,
        "Camisa Casual": 3,
        "Camisa de vestir de algodón manga larga para hombre": 4,
        "Pantalón amplio para mujer": 5,
        "Pantalón slim de algodón para hombre": 6,
        "Pantalón straight para hombre": 7,
        "Pantalón straight para mujer": 8,
        "Vestido a la rodilla casual para mujer": 9,
        "Vestido Elegante": 10
    };
    return productosDisponibles[nombreProducto] || null;
}
