# client.py
import socket
import sys
import os

def format_request(op, key, value=""):
    msg = f"{op} {key} {value}".strip()
    return f"{len(msg)+4:03} {msg}"

def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <host> <port> <request_file>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    filepath = sys.argv[3]

    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" ", 2)
                if len(parts) < 2:
                    print(f"{line}: ERR malformed")
                    continue
                op = parts[0].upper()
                key = parts[1]
                value = parts[2] if len(parts) == 3 else ""

                if len(f"{key} {value}") > 970:
                    print(f"{line}: ERR too long")
                    continue

                if op not in ("PUT", "GET", "READ"):
                    print(f"{line}: ERR unknown op")
                    continue

                cmd = {"PUT": "P", "GET": "G", "READ": "R"}[op]
                msg = format_request(cmd, key, value)
                s.sendall(msg.encode())
                response = s.recv(1024).decode().strip()
                print(f"{line}: {response}")

if __name__ == "__main__":
    main()
