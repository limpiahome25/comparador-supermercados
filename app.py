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
    url = f"https://www.carrefour.com.ar/search?text={q.replace(' ','%20')}"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    resultados = []

    productos = soup.select("article")  # todos los productos

    for prod in productos:
        nombre = prod.select_one(".product-name")
        precio = prod.select_one(".product-sales-price")

        if nombre and precio:
            resultados.append(
                f"{nombre.text.strip()} — {precio.text.strip()}"
            )

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
