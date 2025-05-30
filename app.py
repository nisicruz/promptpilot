import os
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from dotenv import load_dotenv
from supabase_client import register_user, login_user
import openai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SUPABASE_KEY")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = register_user(email, password)
        if result.get("error"):
            return f"Error: {result['error']['message']}"
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        result = login_user(email, password)
        if result.get("error"):
            return f"Error: {result['error']['message']}"
        session["user"] = result['session']['access_token']
        return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html")

@app.route("/generate", methods=["POST"])
def generate():
    if "user" not in session:
        return redirect("/login")

    prompt = request.form.get("prompt")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message["content"]
        return render_template("dashboard.html", output=result, prompt=prompt)
    except Exception as e:
        return f"OpenAI error: {e}"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)
