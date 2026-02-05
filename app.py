from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import shutil

app = Flask(__name__)

# -----------------------------
# DRIVER SELENIUM (RENDER SAFE)
# -----------------------------
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium"

    chromedriver_path = shutil.which("chromedriver")
    if not chromedriver_path:
        raise RuntimeError("chromedriver no encontrado")

    service = Service(chromedriver_path)

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )
    return driver


# -----------------------------
# LA GALLEGA
# -----------------------------
def buscar_lagallega(query):
    resultados = []
    driver = iniciar_driver()

    try:
        url = f"https://www.lagallega.com.ar/buscar?q={query.replace(' ', '+')}"
        driver.get(url)
        time.sleep(4)

        productos = driver.find_elements(By.CSS_SELECTOR, ".product-item")

        for p in productos:
            try:
                nombre = p.find_element(By.CSS_SELECTOR, ".product-item-name").text
                precio = p.find_element(By.CSS_SELECTOR, ".price").text
                resultados.append({
                    "nombre": nombre,
                    "precio": precio
                })
            except:
                continue

    finally:
        driver.quit()

    return resultados


# -----------------------------
# COTO
# -----------------------------
def buscar_coto(query):
    resultados = []
    driver = iniciar_driver()

    try:
        url = f"https://www.cotodigital.com.ar/sitios/cdigi/browse?q={query.replace(' ', '%20')}"
        driver.get(url)
        time.sleep(4)

        productos = driver.find_elements(By.CSS_SELECTOR, ".product-card")

        for p in productos:
            try:
                nombre = p.find_element(By.CSS_SELECTOR, ".product-card__name").text
                precio = p.find_element(By.CSS_SELECTOR, ".product-card__price").text
                resultados.append({
                    "nombre": nombre,
                    "precio": precio
                })
            except:
                continue

    finally:
        driver.quit()

    return resultados


# -----------------------------
# HOME
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    q = request.args.get("q")
    data = {}

    if q:
        data["La Gallega"] = buscar_lagallega(q)
        data["Coto"] = buscar_coto(q)

    return render_template("index.html", data=data)


# -----------------------------
# MAIN (solo local)
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
