from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder=".", static_url_path="")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Serves any other file in the folder (css, js, images, etc.)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# ---- Future API routes go here, e.g.: ----
# @app.route("/api/ticks")
# def ticks():
#     return {"digit": 7}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
