#Importações
import socket
import time
from threading import Thread
import msvcrt



# Inicialização dos contadores

counter_message = 0
taxa_de_perdas = 0
ACK_count = 0

#Criação de função para incrementar o contador de mensagens enviadas

def incrementcounter():
    global counter_message
    counter_message+=1


#Tupla de envio para servidor

#(ENDEREÇO DE IP PÚBLICO DO SERVIDOR, PORTA QUE FOI FEITA O FORWARDING NO SERVIDOR)

serverAddressPort = ('181.223.213.219', 8080)

#Criação do Socket 

UDPClientSocket=socket.socket(family=socket.AF_INET,type = socket.SOCK_DGRAM)


#Definição das Threads


def sendmessage():
    while True:
        incrementcounter()
        time.sleep(0.2)
        message = input('Digite sua Mensagem: ')
        final_message = str( str(counter_message)+ ' - ' + message).encode()
        UDPClientSocket.sendto(final_message,serverAddressPort)
        if counter_message%10==0 and counter_message!=30:
             print('O chat tá em modo de espera, por favor aguarde ...')
             time.sleep(10)
             #Inativar input
             while msvcrt.kbhit():
                hack = input()
        if counter_message == 30:
             print('O chat tá em modo de espera, por favor aguarde ...')
             time.sleep(10)
             while msvcrt.kbhit():
                hack = input()
             taxa_de_perdas = (1 - ACK_count/30) * 100
             print(f'Taxa de Perda de Mensagens: {round(taxa_de_perdas,2)}%')
             break
    UDPClientSocket.close()



def receivemsg():
    counter=0
    global ACK_count
    mensagem_conexao = (str(counter)+'-'+'A conexão foi estabelecida') #Mensagem de conexão com o servidor
    mensagem_conexao = mensagem_conexao.encode()
    UDPClientSocket.sendto(mensagem_conexao,serverAddressPort)
    try:
        while True:
            bytesAdressPair =  UDPClientSocket.recvfrom(1024) #Recepção de mensagens
            serverMessage = bytesAdressPair[0].decode()
            ACK_count+=1 #Incremento do contador de ACKs recebidos
            print('\n'+serverMessage)
    except:
        print('Fim de conexão.')

#Criação das Threads
sendmessage_thread = Thread(target = sendmessage)
receivemsg_thread = Thread(target = receivemsg)

#Inicialização das Threads

sendmessage_thread.start()
receivemsg_thread.start()


