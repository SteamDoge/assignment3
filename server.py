import socket
import threading
import time

# 全局 tuple space 和锁
tuple_space = {}
space_lock = threading.Lock()

# 处理一个客户端连接
def handle_client(conn, addr):
    print(f"[+] 客户端已连接：{addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            request = data.decode().strip()
            print(f"[Request] {addr} → {request}")
            parts = request.split(' ', 2)
            cmd = parts[0].upper()
            key = parts[1] if len(parts) > 1 else ""
            val = parts[2] if len(parts) > 2 else ""
            
            with space_lock:
                if cmd == "PUT" and key:
                    if key in tuple_space:
                        resp = f"ERR {key} already exists"
                    else:
                        tuple_space[key] = val
                        resp = f"OK ({key}, {val}) added"
                elif cmd == "GET" and key:
                    if key in tuple_space:
                        old = tuple_space.pop(key)
                        resp = f"OK ({key}, {old}) removed"
                    else:
                        resp = f"ERR {key} does not exist"
                elif cmd == "READ" and key:
                    if key in tuple_space:
                        resp = f"OK ({key}, {tuple_space[key]}) read"
                    else:
                        resp = f"ERR {key} does not exist"
                else:
                    resp = "ERR invalid command"
            
            # 发送响应
            conn.sendall((resp + "\n").encode())

    print(f"[-] 客户端已断开：{addr}")

# 定时打印 summary
def summary():
    while True:
        time.sleep(10)
        with space_lock:
            n = len(tuple_space)
            avgk = (sum(len(k) for k in tuple_space) / n) if n else 0
            avgv = (sum(len(v) for v in tuple_space.values()) / n) if n else 0
        print(f"\n=== SUMMARY ===\nTuples: {n}, Avg key: {avgk:.1f}, Avg val: {avgv:.1f}\n================\n")

def main():
    HOST, PORT = "localhost", 51234

    threading.Thread(target=summary, daemon=True).start()
    with socket.socket() as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] 服务器启动，监听 {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
