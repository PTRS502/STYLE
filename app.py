from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Habilita CORS en toda la API

# Función para conectar con la base de datos
def connect_db():
    return sqlite3.connect("store.db", check_same_thread=False)

# Crear la base de datos y las tablas
def create_tables():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                precio REAL NOT NULL,
                imagen TEXT,
                descripcion TEXT,
                stock INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                total REAL NOT NULL,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'pendiente',
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detalle_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER,
                producto_id INTEGER,
                cantidad INTEGER,
                subtotal REAL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        ''')
        conn.commit()

create_tables()

# Endpoint para obtener productos
@app.route("/productos", methods=["GET"])
def get_productos():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, precio, imagen, descripcion, stock FROM productos")
        productos = [{
            "id": row[0], "nombre": row[1], "precio": row[2], "imagen": row[3], "descripcion": row[4], "stock": row[5]
        } for row in cursor.fetchall()]
    return jsonify(productos)

# Endpoint para agregar un producto
@app.route("/productos", methods=["POST"])
def add_producto():
    data = request.json
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, imagen, descripcion, stock) VALUES (?, ?, ?, ?, ?)",
                       (data["nombre"], data["precio"], data["imagen"], data.get("descripcion", ""), data["stock"]))
        conn.commit()
    return jsonify({"message": "Producto agregado"}), 201

# Endpoint para eliminar un producto
@app.route("/productos/<int:id>", methods=["DELETE"])
def delete_producto(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
        conn.commit()
    return jsonify({"message": f"Producto con ID {id} eliminado"}), 200

# Endpoint para realizar un pedido
@app.route("/pedidos", methods=["POST"])
def add_pedido():
    data = request.json
    usuario_id = data["usuario_id"]
    productos = data["productos"]  # Lista de productos con id y cantidad
    total = sum(p["precio"] * p["cantidad"] for p in productos)

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pedidos (usuario_id, total, estado) VALUES (?, ?, 'pendiente')", (usuario_id, total))
        pedido_id = cursor.lastrowid

        for producto in productos:
            cursor.execute("INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                           (pedido_id, producto["id"], producto["cantidad"], producto["precio"] * producto["cantidad"]))
        conn.commit()

    return jsonify({"message": "Pedido registrado", "pedido_id": pedido_id}), 201

# Iniciar Flask
if __name__ == "__main__":
    app.run(debug=True)
