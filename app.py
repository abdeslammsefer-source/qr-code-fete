from flask import Flask, request, render_template_string, send_file
import qrcode
import io

app = Flask(__name__)

TICKETS = []  # liste pour stocker les infos des gens

html_form = """
<h2>Créer ton QR</h2>
<form method="post">
  Nom: <input type="text" name="nom"><br>
  Prénom: <input type="text" name="prenom"><br>
  Téléphone: <input type="text" name="tel"><br>
  <input type="submit" value="Générer le QR">
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {
            "nom": request.form["nom"],
            "prenom": request.form["prenom"],
            "tel": request.form["tel"]
        }
        TICKETS.append(data)
        qr_data = f"{data['nom']} {data['prenom']} | {data['tel']}"
        img = qrcode.make(qr_data)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')
    return render_template_string(html_form)

@app.route("/liste")
def liste():
    return {"tickets": TICKETS}

if __name__ == "__main__":
    app.run(debug=True)