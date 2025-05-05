import subprocess
import time
import os

def run_clients(server_host, port, num_clients, workload_dir, delay=0.5):
    processes = []
    for i in range(1, num_clients + 1):
        request_file = os.path.join(workload_dir, f"client_{i}.txt")
        if not os.path.exists(request_file):
            print(f"警告：找不到 {request_file}，跳过此客户端")
            continue
        p = subprocess.Popen(["python", "client.py", server_host, str(port), request_file])
        processes.append(p)
        print(f"已启动 client_{i}.txt")
        time.sleep(delay)  # 增加延迟，避免输出太快

    for p in processes:
        p.wait()

    print("所有客户端执行完毕")

if __name__ == "__main__":
    run_clients("localhost", 8888, 10, "test-workload", delay=0.5)
