class Trader:
    def execute_trade(self, risk_evaluation):
        # 执行交易
        if risk_evaluation == "Low Risk":
            print("Trade executed: Bought Stock XYZ")
        else:
            print("Trade not executed due to high risk")
