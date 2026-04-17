from flask import Flask, request, abort, send_file
from io import BytesIO
from uploadd.service import store, retrieve
from uploadd.paths import UnsafePath

app = Flask(__name__)


@app.post("/upload")
def upload():
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        abort(401)
    f = request.files.get("file")
    if f is None:
        abort(400)
    try:
        path = store(user_id, f.filename, f.read())
    except UnsafePath:
        abort(400)
    return {"stored": path}


@app.get("/files/<name>")
def download(name):
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        abort(401)
    try:
        data = retrieve(user_id, name)
    except UnsafePath:
        abort(400)
    if data is None:
        abort(404)
    return send_file(BytesIO(data), download_name=name)
