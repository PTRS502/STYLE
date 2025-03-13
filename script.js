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
        li.innerHTML = `${item.producto} - $${item.precio.toFixed(2)} 
            <button onclick="eliminarDelCarrito(${index})">❌</button>`;
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

// Cargar productos desde la API de Flask
fetch("http://127.0.0.1:5000/productos")
    .then(response => response.json())
    .then(data => mostrarProductos(data))
    .catch(error => console.error("Error obteniendo productos:", error));

function mostrarProductos(productos) {
    let contenedor = document.querySelector(".productos");
    contenedor.innerHTML = ""; 
    
    let fila;
    productos.forEach((producto, index) => {
        if (index % 4 === 0) {
            fila = document.createElement("div");
            fila.classList.add("fila");
            contenedor.appendChild(fila);
        }
        
        let div = document.createElement("div");
        div.classList.add("producto");
        div.innerHTML = `
            <img src="${producto.imagen}" alt="${producto.nombre}">
            <h3>${producto.nombre}</h3>
            <p>$${producto.precio.toFixed(2)}</p>
            <button onclick="agregarAlCarrito('${producto.nombre}', ${producto.precio})">Agregar al Carrito</button>
        `;
        fila.appendChild(div);
    });
}
