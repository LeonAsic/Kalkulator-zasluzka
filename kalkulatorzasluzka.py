from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Kalkulator plače</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        h2 { color: #333; }
        form { background: white; padding: 20px; border-radius: 10px; max-width: 400px; }
        input, select, button { width: 100%; padding: 10px; margin: 5px 0; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h2>Kalkulator plače</h2>
    <form method="POST">
        <label>Način vnosa:</label>
        <select name="nacin">
            <option value="d">Dnevi (8 ur/dan)</option>
            <option value="u">Ure</option>
        </select>

        <label>Vnesi število dni ali ur:</label>
        <input type="number" name="kolicina" required>

        <label>Vnesi vrednost ene ure (€):</label>
        <input type="number" name="placa" required>

        <button type="submit">Izračunaj</button>
    </form>

    {% if rezultat %}
        <h3>Tvoja osnovna plača je {{ rezultat }} EUR.</h3>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    rezultat = None
    if request.method == "POST":
        nacin = request.form["nacin"]
        kolicina = float(request.form["kolicina"])
        placa = float(request.form["placa"])

        if nacin.lower() == "d":
            rezultat = kolicina * 8 * placa
        else:
            if kolicina > 40:
                rezultat = kolicina * placa * 1.5
            else:
                rezultat = kolicina * placa

    return render_template_string(HTML_PAGE, rezultat=rezultat)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
