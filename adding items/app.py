from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

DB_NAME = "database.db"
UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------- INIT DB ----------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            image TEXT NOT NULL,
            start_bid REAL NOT NULL,
            close_bid REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- HOME ----------
@app.route('/')
def home():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    return render_template("index.html", items=items)

# ---------- ADD ITEM ----------
@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form.get('name')
    start_bid = request.form.get('start_bid')
    close_bid = request.form.get('close_bid')
    file = request.files.get('image')

    if not file or file.filename == "":
        image_path = "static/default.png"
    else:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        image_path = f"static/uploads/{filename}"

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO items (name, image, start_bid, close_bid) VALUES (?, ?, ?, ?)",
        (name, image_path, start_bid, close_bid)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)