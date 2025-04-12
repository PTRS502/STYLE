import unittest
import json
from app import app, connect_db

class TestAppIntegration(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.app = app.test_client()
        self.app.testing = True
        self._limpiar_base_de_datos()

    def _limpiar_base_de_datos(self):
        """Limpiar la base de datos antes de cada prueba"""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM productos')
            cursor.execute('DELETE FROM usuarios')
            conn.commit()

    def test_add_producto(self):
        """Test para agregar un producto"""
        new_producto = {
            "nombre": "Camisa de prueba",
            "precio": 199.99,
            "imagen": "url_imagen",
            "descripcion": "Una camisa de prueba",
            "stock": 100
        }

        response = self.app.post('/productos', 
                                 data=json.dumps(new_producto), 
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn("Producto agregado", str(response.data))

        # Verificar que el producto ha sido agregado a la base de datos
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nombre, precio FROM productos WHERE nombre = ?', ('Camisa de prueba',))
            producto = cursor.fetchone()
            self.assertIsNotNone(producto)
            self.assertEqual(producto[0], 'Camisa de prueba')
            self.assertEqual(producto[1], 199.99)

    def test_get_productos(self):
        """Test para obtener los productos"""
        # Agregar un producto
        new_producto = {
            "nombre": "Pantalón de prueba",
            "precio": 299.99,
            "imagen": "url_imagen",
            "descripcion": "Pantalón de prueba",
            "stock": 50
        }
        self.app.post('/productos', data=json.dumps(new_producto), content_type='application/json')

        # Realizar solicitud GET para obtener productos
        response = self.app.get('/productos')
        self.assertEqual(response.status_code, 200)
        productos = json.loads(response.data)
        self.assertGreater(len(productos), 0)
        self.assertEqual(productos[0]['nombre'], 'Pantalón de prueba')

    def test_delete_producto(self):
        """Test para eliminar un producto"""
        new_producto = {
            "nombre": "Pantalón de prueba",
            "precio": 299.99,
            "imagen": "url_imagen",
            "descripcion": "Pantalón de prueba",
            "stock": 50
        }
        # Agregar un producto
        response = self.app.post('/productos', data=json.dumps(new_producto), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # Obtener el ID del producto agregado
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM productos WHERE nombre = ?', ('Pantalón de prueba',))
            producto = cursor.fetchone()
            producto_id = producto[0]

        # Eliminar el producto
        response = self.app.delete(f'/productos/{producto_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f"Producto con ID {producto_id} eliminado", str(response.data))

        # Verificar que el producto haya sido eliminado
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM productos WHERE id = ?', (producto_id,))
            producto = cursor.fetchone()
            self.assertIsNone(producto)  # Verificar que el producto ya no exista

if __name__ == '__main__':
    unittest.main()
