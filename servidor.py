import socket

localPort = 8080
bufferSize = 1024 

#Criação do Socket

UDPServerSocket=socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)

# Bind com (endereço de IP local do servidor, porta do forwarding feita pelo servidor)
UDPServerSocket.bind(('192.168.0.55', localPort))

print('O servidor UDP está pronto')



while(True): 
    bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
    client_message = bytesAdressPair[0].decode('utf-8')
    address = bytesAdressPair[1]
    #Print para facilitar visualização no vídeo
    print(f"Recebeu mensagem: \"{client_message}\" do ip {address[0]} porta {address[1]}")
    #Número do ACK são os dois primeiros dígitos da mensagem enviada pelo cliente
    ACK_number = client_message[0]+client_message[1]
    #Como a contagem começa em 1 a partir desse momento o servidor manda ACKs de volta para o cliente
    if client_message[0] != '0':
        server_message = ('ACK ' + ACK_number).encode()
        UDPServerSocket.sendto(server_message,address)
        print(f"ACK {ACK_number} enviado")
    #Parada do loop quando o ACK chegar em 30
    if ACK_number=='30':
        break
#Fechameto do Socket do Servidor
UDPServerSocket.close()





   