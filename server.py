#!/usr/bin/env python3

import os
import urllib.parse
import html
import configparser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

CONFIG_PATH = "./config.ini"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAX_UPLOAD_SIZE = 1024 * 1024 * 1024

config = configparser.ConfigParser()
if not config.read(CONFIG_PATH):
    print("Config file not found. Creating default config.ini")

    files_dir = os.path.join(BASE_DIR, "Files")

    if not os.path.exists(files_dir):
        os.makedirs(files_dir)
        print("Created default 'Files' directory.")

    config["server"] = {
        "HOSTED_DIRECTORY": os.path.join(BASE_DIR, "Files"),
        "TEMPLATE_PATH": "index.html",
        "PORT": "8000",
        "DEFAULT_BLOCK_SIZE": "128"
    }

    with open(CONFIG_PATH, "w") as f:
        config.write(f)

    print("Default config.ini created.")

HOSTED_DIRECTORY = config.get("server", "HOSTED_DIRECTORY")
TEMPLATE_PATH = os.path.join(BASE_DIR, config.get("server", "TEMPLATE_PATH"))
PORT = config.getint("server", "PORT")
DEFAULT_BLOCK_SIZE = config.getint("server", "DEFAULT_BLOCK_SIZE")

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HOSTED_DIRECTORY, **kwargs)

    def list_directory(self, path):

        try:
            entries = os.listdir(path)
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        entries.sort(key=lambda a: a.lower())

        displaypath = html.escape(urllib.parse.unquote(self.path))
        hosted_dir_name = os.path.basename(HOSTED_DIRECTORY)

        file_entries = []
        for name in entries:
            fullname = os.path.join(path, name)
            display_name = name
            link_name = name

            if os.path.isdir(fullname):
                display_name = name + ""
                link_name = name + "/"

            file_entries.append(
                f'<li><a class="file-button" href="{urllib.parse.quote(link_name)}">{html.escape(display_name)}</a></li>'
            )

        file_list_html = "\n".join(file_entries)

        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                template = f.read()
        except FileNotFoundError:
            self.send_error(500, "Template file not found")
            return None

        content = template.replace("{{ path }}", displaypath)
        content = content.replace("{{ files }}", file_list_html)
        content = content.replace("{{ hosted_directory }}", hosted_dir_name)

        encoded = content.encode("utf-8", "surrogateescape")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()

        self.wfile.write(encoded)
        return None

    def send_head(self):

        path = self.translate_path(self.path)

        if os.path.isdir(path):
            return self.list_directory(path)

        if not os.path.exists(path):
            self.send_error(404, "File not found")
            return None

        ctype = self.guess_type(path)

        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None

        file_size = os.fstat(f.fileno()).st_size
        range_header = self.headers.get("Range")

        if range_header:

            bytes_range = range_header.strip().split("=")[1]
            range_start, range_end = bytes_range.split("-")

            start = int(range_start) if range_start else 0
            end = int(range_end) if range_end else file_size - 1

            if end >= file_size:
                end = file_size - 1

            content_length = end - start + 1

            self.send_response(206)
            self.send_header("Content-Type", ctype)
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            self.send_header("Content-Length", str(content_length))
            self.end_headers()

            f.seek(start)
            self.copy_file_range(f, self.wfile, content_length)
            f.close()
            return None

        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(file_size))
        self.send_header("Accept-Ranges", "bytes")
        self.end_headers()

        return f

    def copy_file_range(self, source, outputfile, length):

        remaining = length
        while remaining > 0:
            read_length = min(DEFAULT_BLOCK_SIZE, remaining)
            buf = source.read(read_length)
            if not buf:
                break
            outputfile.write(buf)
            remaining -= len(buf)

    def do_POST(self):
        path = self.translate_path(self.path)

        if not os.path.isdir(path):
            self.send_error(400, "Upload target is not a directory")
            return

        content_length = int(self.headers.get('Content-Length', 0))

        if content_length > MAX_UPLOAD_SIZE:
            self.send_error(413, "File too large (max 1GB)")
            return

        content_type = self.headers.get("Content-Type")
        if not content_type or "multipart/form-data" not in content_type:
            self.send_error(400, "Invalid content type")
            return

        boundary = content_type.split("boundary=")[-1].encode()
        boundary = b"--" + boundary

        remaining = content_length
        line = self.rfile.readline()
        remaining -= len(line)

        if boundary not in line:
            self.send_error(400, "Content does not start with boundary")
            return

        line = self.rfile.readline()
        remaining -= len(line)

        disposition = line.decode()
        if "filename=" not in disposition:
            self.send_error(400, "No file uploaded")
            return

        filename = disposition.split("filename=")[-1].strip()
        filename = filename.strip('"')
        filename = os.path.basename(filename)

        line = self.rfile.readline()
        remaining -= len(line)

        line = self.rfile.readline()
        remaining -= len(line)

        file_path = os.path.join(path, filename)

        try:
            with open(file_path, "wb") as output_file:
                prev_line = self.rfile.readline()
                remaining -= len(prev_line)

                while remaining > 0:
                    line = self.rfile.readline()
                    remaining -= len(line)

                    if boundary in line:
                        output_file.write(prev_line.rstrip(b"\r\n"))
                        break
                    else:
                        output_file.write(prev_line)
                        prev_line = line

        except OSError:
            self.send_error(500, "Failed to save file")
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Upload successful")

def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler)
    print(f"Serving {HOSTED_DIRECTORY} at http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run()
