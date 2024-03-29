#implementação de um servidor base para interpratação de métodos HTTP

import socket

#definindo o endereço IP do host
SERVER_HOST = ""
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 8080

#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)

#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    #pega a solicitação do cliente
    request = client_connection.recv(1024).decode()
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        print(request)
        
        #analisa a solicitação HTTP
        headers = request.split("\n")
        #print(headers)#impressão dos cabeçalhos
        #pega o nome do arquivo sendo solicitado
        filename = headers[0].split()[1]

        #verifica qual arquivo está sendo solicitado e envia a resposta para o cliente
        if filename == "/":
            filename = "/index.html"

        #try e except para tratamento de erro quando um arquivo solicitado não existir
        try:
            #abrir o arquivo e enviar para o cliente
            fin = open("htdocs" + filename)
            #leio o conteúdo do arquivo para uma variável
            content = fin.read()
            #fecho o arquivo
            fin.close()
            #envia a resposta
            response = "HTTP/1.1 200 OK\n\n" + content
        except FileNotFoundError:
            #caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
            response = "HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>"


        #envia a resposta HTTP
        client_connection.sendall(response.encode())

        client_connection.close()

server_socket.close()


