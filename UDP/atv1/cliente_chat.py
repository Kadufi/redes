import socket
import threading
import sys
import time

SERVIDOR_HOST = 'localhost'
SERVIDOR_PORT = 9500
BUFFER_SIZE = 1024

try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

def receber_mensagens():
    while True:
        try:
            dados, _ = cliente.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')
            print(f"\n{mensagem}")
        except:
            break

def registrar_usuario(nome, sala):
    comando = f"/registro:{nome}:{sala}"
    cliente.sendto(comando.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

def notificar_digitando(nome):
    comando = f"/digitando:{nome}"
    cliente.sendto(comando.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

def main():
    if len(sys.argv) != 3:
        print("Uso: python cliente_chat.py <seu_nome> <nome_da_sala>")
        sys.exit(1)

    nome_usuario = sys.argv[1]
    nome_sala = sys.argv[2]

    try:
        registrar_usuario(nome_usuario, nome_sala)

        thread_recebimento = threading.Thread(target=receber_mensagens)
        thread_recebimento.daemon = True
        thread_recebimento.start()

        print(f"Conectado ao servidor na sala '{nome_sala}'. Digite '/sair' para sair.")

        while True:
            notificar_digitando(nome_usuario)
            mensagem = input()
            if mensagem.lower() == '/sair':
                cliente.sendto("/sair".encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))
                break
            else:
                cliente.sendto(mensagem.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")

if __name__ == "__main__":
    main()
