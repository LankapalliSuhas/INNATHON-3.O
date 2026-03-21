def generate_recommendations(total_power, budget_status, predicted_bill, monthly_budget, units_to_next_slab):
    recs = []

    if budget_status == "SAFE":
        recs.append("You are well within budget.")
    elif budget_status == "WARNING":
        recs.append("Usage is rising. Reduce runtime slightly to stay comfortable.")
    else:
        recs.append("Projected to exceed budget. Reduce daily usage immediately.")

    if predicted_bill > monthly_budget:
        recs.append(f"Predicted bill exceeds budget by ₹{round(predicted_bill - monthly_budget, 2)}.")

    if units_to_next_slab is not None and units_to_next_slab < 5:
        recs.append(f"You are close to the next tariff slab. Only {units_to_next_slab} units remaining.")

    if total_power < 15:
        recs.append("Current usage pattern is stable.")
    else:
        recs.append("Power draw is elevated. Consider switching off one load if not needed.")

    return recs[:3]