import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

def is_port_open(host: str, port: int, timeout: float) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


def check_ports(
    host: str,
    ports: Iterable[int],
    timeout: float = 1.0,
    workers: int = 200,
) -> dict[int, bool]:
    ports_list = list(ports)
    results: dict[int, bool] = {}

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(is_port_open, host, port, timeout): port for port in ports_list}
        for future, port in futures.items():
            results[port] = future.result()

    return results

def parse_ports(arg: str) -> list[int]:
    ports: list[int] = []
    for part in arg.split(","):
        part = part.strip()
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start > end:
                start, end = end, start
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return sorted(set(ports))

def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python check_ports.py <host> <ports> [timeout_seconds] [workers]")
        print('Example: python check_ports.py 127.0.0.1 "22,80,443,8000-8010" 0.15 200')
        return 1

    host = sys.argv[1]
    ports = parse_ports(sys.argv[2])
    timeout = float(sys.argv[3]) if len(sys.argv) >= 4 else 1.0
    workers = int(sys.argv[4]) if len(sys.argv) >= 5 else 200

    if timeout <= 0:
        print("timeout_seconds must be > 0")
        return 1

    if workers <= 0:
        print("workers must be > 0")
        return 1

    results = check_ports(host, ports, timeout=timeout, workers=workers)
    for port in ports:
        status = "open" if results[port] else "closed"
        print(f"{host}:{port} {status}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())