from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time

# Ruta al archivo index.html
ruta_html = "file:///C:/Users/gaelm/Desktop/style_store_website/index.html"

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/gaelm/SeleniumProfile")  # Ruta al perfil de usuario
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)  # Evita que el navegador se cierre automáticamente

# Inicializar el navegador
driver = webdriver.Chrome(options=options)

def handle_alert():
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = Alert(driver)
        print(f"Alerta detectada: {alert.text}")
        alert.accept()  # Acepta la alerta
        time.sleep(2)  # Asegúrate de que la alerta sea cerrada y que la página se estabilice
    except Exception as e:
        print("No se detectó alerta o error al manejarla:", e)

try:
    # Abrir la página
    print("Abriendo la página...")
    driver.get(ruta_html)
    time.sleep(2)

    # Paso 1: Registro de un usuario
    print("Iniciando el registro de usuario...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "registroBtn"))
    ).click()  # Asegúrate de que el botón tiene este ID en el HTML

    # Completar el formulario de registro
    driver.find_element(By.ID, "nombre").send_keys("Juan Perez")
    driver.find_element(By.ID, "email").send_keys("juanperez@ejemplo.com")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "registroForm").submit()
    time.sleep(2)  # Espera que el registro se procese

    # Verificar si aparece una alerta después del intento de registro
    handle_alert()  # Llama a la función para manejar cualquier alerta que aparezca

    # Paso 2: Iniciar sesión
    print("Iniciando sesión...")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "loginBtn"))
    ).click()  # Asegúrate de que el botón tiene este ID en el HTML
    driver.find_element(By.ID, "email").send_keys("juanperez@ejemplo.com")
    driver.find_element(By.ID, "password").send_keys("123456")
    driver.find_element(By.ID, "loginForm").submit()
    time.sleep(2)  # Espera que el inicio de sesión se procese

    # Verificar si aparece una alerta después del inicio de sesión
    handle_alert()

    # Verificar si la página ha sido redirigida correctamente después del inicio de sesión
    try:
        # Verifica si la página ha cambiado a una página de usuario (por ejemplo, el carrito)
        WebDriverWait(driver, 10).until(
            EC.url_changes(ruta_html)  # Asegúrate de que la URL cambie (indica redirección)
        )
        print("Redirección después del inicio de sesión detectada.")
    except Exception as e:
        print("No se detectó redirección:", e)

    # Paso 3: Agregar productos al carrito
    productos = [
        "Camisa Casual",
        "Vestido Elegante",
        "Pantalón slim de algodón para hombre",
        "Blusa damaia atelier manga larga para mujer"
    ]

    for producto in productos:
        try:
            # Buscar y hacer clic en el botón de agregar al carrito
            agregar_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[h3[text()='{producto}']]//button"))
            )
            agregar_btn.click()
            print(f"Producto '{producto}' agregado al carrito.")

            # Esperar hasta que el producto aparezca en el carrito
            WebDriverWait(driver, 5).until(
                EC.text_to_be_present_in_element((By.ID, "lista-carrito"), producto)
            )
        except Exception as e:
            print(f"No se pudo agregar el producto '{producto}': {e}")

    # Verificar el total actualizado
    try:
        total = driver.find_element(By.ID, "total").text.strip()
        print(f"Total en carrito: ${total}")
    except Exception as e:
        print(f"Error al obtener el total: {e}")

    # Eliminar un producto del carrito
    try:
        eliminar_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@id='lista-carrito']/li[1]/button"))
        )
        eliminar_btn.click()
        print("Primer producto eliminado del carrito.")

        # Esperar a que el total se actualice
        time.sleep(2)
        nuevo_total = driver.find_element(By.ID, "total").text.strip()
        print(f"Total después de eliminar un producto: ${nuevo_total}")
    except Exception as e:
        print(f"Error al eliminar un producto: {e}")

    # Mantener el navegador abierto
    input("Presiona ENTER para cerrar el navegador...")

except Exception as e:
    print(f"Error general durante la prueba: {e}")

finally:
    print("Cerrando el navegador...")
    driver.quit()
