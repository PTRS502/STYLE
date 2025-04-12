import unittest
import sqlite3
from app import app, connect_db
import json

class TestUsuarioAPI(unittest.TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba"""
        self.app = app.test_client()  # Crea un cliente de prueba
        self.app.testing = True  # Establece el modo de prueba

        # Limpiar la base de datos antes de cada prueba
        self._limpiar_base_de_datos()

    def _limpiar_base_de_datos(self):
        """Limpiar la base de datos antes de cada prueba"""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM usuarios')  # Limpiar la tabla de usuarios
            conn.commit()

    def test_register_usuario(self):
        """Test para registrar un nuevo usuario"""
        # Datos de un nuevo usuario a registrar
        new_user = {
            "nombre": "Juan Perez",
            "email": "juanperez@ejemplo.com",
            "password": "123456"  # Contraseña sin encriptar (se encriptará en la app)
        }

        # Hacer la solicitud POST para registrar al usuario
        response = self.app.post('/usuarios', 
                                 data=json.dumps(new_user), 
                                 content_type='application/json')

        # Verificamos que la respuesta sea exitosa (código 201)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Usuario registrado exitosamente", str(response.data))

        # Verificamos que el usuario ha sido agregado a la base de datos
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nombre, email FROM usuarios WHERE email = ?', ('juanperez@ejemplo.com',))
            usuario = cursor.fetchone()

            # Verificamos que el usuario exista en la base de datos
            self.assertIsNotNone(usuario)  # El usuario debe existir
            self.assertEqual(usuario[0], 'Juan Perez')  # Verificar nombre
            self.assertEqual(usuario[1], 'juanperez@ejemplo.com')  # Verificar correo

    def test_register_existing_user(self):
        """Test para registrar un usuario con un correo ya existente"""
        # Primero, registramos un usuario con un correo
        new_user_1 = {
            "nombre": "Carlos Ruiz",
            "email": "carlosruiz@ejemplo.com",  # Correo único
            "password": "654321"
        }
        self.app.post('/usuarios', 
                      data=json.dumps(new_user_1), 
                      content_type='application/json')

        # Intentamos registrar otro usuario con el mismo correo
        new_user_2 = {
            "nombre": "Carlos García",
            "email": "carlosruiz@ejemplo.com",  # Correo duplicado
            "password": "987654"
        }

        # Intentamos registrar un nuevo usuario con un correo ya existente
        response = self.app.post('/usuarios', 
                                 data=json.dumps(new_user_2), 
                                 content_type='application/json')

        # Verificamos que la respuesta sea un error (código 400)
        self.assertEqual(response.status_code, 400)
    
        # Decodificar la respuesta JSON y verificar el mensaje
        response_json = json.loads(response.data)
        self.assertIn("El correo electrónico ya está registrado", response_json["message"])

if __name__ == '__main__':
    unittest.main()
