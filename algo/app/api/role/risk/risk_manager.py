class RiskManager:
    def evaluate_risk(self, decision):
        # 评估风险
        if decision == "Approve":
            return "Low Risk"
        return "High Risk"
