from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<form method="post">
  Email: <input name="email"><br>
  Message: <input name="message"><br>
  <button type="submit">Send</button>
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        requests.post(
            "http://localhost:8000/publish",
            json={
                "email": request.form["email"],
                "message": request.form["message"]
            }
        )
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(port=5000)
