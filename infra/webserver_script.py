"""Файл для сервера."""


from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import json


class MyServer(BaseHTTPRequestHandler):
    """Создание локального вебсервера."""

    def do_POST(self):
        """Обработка POST-запроса."""
        content_length = int(self.headers.get("content-length", 0))
        res = json.loads(self.rfile.read(content_length))
        try:
            file_name = res['file_name']
            command = f"sudo bash ../../root/{res['script_name']} {file_name}"
            os.system(command)
            if res["script_name"] == "add.sh":
                move_to_container = (
                    f"cd VPN_bot/infra && sudo docker compose cp "
                    f"../../../../root/{file_name}.ovpn bot:/app/ovpn_volume/"
                    f"{file_name}.ovpn && cd ../.."
                )
                os.system(move_to_container)
        except Exception as e:
            print(e)
            self.send_response(400)
        else:
            self.send_response(200)
        finally:
            self.end_headers()


def main():
    hostName = "0.0.0.0"
    serverPort = 8080
    webServer = HTTPServer((hostName, serverPort), MyServer)
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()


if __name__ == "__main__":
    main()
