import threading
import queue

from algo.app.api.role import ResearchAnalyst

# 创建结果队列
result_queue = queue.Queue()

# 创建分析员实例
analyst = ResearchAnalyst(result_queue)

def analyst_worker():
    # 分析员生成结果并放入队列
    analyst.generate_investment_recommendation()

# 启动分析员线程，模拟异步生成结果
thread = threading.Thread(target=analyst_worker)
thread.start()

# 主线程继续执行，模拟其他业务逻辑
while True:
    try:
        # 尝试从队列中获取结果
        result = result_queue.get(timeout=2)  # 等待2秒获取结果
        print(f"Received recommendation: {result}")
        break  # 结果已经获取，退出循环
    except queue.Empty:
        print("No result yet, continue waiting...")

# 等待分析员线程完成
thread.join()
