import socket

SERVER_HOST = ""
SERVER_PORT = 8080


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 


server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

print("+-----------------------------------------------------------------+")
print("| Servidor em execução...")
print("| Escutando por conexões na porta %s" % SERVER_PORT)
print("+-----------------------------------------------------------------+")


while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    if request:
        print("| -> Request: ")
        print()
        print(request)

        headers = request.split("\n")
        print("Headers", headers)
        method = headers[0].split()[0]
        print("| -> method: ", method)

        filename = headers[0].split()[1]
        print("| -> filename: ", filename)

        if method == "GET":

            if filename == "/":
                filename = "/index.html"


            try:
                requested_file = open("htdocs" + filename)
                content = requested_file.read()
                requested_file.close()

                response = "HTTP/1.1 200 OK\n\n" + content
            except FileNotFoundError:
                response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
        elif method == "PUT":
            try:
                requested_file = open("htdocs" + filename, "w")
                requested_file.write(headers[-1])
                requested_file.close()
                print("| -> file content:")
                print(headers[-1])
                response = "HTTP/1.1 201 Created\n\n<h1>File Created!</h1>"
            except FileNotFoundError:
                response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"
        else:
            response = "HTTP/1.1 405 METHOD NOT ALLOWED\n\n<h1>ERROR 405!<br>Method Not Allowed!</h1>"


        #envia a resposta HTTP
        client_connection.sendall(response.encode())

        client_connection.close()
        print("| -> Connection closed!")
        print("+-----------------------------------------------------------------+")

server_socket.close()
