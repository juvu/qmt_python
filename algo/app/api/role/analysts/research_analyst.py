import time


class ResearchAnalyst:
    def __init__(self, result_queue):
        self.result_queue = result_queue

    def generate_investment_recommendation(self):
        # 模拟生成投资建议的过程
        recommendation = "Buy Stock XYZ"

        # 将结果放入队列中
        self.result_queue.put(recommendation)

        # 模拟某些耗时操作
        time.sleep(1)

        return recommendation
