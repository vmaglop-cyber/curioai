from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "curioai_super_secret_123"

USUARIO = "admin"
PASSWORD = "1234"

HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
  <title>CurioAI Login</title>
</head>
<body>
  <h2>CurioAI Login</h2>

  <form method="post">
    <input name="user" placeholder="Usuario" required><br><br>
    <input name="pass" type="password" placeholder="Contraseña" required><br><br>
    <button type="submit">Entrar</button>
  </form>

</body>
</html>
"""

HTML_PANEL = """
<!DOCTYPE html>
<html>
<head>
  <title>CurioAI Panel</title>
</head>
<body>

  <h1>CurioAI Panel</h1>
  <p>Bienvenido bro 😎</p>

  <form method="post" action="/generar">
    <input name="tema" placeholder="Tema de curiosidades" required>
    <button type="submit">Generar guion</button>
  </form>

  {% if guion %}
    <h3>Guion generado:</h3>
    <p>{{ guion }}</p>
  {% endif %}

  <br><br>
  <a href="/logout">Cerrar sesión</a>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("pass")

        if user == USUARIO and password == PASSWORD:
            session["logged"] = True
            return redirect("/panel")

    return render_template_string(HTML_LOGIN)

@app.route("/panel")
def panel():
    if not session.get("logged"):
        return redirect("/")
    return render_template_string(HTML_PANEL, guion=None)

@app.route("/generar", methods=["POST"])
def generar():
    if not session.get("logged"):
        return redirect("/")

    tema = request.form.get("tema")

    guion = f"""
    🔥 Curiosidad sobre {tema}:

    Este es un guion automático generado por CurioAI.
    Aquí iría contenido interesante para YouTube.
    """

    return render_template_string(HTML_PANEL, guion=guion)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)