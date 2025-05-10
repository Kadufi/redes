import socket
import os
import time
import sys

# Configurações do servidor
HOST = '192.168.1.8'
PORT = 9600
BUFFER_SIZE = 1024
DIRETORIO_ARQUIVOS = './arquivos_recebidos/'

# Criar diretório para salvar arquivos se não existir
os.makedirs(DIRETORIO_ARQUIVOS, exist_ok=True)

# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor de arquivos iniciado em {HOST}:{PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

# Função para receber arquivo
def receber_arquivo(nome_arquivo, endereco_cliente):
    caminho_completo = os.path.join(DIRETORIO_ARQUIVOS, nome_arquivo)
    with open(caminho_completo, 'wb') as f:
        print("Recebendo arquivo...")
        num_esperado = 0
        while True:
            pacote, addr = servidor.recvfrom(BUFFER_SIZE + 10)  # +10 para header
            if addr != endereco_cliente:
                continue

            if pacote == b'FIM':
                print("Arquivo recebido com sucesso.")
                break

            try:
                header, dados = pacote.split(b'|', 1)
                num_seq = int(header.decode())

                if num_seq == num_esperado:
                    f.write(dados)
                    servidor.sendto(f"ACK:{num_seq}".encode(), endereco_cliente)
                    num_esperado += 1
                else:
                    # ACK anterior para reenvio
                    servidor.sendto(f"ACK:{num_esperado - 1}".encode(), endereco_cliente)
            except Exception as e:
                print(f"Erro ao processar fragmento: {e}")
                servidor.sendto(b'ERRO', endereco_cliente)

# Loop principal do servidor
try:
    print("Aguardando conexões...")
    while True:
        try:
            dados, endereco = servidor.recvfrom(BUFFER_SIZE)
            mensagem = dados.decode('utf-8')

            if mensagem.startswith('ENVIAR:'):
                nome_arquivo = mensagem.split(':')[1]
                print(f"Solicitação para receber arquivo: {nome_arquivo} de {endereco}")

                servidor.sendto("PRONTO".encode('utf-8'), endereco)
                receber_arquivo(nome_arquivo, endereco)
        except Exception as e:
            print(f"Erro: {e}")
except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")
