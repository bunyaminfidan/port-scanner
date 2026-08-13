import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(host, port, timeout=1):
    """Check if a single port is open on the given host."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def scan_port_threaded(host, port):
    """Wrapper used by threads — returns (port, is_open) tuple."""
    return port, check_port(host, port)


def scan_range_threaded(host, start_port, end_port, max_workers=100):
    """Scan a range of ports concurrently using threads."""
    open_ports = []
    ports = range(start_port, end_port + 1)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port_threaded, host, port) for port in ports]

        for future in as_completed(futures):
            port, is_open = future.result()
            if is_open:
                print(f"[+] Port {port} is open")
                open_ports.append(port)

    return sorted(open_ports)


if __name__ == "__main__":
    target = "192.168.0.180"
    print(f"Scanning {target} from port 1 to 1024...")
    results = scan_range_threaded(target, 1, 8889)
    print(f"\nScan complete. Open ports: {results}")