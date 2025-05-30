import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from supabase_client import register_user, login_user, save_prompt
import openai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        result = register_user(email, password)

        if result.error:
            flash(result.error.message, "danger")
        else:
            flash("Registration successful. You can now log in.", "success")
            return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        result = login_user(email, password)

        if result.error:
            flash(result.error.message, "danger")
        else:
            session["user"] = result.user.email
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    response_text = ""
    if request.method == "POST":
        user_prompt = request.form["prompt"]
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_prompt,
                max_tokens=100
            )
            response_text = response.choices[0].text.strip()
            save_prompt(session["user"], user_prompt, response_text)
        except Exception as e:
            response_text = f"Error: {e}"

    return render_template("dashboard.html", user=session["user"], response=response_text)

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)