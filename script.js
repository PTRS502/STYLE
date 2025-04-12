// 1. Inicialización del carrito y el total
let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
let total = parseFloat(localStorage.getItem("total")) || 0;

// Función para agregar un producto al carrito
function agregarAlCarrito(producto, precio) {
    carrito.push({ producto, precio });
    total += precio;
    actualizarCarrito();
    guardarCarrito();
}

// Función para actualizar la vista del carrito
function actualizarCarrito() {
    let listaCarrito = document.getElementById("lista-carrito");
    let totalElemento = document.getElementById("total");

    listaCarrito.innerHTML = ""; // Limpiar la lista de productos
    carrito.forEach((item, index) => {
        let li = document.createElement("li");
        
        // Botón con un ícono de "X" para eliminar el producto
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

    // Actualizar el total del carrito
    totalElemento.textContent = total.toFixed(2);
}

// Función para eliminar un producto del carrito
function eliminarDelCarrito(index) {
    if (index > -1) {
        total -= carrito[index].precio;
        carrito.splice(index, 1); // Eliminar el producto del array
    }
    actualizarCarrito();
    guardarCarrito();
}

// Función para guardar el carrito en localStorage
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
    localStorage.setItem("total", total.toFixed(2));
}

// Función para vaciar el carrito
function vaciarCarrito() {
    carrito = [];
    total = 0;
    actualizarCarrito();
    guardarCarrito();
}

// 2. Enviar pedido a Flask cuando el usuario presione "Comprar"
function enviarPedido() {
    if (carrito.length === 0) {
        alert("El carrito está vacío.");
        return;
    }

    let usuario_id = 1; // Este es un valor de ejemplo, si tienes login, deberías obtener el ID del usuario autenticado

    let pedido = {
        usuario_id: usuario_id,
        productos: carrito.map(item => ({
            id: obtenerIdProducto(item.producto), // Obtener el ID del producto
            nombre: item.producto,
            precio: item.precio,
            cantidad: 1 // Suponemos que solo agregan 1 de cada producto
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

// 3. Obtener el ID del producto según su nombre (esto es importante)
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

// Cuando la página carga, recuperamos el carrito guardado en localStorage
window.onload = function () {
    carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    total = parseFloat(localStorage.getItem("total")) || 0;
    actualizarCarrito();
};

// 4. Esta función se ejecutará cuando el formulario de agregar producto sea enviado
document.getElementById("agregarProductoForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Previene el comportamiento por defecto de envío del formulario

    // Crear el objeto producto con los valores del formulario
    const producto = {
        nombre: document.getElementById("nombre").value,
        precio: parseFloat(document.getElementById("precio").value),
        imagen: document.getElementById("imagen").value,
        descripcion: document.getElementById("descripcion").value,
        stock: parseInt(document.getElementById("stock").value)
    };

    // Hacer la solicitud POST al backend (Flask) para agregar el producto
    fetch("http://127.0.0.1:5000/productos", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(producto)
    })
    .then(response => response.json())
    .then(data => {
        alert("Producto agregado!");
    })
    .catch(error => {
        alert("Error al agregar producto");
    });
});

// 5. Registro de usuario
document.getElementById("registroForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Previene el comportamiento por defecto de envío del formulario

    // Crear el objeto usuario con los valores del formulario
    const usuario = {
        nombre: document.getElementById("nombre").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    // Hacer la solicitud POST al backend (Flask) para registrar al usuario
    fetch("http://127.0.0.1:5000/usuarios", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(usuario)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Muestra el mensaje del backend
    })
    .catch(error => {
        alert("Error al registrar usuario");
    });
});

// 6. Aquí es donde colocas la función para cargar los productos cuando la página se haya cargado
document.addEventListener('DOMContentLoaded', function() {
    // Realizar solicitud para obtener los productos
    fetch('http://127.0.0.1:5000/productos')
        .then(response => response.json())
        .then(data => {
            // Mostrar productos en la página
            const productosContainer = document.querySelector('.productos');
            data.forEach(producto => {
                const productHTML = `
                    <div class="producto">
                        <img src="${producto.imagen}" alt="${producto.nombre}">
                        <h3>${producto.nombre}</h3>
                        <p>$${producto.precio}</p>
                        <button onclick="agregarAlCarrito('${producto.nombre}', ${producto.precio})">Agregar al Carrito</button>
                    </div>
                `;
                productosContainer.innerHTML += productHTML;
            });
        })
        .catch(error => console.error('Error al obtener los productos:', error));
});
