import socket

def check_port(host, port, timeout=1):
    """Check if a single port is open on the given host."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def scan_range(host, start_port, end_port):
    """Scan a range of ports and return a list of open ones."""
    open_ports = []
    for port in range(start_port, end_port + 1):
        if check_port(host, port):
            print(f"[+] Port {port} is open")
            open_ports.append(port)
    return open_ports


if __name__ == "__main__":
    target = "127.0.0.1"
    print(f"Scanning {target} from port 1 to 1024...")
    results = scan_range(target, 1, 1024)
    print(f"\nScan complete. Open ports: {results}")