from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt  # Usamos bcrypt para encriptar la contraseña

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

# Crear las tablas al inicio
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

# Endpoint para registrar un usuario (POST)
@app.route("/usuarios", methods=["POST"])
def register_usuario():
    data = request.json
    nombre = data["nombre"]
    email = data["email"]
    password = data["password"]

    # Encriptar la contraseña antes de guardarla en la base de datos
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
                           (nombre, email, hashed_password))
            conn.commit()
            return jsonify({"message": "Usuario registrado exitosamente"}), 201
        except sqlite3.IntegrityError:
            return jsonify({"message": "El correo electrónico ya está registrado"}), 400

# Endpoint para iniciar sesión (POST)
@app.route("/login", methods=["POST"])
def login_usuario():
    data = request.json
    email = data["email"]
    password = data["password"]

    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, password FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()

        if user:
            # Verificamos si la contraseña ingresada coincide con la almacenada
            if bcrypt.checkpw(password.encode('utf-8'), user[2]):
                return jsonify({"message": "Inicio de sesión exitoso", "user": {"id": user[0], "nombre": user[1]}}), 200
            else:
                return jsonify({"message": "Contraseña incorrecta"}), 401
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
@app.route("/usuarios/<int:id>", methods=["GET"])
def get_usuario(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, email FROM usuarios WHERE id = ?", (id,))
        user = cursor.fetchone()

        if user:
            return jsonify({"id": user[0], "nombre": user[1], "email": user[2]}), 200
        else:
            return jsonify({"message": "Usuario no encontrado"}), 404

# Endpoint para ver todos los pedidos
@app.route("/admin/pedidos", methods=["GET"])
def obtener_pedidos():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.id, u.nombre, p.total, p.estado, p.fecha
            FROM pedidos p
            JOIN usuarios u ON p.usuario_id = u.id
            ORDER BY p.fecha DESC
        ''')
        pedidos = [{
            "id": row[0],
            "usuario": row[1],
            "total": row[2],
            "estado": row[3],
            "fecha": row[4]
        } for row in cursor.fetchall()]
    return jsonify(pedidos)


# Endpoint para ver los detalles de un pedido
@app.route("/admin/pedidos/<int:id>", methods=["GET"])
def obtener_detalle_pedido(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT p.nombre, dp.cantidad, dp.subtotal
            FROM detalle_pedido dp
            JOIN productos p ON dp.producto_id = p.id
            WHERE dp.pedido_id = ?
        ''', (id,))
        productos = [{
            "producto": row[0],
            "cantidad": row[1],
            "subtotal": row[2]
        } for row in cursor.fetchall()]
    return jsonify(productos)


# Endpoint para actualizar el estado de un pedido
@app.route("/admin/pedidos/<int:id>", methods=["PUT"])
def actualizar_estado_pedido(id):
    data = request.json
    nuevo_estado = data.get("estado")
    
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pedidos
            SET estado = ?
            WHERE id = ?
        ''', (nuevo_estado, id))
        conn.commit()
    
    return jsonify({"message": "Estado del pedido actualizado"}), 200


# Endpoint para eliminar un pedido
@app.route("/admin/pedidos/<int:id>", methods=["DELETE"])
def eliminar_pedido(id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM detalle_pedido WHERE pedido_id = ?
        ''', (id,))
        cursor.execute('''
            DELETE FROM pedidos WHERE id = ?
        ''', (id,))
        conn.commit()

    return jsonify({"message": "Pedido eliminado"}), 200

# Iniciar Flask
if __name__ == "__main__":
    app.run(debug=True)
