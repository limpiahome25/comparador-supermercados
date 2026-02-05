from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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

def buscar_carrefour(q):
    url = f"https://www.carrefour.com.ar/search?text={q.replace(' ', '%20')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "es-AR,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml"
    }

    r = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    resultados = []

    for prod in soup.find_all("article"):
        nombre = prod.find("h2")
        precio = prod.find("span", {"class": "valtech-carrefourar-product-price-0-x-currencyContainer"})

        if nombre and precio:
            texto_precio = precio.get_text(strip=True)
            resultados.append(f"{nombre.get_text(strip=True)} — {texto_precio}")

    return resultados

@app.route("/")
def home():
    q = request.args.get("q")
    data = {}
    if q:
        data["Carrefour"] = buscar_carrefour(q)
        data["La Gallega"] = ["(pendiente de ajuste)"]
        data["Coto"] = ["(pendiente de ajuste)"]
    return render_template_string(HTML, data=data)

if __name__ == "__main__":

    app.run()

