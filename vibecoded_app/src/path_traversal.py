#!/usr/bin/env python3
"""
Vulnerable Python code with Path Traversal examples
FOR SAST TESTING ONLY - DO NOT RUN IN PRODUCTION
"""

import os
import pathlib

from flask import Flask, request, send_file

app = Flask(__name__)


# VULNERABLE: Direct file access with user input
@app.route("/file")
def get_file():
    filename = request.args.get("file", "index.html")

    # CRITICAL VULNERABILITY: No path validation
    file_path = f"/var/www/files/{filename}"

    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "File not found", 404


# VULNERABLE: Path traversal with os.path.join
def vulnerable_file_access():
    user_file = request.args.get("file", "")

    # CRITICAL VULNERABILITY: User input in path construction
    base_path = "/var/www/uploads/"
    full_path = os.path.join(base_path, user_file)

    with open(full_path, "r") as f:
        return f.read()


# VULNERABLE: Directory listing with path traversal
@app.route("/list")
def list_directory():
    directory = request.args.get("dir", ".")

    # CRITICAL VULNERABILITY: User input in directory path
    path = f"/var/www/{directory}"

    try:
        files = os.listdir(path)
        return str(files)
    except OSError:
        return "Directory not found", 404


# VULNERABLE: File upload with path traversal
@app.route("/upload")
def upload_file():
    filename = request.form.get("filename", "")
    content = request.form.get("content", "")

    # CRITICAL VULNERABILITY: User input in file path
    upload_path = f"/var/www/uploads/{filename}"

    with open(upload_path, "w") as f:
        f.write(content)

    return "File uploaded"


# VULNERABLE: Path traversal with pathlib
def vulnerable_pathlib_access():
    user_path = request.args.get("path", "")

    # CRITICAL VULNERABILITY: User input in Path object
    file_path = pathlib.Path(f"/var/www/{user_path}")

    if file_path.exists():
        return file_path.read_text()
    return "File not found"


# VULNERABLE: File inclusion vulnerability
@app.route("/include")
def include_file():
    template = request.args.get("template", "default.html")

    # CRITICAL VULNERABILITY: User input in include path
    include_path = f"/var/www/templates/{template}"

    try:
        with open(include_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Template not found", 404


# VULNERABLE: Directory traversal with chdir
def vulnerable_chdir():
    directory = request.args.get("dir", ".")

    # CRITICAL VULNERABILITY: User input in chdir
    os.chdir(f"/var/www/{directory}")

    files = os.listdir(".")
    return str(files)


# VULNERABLE: File deletion with path traversal
@app.route("/delete")
def delete_file():
    filename = request.args.get("file", "")

    # CRITICAL VULNERABILITY: User input in delete path
    file_path = f"/var/www/files/{filename}"

    try:
        os.remove(file_path)
        return "File deleted"
    except OSError:
        return "File not found", 404


# VULNERABLE: File copy with path traversal
def vulnerable_file_copy():
    source = request.args.get("source", "")
    destination = request.args.get("dest", "")

    # CRITICAL VULNERABILITY: User input in copy paths
    source_path = f"/var/www/{source}"
    dest_path = f"/var/www/{destination}"

    import shutil

    shutil.copy2(source_path, dest_path)


# VULNERABLE: File move with path traversal
def vulnerable_file_move():
    source = request.args.get("source", "")
    destination = request.args.get("dest", "")

    # CRITICAL VULNERABILITY: User input in move paths
    source_path = f"/var/www/{source}"
    dest_path = f"/var/www/{destination}"

    import shutil

    shutil.move(source_path, dest_path)


if __name__ == "__main__":
    app.run(debug=True)
