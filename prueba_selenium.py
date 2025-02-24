from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Ruta al archivo index.html
ruta_html = "file:///C:/Users/gaelm/Desktop/style_store_website/index.html"

# Configuración del perfil de usuario para mantener localStorage
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/gaelm/SeleniumProfile")  # Ruta a perfil personalizado
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Inicializar el navegador
driver = webdriver.Chrome(options=options)

try:
    # Abrir la página
    driver.get(ruta_html)
    time.sleep(1)  # Espera inicial por si la página tarda en cargar

    # Agregar producto al carrito (para "Camisa Casual")
    agregar_btn = driver.find_element(By.XPATH, "//div[h3[text()='Camisa Casual']]//button")
    agregar_btn.click()

    # Esperar hasta que el producto aparezca en la lista del carrito
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "lista-carrito"), "Camisa Casual")
    )

    # Esperar que el total se actualice
    WebDriverWait(driver, 5).until(
        EC.text_to_be_present_in_element((By.ID, "total"), "799.00")
    )

    # Verificar que el producto se añadió al carrito
    carrito_items = driver.find_element(By.ID, "lista-carrito").text.strip()
    assert "Camisa Casual" in carrito_items, "El producto no fue agregado al carrito."

    # Verificar el total
    total = driver.find_element(By.ID, "total").text.strip()
    assert total == "799.00", f"El total es incorrecto: {total}"

    print("Prueba completada con éxito. El producto se agregó y el total es correcto.")

    # Mantener el navegador abierto hasta que el usuario decida cerrarlo
    input("Presiona ENTER para cerrar el navegador...")

except Exception as e:
    print(f"Error durante la prueba: {e}")

finally:
    driver.quit()
