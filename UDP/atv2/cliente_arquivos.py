import socket
import os
import sys
import time

# Configurações do cliente
SERVIDOR_HOST = 'localhost'
SERVIDOR_PORT = 9600
BUFFER_SIZE = 1024
TAMANHO_FRAGMENTO = 1000  # Tamanho de cada fragmento a ser enviado
TIMEOUT = 1.0             # Timeout para retransmissão em segundos
MAX_TENTATIVAS = 10       # Número máximo de tentativas de retransmissão

# Criar socket UDP
try:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para enviar arquivo
def enviar_arquivo(caminho_arquivo):
    inicio = time.time()  # Marca o início da transferência

    total_bytes_enviados = 0  # Para calcular a quantidade total de bytes enviados

    with open(caminho_arquivo, 'rb') as f:
        num_seq = 0
        while True:
            fragmento = f.read(TAMANHO_FRAGMENTO)
            if not fragmento:
                break

            ack_recebido = False
            tentativas = 0

            while not ack_recebido and tentativas < MAX_TENTATIVAS:
                header = f"{num_seq}|".encode()
                pacote = header + fragmento
                cliente.sendto(pacote, (SERVIDOR_HOST, SERVIDOR_PORT))
                print(f"Enviado fragmento {num_seq}")

                total_bytes_enviados += len(pacote)  # Atualiza o total de bytes enviados

                cliente.settimeout(TIMEOUT)
                try:
                    resposta, _ = cliente.recvfrom(BUFFER_SIZE)
                    resposta = resposta.decode()

                    if resposta == f"ACK:{num_seq}":
                        ack_recebido = True
                        print(f"ACK {num_seq} recebido.")
                        num_seq += 1
                    else:
                        print(f"ACK inesperado: {resposta}")
                except socket.timeout:
                    tentativas += 1
                    print(f"Timeout. Reenviando fragmento {num_seq} (tentativa {tentativas})")

            if not ack_recebido:
                print(f"Falha ao enviar fragmento {num_seq} após {MAX_TENTATIVAS} tentativas.")
                return

    # Enviar pacote de finalização
    cliente.sendto(b'FIM', (SERVIDOR_HOST, SERVIDOR_PORT))
    print("Arquivo enviado com sucesso.")

    # Marca o fim da transferência
    fim = time.time()
    tempo_total = fim - inicio
    print(f"Tempo total de transferência: {tempo_total:.2f} segundos")

    # Calcular a taxa de transferência em KB/s
    taxa_transferencia = (total_bytes_enviados / 1024) / tempo_total  # KB/s
    print(f"Taxa de transferência: {taxa_transferencia:.2f} KB/s")

# Função principal
def main():
    if len(sys.argv) != 2:
        print("Uso: python cliente_arquivos.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    # Verificar se o arquivo existe
    if not os.path.isfile(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não existe.")
        sys.exit(1)

    try:
        # Enviar solicitação inicial ao servidor
        nome_arquivo = os.path.basename(caminho_arquivo)
        solicitacao = f"ENVIAR:{nome_arquivo}"
        print(f"Solicitando envio de '{nome_arquivo}' para o servidor...")
        cliente.sendto(solicitacao.encode('utf-8'), (SERVIDOR_HOST, SERVIDOR_PORT))

        # Esperar confirmação do servidor
        cliente.settimeout(5.0)  # 5 segundos para timeout inicial
        try:
            resposta, _ = cliente.recvfrom(BUFFER_SIZE)
            if resposta.decode('utf-8') == "PRONTO":
                print("Servidor pronto para receber. Iniciando envio...")
                enviar_arquivo(caminho_arquivo)
            else:
                print(f"Resposta inesperada do servidor: {resposta.decode('utf-8')}")
        except socket.timeout:
            print("Timeout: O servidor não respondeu à solicitação inicial.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nCliente encerrado pelo usuário.")
    finally:
        cliente.close()
        print("Socket do cliente fechado.")

if __name__ == "__main__":
    main()
