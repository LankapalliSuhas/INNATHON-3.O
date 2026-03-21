def calculate_eco_score(total_power: float, budget_status: str, predicted_bill: float, monthly_budget: float):
    score = 100

    if total_power > 15:
        score -= 10
    if total_power > 25:
        score -= 15

    if budget_status == "WARNING":
        score -= 15
    elif budget_status == "RISK":
        score -= 30

    if predicted_bill > monthly_budget:
        score -= 15

    score = max(0, min(100, score))

    if score >= 90:
        badge = "Eco Master"
    elif score >= 75:
        badge = "Smart Saver"
    elif score >= 50:
        badge = "Average User"
    else:
        badge = "Energy Risk"

    return score, badge