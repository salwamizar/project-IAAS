from flask import Flask, render_template, request, jsonify, session, redirect
import paramiko

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

#login via ssh
def test_login(ip, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password)
        ssh.close()
        return True
    except Exception as e:
        return str(e)

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

@app.route("/login", method=["GET", "POST"])
def login():
    if request.method == "POST":
        ip = request.form.get("ip")
        username = request.form.get("username")
        password = request.form.get("password")

        login_result = test_login(ip, username, password)
        if login_result is True:
            session["ip"] = ip
            session["username"] = username
            return redirect("/dashboard")  # Redirect ke dashboard setelah login sukses
        else:
            return render_template("login.html", error="Login gagal, periksa IP, username, atau password.")


    return render_template("login.html")


@app.route("/backup")
def backup():
    return render_template("backup.html")

@app.route("/tes")
def tes():
    return render_template("tes.html")

if __name__ == "__main__":
    app.run(debug=True)