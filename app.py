from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ----------------------
# COTO
# ----------------------
def buscar_coto(query):
    resultados = []

    q = query.replace(" ", "%20")
    url = f"https://www.cotodigital.com.ar/sitios/cdigi/categoria?_dyncharset=utf-8&Dy=1&Ntt={q}&idSucursal=200"

    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    productos = soup.select(".atg_store_product")

    for p in productos:
        nombre = p.select_one(".product_name")
        precio = p.select_one(".atg_store_newPrice")

        if nombre and precio:
            resultados.append({
                "nombre": nombre.get_text(strip=True),
                "precio": precio.get_text(strip=True)
            })

    return resultados


# ----------------------
# CARREFOUR
# ----------------------
def buscar_carrefour(query):
    resultados = []

    q = query.replace(" ", "%20")
    url = f"https://www.carrefour.com.ar/{q}?_q={q}&map=ft"

    r = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    productos = soup.select("section.vtex-product-summary-2-x-container")

    for p in productos:
        nombre = p.select_one("span.vtex-product-summary-2-x-productBrand")
        precio = p.select_one("span.vtex-product-price-1-x-sellingPriceValue")

        if nombre and precio:
            resultados.append({
                "nombre": nombre.get_text(strip=True),
                "precio": precio.get_text(strip=True)
            })

    return resultados


# ----------------------
# HOME
# ----------------------
@app.route("/", methods=["GET"])
def home():
    q = request.args.get("q")
    data = {}

    if q:
        data["Coto"] = buscar_coto(q)
        data["Carrefour"] = buscar_carrefour(q)

    return render_template("index.html", data=data, q=q)


if __name__ == "__main__":
    app.run(debug=True)
