class PortfolioManager:
    def make_investment_decision(self, recommendation):
        # 根据建议做出投资决策
        if recommendation == "Buy Stock XYZ":
            return "Approve"
        return "Reject"
