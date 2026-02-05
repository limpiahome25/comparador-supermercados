from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# =========================
# HTML SIMPLE
# =========================
HTML = """
<h2>Comparador de precios</h2>

<form method="get">
  <input name="q" placeholder="Ej: cif crema" value="{{ request.args.get('q','') }}">
  <button>Buscar</button>
</form>

{% for super, items in data.items() %}
  <h3>{{ super }}</h3>

  {% if items %}
    <ul>
    {% for i in items %}
      <li>{{ i }}</li>
    {% endfor %}
    </ul>
  {% else %}
    <p>No se encontraron resultados</p>
  {% endif %}

{% endfor %}
"""

# =========================
# SELENIUM DRIVER
# =========================
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=chrome_options
    )
    return driver

# =========================
# LA GALLEGA
# =========================
def buscar_lagallega(q):
    driver = iniciar_driver()
    url = f"https://www.lagallega.com.ar/buscar?search={q.replace(' ', '+')}"
    driver.get(url)

    time.sleep(6)  # esperar JS

    resultados = []
    productos = driver.find_elements(By.CLASS_NAME, "product-item")

    for p in productos:
        try:
            nombre = p.find_element(By.CLASS_NAME, "product-title").text
            precio = p.find_element(By.CLASS_NAME, "price").text
            resultados.append(f"{nombre} — {precio}")
        except:
            pass

    driver.quit()
    return resultados

# =========================
# COTO
# =========================
def buscar_coto(q):
    driver = iniciar_driver()
    url = f"https://www.cotodigital.com.ar/sitios/cdigi/nuevositio/buscar?Ntt={q.replace(' ', '%20')}"
    driver.get(url)

    time.sleep(7)  # esperar JS

    resultados = []
    productos = driver.find_elements(By.CLASS_NAME, "product_info_container")

    for p in productos:
        try:
            nombre = p.find_element(By.CLASS_NAME, "product_name").text
            precio = p.find_element(By.CLASS_NAME, "atg_store_newPrice").text
            resultados.append(f"{nombre} — {precio}")
        except:
            pass

    driver.quit()
    return resultados

# =========================
# ROUTE PRINCIPAL
# =========================
@app.route("/")
def home():
    q = request.args.get("q")
    data = {}

    if q:
        data["La Gallega"] = buscar_lagallega(q)
        data["Coto"] = buscar_coto(q)

    return render_template_string(HTML, data=data)

# =========================
# RUN LOCAL (Render usa gunicorn)
# =========================
if __name__ == "__main__":
    app.run()
