from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

try:
    # Abrir la página
    driver.get(ruta_html)
    time.sleep(2)

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
    driver.quit()
