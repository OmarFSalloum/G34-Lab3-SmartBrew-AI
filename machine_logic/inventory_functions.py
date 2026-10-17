#Returns a list of strings with which ingredients are low
def get_ingredient_alerts(inventory):
    alerts = []
    for item, data in inventory.items():
        if data["current_qty"] <= data["min_threshold"] + 5:
            alerts.append(f"Low ingredient: {item} ({data['current_qty']}/{data['max_capacity']})")
    return alerts

#Returns a list of strings with which waste bins are near full
def get_waste_alerts(waste_bins):
    alerts = []
    for bin_name, data in waste_bins.items():
        # Alerts if within 5 units of max capacity
        if data["current_qty"] >= data["max_capacity"] - 5:
            alerts.append(f"Bin near full: {bin_name} ({data['current_qty']}/{data['max_capacity']})")
    return alerts

#Resets all ingredient counters back to maximum
def refill_all_ingredients(inventory):
    for item, data in inventory.items():
        inventory[item]["current_qty"] = data["max_capacity"]

#Resets waste bins back to 0
def empty_waste_bins(waste_bins):
    for bin_name, data in waste_bins.items():
        waste_bins[bin_name]["current_qty"] = 0