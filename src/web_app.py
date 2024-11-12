# Импорт встроенной библиотеки для работы веб-сервера
from http.server import BaseHTTPRequestHandler, HTTPServer

# Для начала определим настройки запуска
hostName = "localhost"  # Адрес для доступа по сети
serverPort = 8080  # Порт для доступа по сети


class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """

    def do_GET(self) -> None:
        """ Метод для обработки входящих GET-запросов """

        if self.path != '../html/contacts.html':
            self.path = '../html/contacts.html'
        try:
            with open(self.path, 'rb') as file:
                self.send_response(200)  # Отправка кода ответа
                self.send_header("Content-type", "text/html")  # Отправка типа данных, который будет передаваться
                self.end_headers()  # Завершение формирования заголовков ответа
                self.wfile.write(file.read())  # Тело ответа
        except FileNotFoundError:
            self.send_error(404, 'Файл не найден')

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        response = f"Полученные данные POST: {post_data.decode("utf-8")}"
        print(response)
        self.send_response(200)
        self.end_headers()


if __name__ == "__main__":
    # Инициализация веб-сервера, который будет по заданным параметрах в сети
    # принимать запросы и отправлять их на обработку специальному классу, который был описан выше
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Cтарт веб-сервера в бесконечном цикле прослушивания входящих запросов
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректный способ остановить сервер в консоли через сочетание клавиш Ctrl + C
        pass

    # Корректная остановка веб-сервера, чтобы он освободил адрес и порт в сети, которые занимал
    webServer.server_close()
    print("Server stopped.")
