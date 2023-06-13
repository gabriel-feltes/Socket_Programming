import socket
import argparse
from datetime import datetime

def scan_tcp(ip, portas, arquivo_saida):
    resultados = [] # Armazena os resultados da varredura
    for porta in portas:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Cria um objeto de soquete TCP
        sock.settimeout(2) # Define um tempo limite de 2 segundos para a conexão
        resultado = sock.connect_ex((ip, porta)) # Tenta conectar ao endereço IP e porta especificados
        if resultado == 0:
            resultados.append(f"tcp/{porta} Open") # Adiciona a porta aberta à lista de resultados
        else:
            resultados.append(f"tcp/{porta} Closed") # Adiciona a porta fechada à lista de resultados
        sock.close() # Fecha o soquete

    if arquivo_saida: # Se um arquivo de saída for especificado
        with open(arquivo_saida, 'a') as arquivo: # Abre o arquivo no modo de anexação
            arquivo.write('\n'.join(resultados)) # Escreve os resultados no arquivo
            arquivo.write('\n')
    else:
        print('\n'.join(resultados)) # Caso contrário, imprime os resultados na saída padrão

def scan_udp(ip, portas, arquivo_saida):
    resultados = [] # Armazena os resultados da varredura
    for porta in portas:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Cria um objeto de soquete UDP
        sock.settimeout(2) # Define um tempo limite de 2 segundos para a operação
        carga = bytes('noname'.encode('utf-8')) # Prepara uma carga útil de dados para enviar ao servidor UDP
        sock.sendto(carga, (ip, porta)) # Envia a carga útil para o endereço IP e porta especificados
        try:
            dados, _ = sock.recvfrom(1024) # Tenta receber dados de volta do servidor UDP
            resposta = dados.decode('utf-8').split('.') # Decodifica os dados recebidos e divide-os em partes separadas
            if len(resposta) == 4 and resposta[0] == 'ACK' and resposta[1] == 'NONAME': # Se a resposta for válida (ACK.NONAME.X.X)
                resultados.append(f"{porta}/udp Open") # Adiciona a porta aberta à lista de resultados
                resultados.append('.'.join(resposta)) # Adiciona a resposta completa à lista de resultados
            else:
                resultados.append(f"{porta}/udp Closed") # Adiciona a porta fechada à lista de resultados
        except socket.timeout:
            resultados.append(f"{porta}/udp Closed/Filtered") # Adiciona a porta filtrada à lista de resultados
        sock.close() # Fecha o soquete

    if arquivo_saida: # Se um arquivo de saída for especificado
        with open(arquivo_saida, 'a') as arquivo: # Abre o arquivo no modo de anexação
            arquivo.write('\n'.join(resultados))# Escreve os resultados no arquivo
            arquivo.write('\n')
    else:
        print('\n'.join(resultados)) # Caso contrário, imprime os resultados na saída padrão

def main():
    parser = argparse.ArgumentParser(description='Scanner de Rede') # Cria um objeto de análise de argumentos
    parser.add_argument('protocolo', choices=['tcp', 'udp'], help='Tipo de protocolo de transporte (TCP ou UDP)') # Adiciona um argumento obrigatório para especificar o protocolo
    parser.add_argument('ip', help='Endereço IPv4 do host de destino') # Adiciona um argumento obrigatório para especificar o endereço IP de destino
    parser.add_argument('portas', nargs='+', type=int, help='Portas a serem verificadas (separadas por vírgula)') # Adiciona um argumento obrigatório para especificar as portas a serem verificadas
    parser.add_argument('--saida', '-o', help='Arquivo de saída') # Adiciona um argumento opcional para especificar um arquivo de saída
    args = parser.parse_args() # Analisa os argumentos da linha de comando

    if args.protocolo == 'tcp':
        scan_tcp(args.ip, args.portas, args.saida) # Executa a varredura TCP
    elif args.protocolo == 'udp':
        scan_udp(args.ip, args.portas, args.saida) # Executa a varredura UDP

if __name__ == '__main__':
    main()