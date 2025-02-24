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
    carrito.forEach(item => {
        let li = document.createElement("li");
        li.textContent = `${item.producto} - $${item.precio.toFixed(2)}`;
        listaCarrito.appendChild(li);
    });

    totalElemento.textContent = total.toFixed(2);
}

// Guardar carrito en localStorage
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
    localStorage.setItem("total", total.toFixed(2));
}

// Cargar carrito al iniciar la página y actualizar el total desde localStorage
window.onload = function () {
    // Recuperar carrito y total al recargar la página
    carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    total = parseFloat(localStorage.getItem("total")) || 0;
    actualizarCarrito();
};

// Vaciar carrito
function vaciarCarrito() {
    carrito = [];
    total = 0;
    actualizarCarrito();
    guardarCarrito();
}
