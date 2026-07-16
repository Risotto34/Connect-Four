from flask import Flask, render_template
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "frontend/templates"),
    static_folder=os.path.join(BASE_DIR, "frontend/static")
)


@app.route("/")
def home():
    return render_template("index.html")


def start():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )