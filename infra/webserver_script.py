"""Файл для сервера.
На сервере необходимо установить python и его библиотеку outline-vpn-api.
Далее необходимо задать аргументы api_url и cert_sha256.
Далее необходимо указать порт в main.
После чего запустить скрипт.
С этого момента сервер будет отвечать на GET-запросы к этому порту и будет
возвращать новый ключ.
"""


from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from outline_vpn.outline_vpn import OutlineVPN

client = OutlineVPN(
    # Необходимо прописывать на каждом сервере
    # Также сначала необходимо установить библиотеку для Питона
    api_url="https://65.108.84.185:14918/OXMdHVcUerwYjSZB763h1w",
    cert_sha256="4A5FBF57E5E6FEF2B3066CCE1D33EAC04760F16D022144595CD712586A65CCF7",
)


class MyServer(BaseHTTPRequestHandler):
    """Создание локального вебсервера."""

    @staticmethod
    def _generate_key(key_name):
        """Создание нового ключа с заданным именем."""
        new_key = client.create_key()
        client.rename_key(new_key.key_id, key_name)
        client.delete_data_limit(new_key.key_id)
        return new_key.access_url, new_key.key_id

    @staticmethod
    def _delete_key(key_id):
        client.delete_key(key_id)

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        # Тут будет вызов скриптом для генерации ключей и формирование ответа
        # в виде ключа для Outline
        self._set_headers()
        content_length = int(self.headers.get("content-length", 0))
        response = json.loads(self.rfile.read(content_length))
        to_create = response["create"]
        if to_create:
            key_name = response["key_name"]
            key, key_id = self._generate_key(key_name)
            message = {"key": key, "key_id": key_id}
            self.wfile.write(bytes(json.dumps(message), encoding="UTF-8"))
        else:
            key_id = response["key_id"]
            self._delete_key(key_id)


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
