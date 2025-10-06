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
        .results { background: white; padding: 20px; border-radius: 10px; max-width: 400px; margin-top: 20px; }
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
        <input type="number" step="any" name="kolicina" required>

        <label>Vnesi vrednost ene ure (€):</label>
        <input type="number" step="any" name="placa" required>

        <label>Vrsta plače:</label>
        <select name="vrsta_place">
            <option value="bruto">Bruto (pred davki)</option>
            <option value="neto">Neto (po davkih)</option>
        </select>

        <button type="submit">Izračunaj</button>
    </form>

    {% if rezultat_bruto %}
        <div class="results">
            <h3>Bruto plača: {{ rezultat_bruto }} EUR</h3>
            <h3>Neto plača: {{ rezultat_neto }} EUR</h3>
        </div>
    {% endif %}
</body>
</html>
"""

def calculate_neto_from_bruto(bruto):
    return round(bruto * 0.65, 2)

def calculate_bruto_from_neto(neto):
    return round(neto / 0.65, 2)

@app.route("/", methods=["GET", "POST"])
def home():
    rezultat_bruto = None
    rezultat_neto = None
    
    if request.method == "POST":
        nacin = request.form["nacin"]
        kolicina = float(request.form["kolicina"])
        placa = float(request.form["placa"])
        vrsta_place = request.form["vrsta_place"]

        if nacin.lower() == "d":
            base_salary = kolicina * 8 * placa
        else:
            if kolicina > 40:
                base_salary = kolicina * placa
            else:
                base_salary = kolicina * placa

        if vrsta_place == "bruto":
            rezultat_bruto = round(base_salary, 2)
            rezultat_neto = calculate_neto_from_bruto(base_salary)
        else:
            rezultat_neto = round(base_salary, 2)
            rezultat_bruto = calculate_bruto_from_neto(base_salary)

    return render_template_string(HTML_PAGE, rezultat_bruto=rezultat_bruto, rezultat_neto=rezultat_neto)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)