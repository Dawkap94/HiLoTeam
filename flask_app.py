import subprocess
from os import path

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/run_script", methods=["POST"])
def run_script():
    if request.method == "POST":
        if not path.exists("./keys"):
            try:
                # Uruchamianie skryptu pythona ssh_generator.py
                subprocess.run(["python3", "ssh_generator.py"], check=True)
                with open("keys/ssh_id.pub") as public_key:
                    public_key = public_key.read()
                return render_template("keys_success.html", public_key=public_key)
            except subprocess.CalledProcessError as e:
                return f"Błąd podczas generowania kluczy: {e}"
        else:
            with open("keys/ssh_id.pub") as public_key:
                public_key = public_key.read()
            return render_template("keys_success.html", public_key=public_key)
    return "Naciśnij przycisk, aby uruchomić skrypt."


if __name__ == "__main__":
    app.run()
