from flask import Flask, render_template, request, jsonify
import paramiko

app = Flask(__name__)

# Fungsi koneksi SSH ke MikroTik
def connect_mikrotik():
    mikrotik_ip = "192.168.126.128"
    username = "admin"
    password = "123"

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(mikrotik_ip, port=22, username=username, password=password)
        return ssh
    except Exception as e:
        print(f"Gagal terhubung ke MikroTik: {e}")
        return None

# Fungsi mendapatkan daftar interface
def get_interfaces():
    ssh = connect_mikrotik()
    if ssh is None:
        return []

    command = "/interface print terse"
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()
    ssh.close()

    print(f"DEBUG OUTPUT:\n{output}")  # Tambahkan ini untuk melihat hasil asli dari MikroTik

    # Parsing nama interface dari output MikroTik
    interfaces = []
    for line in output.split("\n"):
        print(f"DEBUG LINE: {line}")  # Tambahkan ini untuk debug setiap baris
        parts = line.split()
        for part in parts:
            print(f"DEBUG PART: {part}")  # Debug tiap bagian teks
            if part.startswith("name="):
                interface_name = part.replace("name=", "").strip()
                interfaces.append(interface_name)

    print(f"DEBUG INTERFACES: {interfaces}")  # Lihat hasil akhirnya
    return interfaces

# Halaman utama
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("disable.html")

# Halaman disable interface
@app.route("/disable")
def disable():
    interfaces = get_interfaces()
    return render_template("disable.html", interfaces=interfaces)

# API untuk enable/disable interface
@app.route("/interface", methods=["POST"])
def interface():
    data = request.json
    interface = data.get("interface")
    action = data.get("action")

    if not interface or not action:
        return jsonify({"success": False, "message": "Data tidak lengkap"}), 400

    ssh = connect_mikrotik()
    if ssh is None:
        return jsonify({"success": False, "message": "Gagal terhubung ke MikroTik"}), 500

    try:
        # Pastikan format perintah benar
        command = f"/interface set [find name=\"{interface}\"] disabled={'yes' if action == 'disable' else 'no'}"
        print(f"COMMAND: {command}")  # Debugging
        stdin, stdout, stderr = ssh.exec_command(command)
        error_output = stderr.read().decode()

        if error_output:
            print(f"ERROR: {error_output}")  # Debugging
            return jsonify({"success": False, "message": f"Error dari MikroTik: {error_output}"}), 500

        ssh.close()
        return jsonify({"success": True, "message": f"Interface {interface} berhasil {action}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

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
