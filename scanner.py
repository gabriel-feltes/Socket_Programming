import socket
import argparse
from datetime import datetime

def scan_tcp(ip, portas, arquivo_saida):
    resultados = []
    for porta in portas:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        resultado = sock.connect_ex((ip, porta))
        if resultado == 0:
            resultados.append(f"tcp/{porta} Open")
        else:
            resultados.append(f"tcp/{porta} Closed")
        sock.close()

    if arquivo_saida:
        with open(arquivo_saida, 'a') as arquivo:
            arquivo.write('\n'.join(resultados))
            arquivo.write('\n')
    else:
        print('\n'.join(resultados))

def scan_udp(ip, portas, arquivo_saida):
    resultados = []
    for porta in portas:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        carga = bytes('noname'.encode('utf-8'))
        sock.sendto(carga, (ip, porta))
        try:
            dados, _ = sock.recvfrom(1024)
            resposta = dados.decode('utf-8').split('.')
            if len(resposta) == 4 and resposta[0] == 'ACK' and resposta[1] == 'NONAME':
                resultados.append(f"{porta}/udp Open")
                resultados.append('.'.join(resposta))
            else:
                resultados.append(f"{porta}/udp Closed")
        except socket.timeout:
            resultados.append(f"{porta}/udp Closed/Filtered")
        sock.close()

    if arquivo_saida:
        with open(arquivo_saida, 'a') as arquivo:
            arquivo.write('\n'.join(resultados))
            arquivo.write('\n')
    else:
        print('\n'.join(resultados))

def main():
    parser = argparse.ArgumentParser(description='Scanner de Rede')
    parser.add_argument('protocolo', choices=['tcp', 'udp'], help='Tipo de protocolo de transporte (TCP ou UDP)')
    parser.add_argument('ip', help='Endereço IPv4 do host de destino')
    parser.add_argument('portas', nargs='+', type=int, help='Portas a serem verificadas (separadas por vírgula)')
    parser.add_argument('--saida', '-o', help='Arquivo de saída')
    args = parser.parse_args()

    if args.protocolo == 'tcp':
        scan_tcp(args.ip, args.portas, args.saida)
    elif args.protocolo == 'udp':
        scan_udp(args.ip, args.portas, args.saida)

if __name__ == '__main__':
    main()