# server.py
import socket
import threading
import time

tuple_space = {}  # 共享空间：key -> value
stats = {
    "clients": 0,
    "ops": 0,
    "reads": 0,
    "gets": 0,
    "puts": 0,
    "errors": 0
}
lock = threading.Lock()

def format_response(status, key, value="", op=""):
    if status == "OK":
        return f"{len(f'OK ({key}, {value}) {op}')+4:03} OK ({key}, {value}) {op}"
    else:
        msg = f"{key} {value}"
        return f"{len(f'ERR {msg}')+4:03} ERR {msg}"

def handle_client(conn, addr):
    global stats
    with conn:
        with lock:
            stats["clients"] += 1
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                msg = data.decode().strip()
                if len(msg) < 5:
                    continue
                _, cmd, rest = msg[0:3], msg[4], msg[6:]
                parts = rest.split(" ", 1)
                key = parts[0]
                value = parts[1] if len(parts) > 1 else ""

                response = ""
                with lock:
                    stats["ops"] += 1
                    if cmd == "R":
                        stats["reads"] += 1
                        if key in tuple_space:
                            response = format_response("OK", key, tuple_space[key], "read")
                        else:
                            stats["errors"] += 1
                            response = format_response("ERR", key, "does not exist")
                    elif cmd == "G":
                        stats["gets"] += 1
                        if key in tuple_space:
                            val = tuple_space.pop(key)
                            response = format_response("OK", key, val, "removed")
                        else:
                            stats["errors"] += 1
                            response = format_response("ERR", key, "does not exist")
                    elif cmd == "P":
                        stats["puts"] += 1
                        if key in tuple_space:
                            stats["errors"] += 1
                            response = format_response("ERR", key, "already exists")
                        else:
                            tuple_space[key] = value
                            response = format_response("OK", key, value, "added")
                    else:
                        continue
                conn.sendall(response.encode() + b"\n")
            except Exception as e:
                print("Error:", e)
                break

def summary_thread():
    while True:
        time.sleep(10)
        with lock:
            count = len(tuple_space)
            total_key = sum(len(k) for k in tuple_space)
            total_val = sum(len(v) for v in tuple_space.values())
            print(f"\n--- Server Summary ---")
            print(f"Tuples: {count}")
            print(f"Avg key size: {total_key / count if count else 0:.2f}")
            print(f"Avg val size: {total_val / count if count else 0:.2f}")
            print(f"Total clients: {stats['clients']}")
            print(f"Total ops: {stats['ops']}, READs: {stats['reads']}, GETs: {stats['gets']}, PUTs: {stats['puts']}, ERRs: {stats['errors']}")
            print(f"----------------------\n")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        return
    port = int(sys.argv[1])
    host = "0.0.0.0"

    threading.Thread(target=summary_thread, daemon=True).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on port {port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
