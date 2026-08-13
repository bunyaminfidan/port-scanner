import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(host, port, timeout=1):
    """Check if a single port is open on the given host."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((host, port))
    sock.close()
    return result == 0


def grab_banner(host, port, timeout=1):
    """Try to grab a service banner from an open port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))

        try:
            banner = sock.recv(1024).decode(errors="ignore").strip()
        except TimeoutError:
            banner = ""

        sock.close()
        return banner if banner else "No banner received"
    except Exception as e:  # noqa: BLE001
        return f"Error: {e}"

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
    target = "127.0.0.1"
    print(f"Scanning {target} from port 1 to 8889...\n")

    results = scan_range_threaded(target, 1, 8889)
    
    print(f"Scan complete. {len(results)} open port(s) found.\n")

    for port in results:
        banner = grab_banner(target, port)
        print(f"[+] Port {port} open — Banner: {banner}")