from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        ssid = request.form.get("ssid")
        password = request.form.get("password")

        pass
    return render_template("index.html")

@app.route("/disable")
def disable():
    return render_template("disable.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/backup")
def backup():
    return render_template("backup.html")

@app.route("/tes")
def tes():
    return render_template("tes.html")

if __name__ == "__main__":
    app.run(debug=True)