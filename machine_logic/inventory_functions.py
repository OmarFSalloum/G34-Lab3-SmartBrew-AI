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

def check_order_status(inventory, waste_bins, required_ingredients):
    
    # Block order and halt operations if waste bins are full
    for bin_name, data in waste_bins.items():
        if data["current_qty"] >= data["max_capacity"]:
            return False, f"Machine halted: {bin_name} waste bin is full. Please contact a technician."
    
    # Block order if any required ingredient is depleted below minimum threshold
    for item, amount_needed in required_ingredients.items():
        if item in inventory:
            projected_qty = inventory[item]["current_qty"] - amount_needed
            if projected_qty < inventory[item]["min_threshold"]:
                return False, f"Cannot order: {item} is currently depleted."
    
    return True, "Order can proceed."

def process_successful_order(inventory, waste_bins, req_ingredients):
    #Deducts ingredients from inventory and increments waste bins.
    for item, amount in req_ingredients.items():
        if item in inventory:
            inventory[item]["current_qty"] -= amount
    
    # Every successful drink adds 1 unit of liquid and 1 unit of grounds to the waste bins
    waste_bins["liquid"]["current_qty"] += 1
    waste_bins["grounds"]["current_qty"] += 1