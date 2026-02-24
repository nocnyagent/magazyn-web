from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)
PLIK = "produkty.json"


def wczytaj_produkty():
    try:
        with open(PLIK, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def zapisz_produkty(produkty):
    with open(PLIK, "w", encoding="utf-8") as f:
        json.dump(produkty, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    produkty = wczytaj_produkty()
    return render_template("index.html", produkty=produkty)


@app.route("/dodaj", methods=["POST"])
def dodaj():
    nazwa = request.form["nazwa"]
    ilosc = int(request.form["ilosc"])

    produkty = wczytaj_produkty()
    produkty.append({"nazwa": nazwa, "ilosc": ilosc})
    zapisz_produkty(produkty)

    return redirect("/")


@app.route("/usun/<int:index>")
def usun(index):
    produkty = wczytaj_produkty()
    produkty.pop(index)
    zapisz_produkty(produkty)
    return redirect("/")


@app.route("/szukaj", methods=["POST"])
def szukaj():
    fraza = request.form["fraza"].lower()
    produkty = wczytaj_produkty()
    wyniki = [p for p in produkty if fraza in p["nazwa"].lower()]
    return render_template("index.html", produkty=wyniki)


if __name__ == "__main__":
   import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)