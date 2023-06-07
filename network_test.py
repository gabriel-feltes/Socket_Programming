import socket
import argparse

def test_udp_connection(ip, ports, report_file):
    report = f"UDP Connection Test for IP: {ip}\n"
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        result = sock.connect_ex((ip, port))
        if result == 0:
            report += f"UDP Port {port}: Open\n"
        else:
            report += f"UDP Port {port}: Closed\n"
        sock.close()
    report += "\n"

    with open(report_file, "a") as file:
        file.write(report)

def test_tcp_connection(ip, ports, report_file):
    report = f"TCP Connection Test for IP: {ip}\n"
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((ip, port))
        if result == 0:
            report += f"TCP Port {port}: Open\n"
        else:
            report += f"TCP Port {port}: Closed\n"
        sock.close()
    report += "\n"

    with open(report_file, "a") as file:
        file.write(report)

def main():
    parser = argparse.ArgumentParser(description="Network Connection Tester")
    parser.add_argument("port_type", choices=["UDP", "TCP"], help="Type of port: UDP or TCP")
    parser.add_argument("ip", type=str, help="IP address to test")
    parser.add_argument("ports", type=str, help="Three comma-separated port numbers")
    parser.add_argument("report_file", type=str, help="Path to the report file")

    args = parser.parse_args()

    port_type = args.port_type.upper()
    ip = args.ip
    ports = [int(port.strip()) for port in args.ports.split(",")]
    report_file = args.report_file

    if port_type == "UDP":
        test_udp_connection(ip, ports, report_file)
    elif port_type == "TCP":
        test_tcp_connection(ip, ports, report_file)
    else:
        print("Invalid port type. Please choose either UDP or TCP.")

if __name__ == "__main__":
    main()
