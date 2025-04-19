import socket
import threading
import sys

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 65433
BUFFER_SIZE = 1024

def receive_messages(sock):
    """Função para receber mensagens do servidor em uma thread separada"""
    while True:
        try:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                print("\nConexão com o servidor perdida!")
                sock.close()
                sys.exit(0)  # Saída limpa
            print(data.decode('utf-8'), end='')
        except ConnectionResetError:
            print("\nConexão encerrada pelo servidor.")
            sock.close()
            sys.exit(0)  # Saída limpa
        except Exception as e:
            print(f"\nErro ao receber mensagem do servidor: {e}")
            sock.close()
            sys.exit(1)

def main():
    try:
        # Criação do socket TCP/IP
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((HOST, PORT))
            print(f"Conectado ao servidor de chat em {HOST}:{PORT}")
        except ConnectionRefusedError:
            print("Erro: Não foi possível conectar ao servidor. Verifique se o servidor está em execução.")
            return
        except socket.timeout:
            print("Erro: Tempo limite ao tentar conectar ao servidor.")
            return
        except Exception as e:
            print(f"Erro inesperado ao conectar: {e}")
            return

        # Inicia thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages, args=(s,))
        receive_thread.daemon = True
        receive_thread.start()

        # Loop principal para enviar mensagens
        while True:
            try:
                message = input()
                if message.strip() == "":
                    print("[!] Mensagem vazia não será enviada.")
                    continue

                s.send(message.encode('utf-8'))

                if message == "/quit":
                    print("[i] Enviando comando /quit e encerrando a conexão.")
                    break
            except KeyboardInterrupt:
                print("\n[i] Interrupção detectada. Enviando /quit e encerrando conexão.")
                try:
                    s.send("/quit".encode('utf-8'))
                except Exception as e:
                    print(f"Erro ao enviar /quit: {e}")
                break
            except Exception as e:
                print(f"Erro ao enviar mensagem: {e}")
                break

        s.close()
        print("[✓] Conexão encerrada.")
    except Exception as e:
        print(f"Erro fatal no cliente: {e}")

if __name__ == "__main__":
    main()
