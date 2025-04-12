import os

# Eliminar el archivo de la base de datos
if os.path.exists("store.db"):
    os.remove("store.db")
    print("Base de datos eliminada.")
else:
    print("El archivo de la base de datos no existe.")
