import socket
import time
import os

# 默认服务器配置
SERVER_HOST = "localhost"
SERVER_PORT = 51234
WORKLOAD_DIR = "test-workload"


def send_request(request: str) -> str:
    """发送单条请求到服务器，并返回响应字符串"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_HOST, SERVER_PORT))
            s.send(request.encode())
            return s.recv(4096).decode().strip()
    except Exception as e:
        return f"ERR sending request: {e}"


def main():
    # 检查工作负载目录是否存在
    if not os.path.isdir(WORKLOAD_DIR):
        print(f"工作负载目录不存在：{WORKLOAD_DIR}")
        return

    # 查找并排序所有 client_*.txt 文件
    files = sorted(
        [f for f in os.listdir(WORKLOAD_DIR)
         if f.startswith("client_") and f.endswith(".txt")]
    )

    if not files:
        print(f"在目录 {WORKLOAD_DIR} 中未找到任何 client_*.txt 文件。")
        return

    # 依次处理每个请求文件
    for filename in files:
        path = os.path.join(WORKLOAD_DIR, filename)
        print(f"\n>>> 开始处理文件：{path}")
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                request = line.strip()
                if not request:
                    continue
                # 发送并打印响应
                response = send_request(request)
                print(f"{request}  →  {response}")
                time.sleep(0.2)  # 请求间延时，可根据需要调整


if __name__ == "__main__":
    main()
