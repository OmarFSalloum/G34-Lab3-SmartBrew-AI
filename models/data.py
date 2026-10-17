

# Dictionary representing the machine's inventory state
inventory = {
    "beans": {"current_qty": 50, "min_threshold": 10, "max_capacity": 100},
    "milk": {"current_qty": 50, "min_threshold": 10, "max_capacity": 100},
    "water": {"current_qty": 50, "min_threshold": 10, "max_capacity": 100},
    "syrup": {"current_qty": 20, "min_threshold": 5, "max_capacity": 50},
    "cups": {"current_qty": 20, "min_threshold": 2, "max_capacity": 20}
}

# Dictionary representing the machine's waste bins
waste_bins = {
    "liquid": {"current_qty": 0, "max_capacity": 20},
    "grounds": {"current_qty": 0, "max_capacity": 20}
}