from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from ai_model import predict_waste

app = Flask(__name__)
app.secret_key = "smartwaste123"


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ---------------- #

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("waste.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(fullname,email,username,password)
        VALUES(?,?,?,?)
        """, (fullname, email, username, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ---------------- #

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("waste.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT * FROM users
        WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Invalid Username or Password"

    return render_template("login.html")


# ---------------- DASHBOARD ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template("dashboard.html", user=session["user"])


# ---------------- CLASSIFY ---------------- #

@app.route("/classify")
def classify():

    if "user" not in session:
        return redirect("/login")

    return render_template("classify.html")


# ---------------- PREDICT ---------------- #

@app.route("/predict", methods=["POST"])
def predict():

    if "user" not in session:
        return redirect("/login")

    if "image" not in request.files:
        return "No image uploaded"

    image = request.files["image"]

    if image.filename == "":
        return "Please select an image"

    upload_folder = "static/uploads"

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, image.filename)
    image.save(filepath)

    # AI Simulation
    prediction, tip = predict_waste(filepath)

    return render_template(
        "result.html",
        prediction=prediction,
        tip=tip,
        image=filepath
    )


# ---------------- LOGOUT ---------------- #

@app.route("/logout")
def logout():

    session.pop("user", None)
    return redirect("/")


# ---------------- RUN ---------------- #

if __name__ == "__main__":
    app.run(debug=True)