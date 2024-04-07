import socket

SERVER_HOST = ""
SERVER_PORT = 8080


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 


server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.listen(1)

def handle_content_type(filename):
    file_extension = filename.split('.')[1]

    if file_extension == "html":
        return "text/html"
    elif file_extension == "css":
        return "text/css"
    elif file_extension == "js":
        return "text/javascript"
    elif file_extension == "jpg" or file_extension == "jpeg":
        return "image/jpeg"
    elif file_extension == "png":
        return "image/png"
    elif file_extension == "gif":
        return "image/gif"
    else:
        return "application/octet-stream"

print("+-----------------------------------------------------------------+")
print("| Servidor em execução...")
print("| Escutando por conexões na porta %s" % SERVER_PORT)
print("+-----------------------------------------------------------------+")


while True:
    client_connection, client_address = server_socket.accept()
    print(f"Uma conexão com {client_address} foi estabelecida!")

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
                requested_file = open("htdocs" + filename, "rb")
                content = requested_file.read()
                requested_file.close()

                content_type = handle_content_type(filename)

                response = f"HTTP/1.1 200 OK\nContent-Type: {content_type}\n\n".encode() + content
            except FileNotFoundError:
                response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>".encode()
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

        if method == "GET":
            client_connection.sendall(response)
        else:
            client_connection.sendall(response.encode())

        client_connection.close()
        print("| -> Conexão Fechada!")
        print("+-----------------------------------------------------------------+")

server_socket.close()
