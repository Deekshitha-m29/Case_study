# ...existing code...
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from pathlib import Path
import os

app = Flask(__name__)

# store data in the flask instance folder (writable inside container)
FILE_PATH = Path(app.instance_path) / "motivations.txt"
os.makedirs(app.instance_path, exist_ok=True)

def load_motivations():
    if not FILE_PATH.exists():
        return []
    with FILE_PATH.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines

def save_motivation(text):
    text = (text or "").strip()
    if not text:
        return
    text = text[:500]  # limit length
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with FILE_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{ts} - {text}\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = (request.form.get("note") or "").strip()
        if note:
            save_motivation(note)
            return redirect(url_for("history"))
    return render_template("index.html")

@app.route("/history")
def history():
    notes = load_motivations()
    return render_template("history.html", notes=notes)

if __name__ == "__main__":
    # do not enable debug=True in production
    app.run(host="0.0.0.0", port=5000)
# ...existing code...