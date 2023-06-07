import socket
import argparse
from datetime import datetime

def scan_tcp(ip, ports, output_file):
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip, port))
        if result == 0:
            results.append(f"tcp/{port} Open")
        else:
            results.append(f"tcp/{port} Closed")
        sock.close()

    if output_file:
        with open(output_file, 'a') as file:
            file.write('\n'.join(results))
            file.write('\n')
    else:
        print('\n'.join(results))

def scan_udp(ip, ports, output_file):
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        payload = bytes('noname'.encode('utf-8'))
        sock.sendto(payload, (ip, port))
        try:
            data, _ = sock.recvfrom(1024)
            response = data.decode('utf-8').split('.')
            if len(response) == 4 and response[0] == 'ACK' and response[1] == 'NONAME':
                results.append(f"{port}/udp Open")
                results.append('.'.join(response))
            else:
                results.append(f"{port}/udp Closed")
        except socket.timeout:
            results.append(f"{port}/udp Filtered")
        sock.close()

    if output_file:
        with open(output_file, 'a') as file:
            file.write('\n'.join(results))
            file.write('\n')
    else:
        print('\n'.join(results))

def main():
    parser = argparse.ArgumentParser(description='Network Scanner')
    parser.add_argument('protocol', choices=['tcp', 'udp'], help='Type of transport protocol (TCP or UDP)')
    parser.add_argument('ip', help='IPv4 address of the target host')
    parser.add_argument('ports', nargs='+', type=int, help='Ports to scan (separated by commas)')
    parser.add_argument('--output', '-o', help='Output file')
    args = parser.parse_args()

    if args.protocol == 'tcp':
        scan_tcp(args.ip, args.ports, args.output)
    elif args.protocol == 'udp':
        scan_udp(args.ip, args.ports, args.output)

if __name__ == '__main__':
    main()