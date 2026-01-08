from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# HTML básico para el formulario
HTML = """
<form method="post">
  Email: <input name="email"><br>
  Message: <input name="message"><br>
  <button type="submit">Send</button>
</form>
"""


# De index servir formulario estático,
# al darle al submit el evento post redirige a
# la URL de la API con el JSON estructurado
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        requests.post(
            "http://localhost:8000/publish",
            json={"email": request.form["email"], "message": request.form["message"]},
        )
    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(port=5000)  # Por defecto usamos puerto 5000, se puede modificar
