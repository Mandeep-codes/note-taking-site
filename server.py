import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse

NOTES_FILE = "notes.json"

def load_notes():
    try:
        with open(NOTES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as file:
        json.dump(notes, file, indent=4)

class NotesHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/notes":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(load_notes()).encode())
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == "/add_note":
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length))
            
            notes = load_notes()
            notes.append(post_data)
            save_notes(notes)
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Note added"}).encode())
    
    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path.startswith("/delete_note/"):
            try:
                note_index = int(parsed_path.path.split("/")[-1])
                notes = load_notes()
                if 0 <= note_index < len(notes):
                    notes.pop(note_index)
                    save_notes(notes)
            except ValueError:
                pass
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Note deleted"}).encode())

if __name__ == "__main__":
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, NotesHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()
