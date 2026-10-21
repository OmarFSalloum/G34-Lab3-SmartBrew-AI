

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

# Dictionary representing the standard menu options available to all users
standard_menu = {
    "1": {
        "name": "Black Coffee",
        "ingredients": {"beans": 2, "water": 10, "milk": 0, "syrup": 0, "cups": 1},
        "customization": {"coffee_strength": 2, "milk_type": "None", "temperature": "Hot", "syrup_shots": 0}
    },
    "2": {
        "name": "Latte",
        "ingredients": {"beans": 2, "water": 5, "milk": 5, "syrup": 0, "cups": 1},
        "customization": {"coffee_strength": 2, "milk_type": "Whole", "temperature": "Hot", "syrup_shots": 0}
    },
    "3": {
        "name": "Iced Vanilla Latte",
        "ingredients": {"beans": 2, "water": 5, "milk": 5, "syrup": 2, "cups": 1},
        "customization": {"coffee_strength": 2, "milk_type": "Oat", "temperature": "Iced", "syrup_shots": 2}
    }
}