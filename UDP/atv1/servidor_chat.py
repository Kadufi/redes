import socket
import threading
import time
import sys
from datetime import datetime

HOST = '0.0.0.0'
PORT = 9500
BUFFER_SIZE = 1024

# salas = { nome_sala: { endereco: nome_usuario } }
salas = {}

# Criar socket UDP
try:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    servidor.bind((HOST, PORT))
    print(f"Servidor iniciado em {HOST}:{PORT}")
except socket.error as e:
    print(f"Erro ao criar socket: {e}")
    sys.exit(1)

def broadcast(mensagem, sala, endereco_origem=None):
    for endereco, nome in salas.get(sala, {}).items():
        if endereco != endereco_origem:
            servidor.sendto(mensagem.encode('utf-8'), endereco)

try:
    print("Aguardando mensagens...")
    while True:
        dados, endereco = servidor.recvfrom(BUFFER_SIZE)
        mensagem = dados.decode('utf-8')

        if mensagem.startswith('/registro:'):
            partes = mensagem.split(':')
            if len(partes) < 3:
                continue
            nome = partes[1].strip()
            sala = partes[2].strip()

            if sala not in salas:
                salas[sala] = {}
            salas[sala][endereco] = nome

            servidor.sendto(f"Bem-vindo à sala '{sala}', {nome}!".encode('utf-8'), endereco)
            broadcast(f"{nome} entrou na sala '{sala}'.", sala, endereco)

        elif mensagem.startswith('/sair'):
            nome = None
            sala_do_usuario = None
            for sala, membros in salas.items():
                if endereco in membros:
                    nome = membros.pop(endereco)
                    sala_do_usuario = sala
                    break
            if nome:
                print(f"{nome} saiu da sala {sala_do_usuario}")
                broadcast(f"{nome} saiu da sala.", sala_do_usuario, endereco)

        elif mensagem.startswith('/digitando:'):
            nome = mensagem.split(':')[1].strip()
            for sala, membros in salas.items():
                if endereco in membros:
                    broadcast(f"{nome} está digitando...", sala, endereco)
                    break

        elif mensagem.startswith('/pm'):
            partes = mensagem.split(' ', 2)
            if len(partes) < 3:
                continue
            _, nome_dest, msg_privada = partes
            nome_remetente = None
            for membros in salas.values():
                if endereco in membros:
                    nome_remetente = membros[endereco]
                    break
            for membros in salas.values():
                for end, nome in membros.items():
                    if nome == nome_dest:
                        servidor.sendto(f"[PM de {nome_remetente}] {msg_privada}".encode('utf-8'), end)

        else:
            for sala, membros in salas.items():
                if endereco in membros:
                    nome = membros[endereco]
                    hora = datetime.now().strftime('%H:%M:%S')
                    broadcast(f"[{hora}] {nome}: {mensagem}", sala, endereco)
                    break

except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    servidor.close()
    print("Socket do servidor fechado.")
