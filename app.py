from flask import Flask, request, send_file, render_template, redirect, url_for
import os
from crypto_utils import encrypt_file, decrypt_file

app = Flask(__name__)

STORE_DIR = "storage"
TEMP_DIR = "uploads"

os.makedirs(STORE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

@app.route("/")
def index():
    files = os.listdir(STORE_DIR)
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    data = file.read()

    encrypted = encrypt_file(data)
    enc_path = os.path.join(STORE_DIR, file.filename + ".enc")

    with open(enc_path, "wb") as f:
        f.write(encrypted)

    return redirect(url_for("index"))

@app.route("/download/<filename>")
def download(filename):
    enc_path = os.path.join(STORE_DIR, filename)

    with open(enc_path, "rb") as f:
        decrypted = decrypt_file(f.read())

    original_name = filename.replace(".enc", "")
    temp_path = os.path.join(TEMP_DIR, original_name)

    with open(temp_path, "wb") as f:
        f.write(decrypted)

    return send_file(temp_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
