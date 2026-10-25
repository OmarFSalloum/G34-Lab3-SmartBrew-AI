from models.data import inventory

def calculate_dynamic_price(req_ingredients, customization):
    """Calculates the price of the drink based on its ingredients."""
    base_price = 1.00 # Flat cup/water base fee
    base_price += req_ingredients.get('beans', 0) * 0.50
    base_price += req_ingredients.get('syrup', 0) * 0.50
    
    milk_type = customization.get('milk_type', 'None')
    if milk_type in ['Oat', 'Almond']:
        base_price += 1.00 # Premium milk surcharge
    elif milk_type == 'Whole':
        base_price += 0.50
        
    return base_price

# Handles the interactive prompts for modifying a drink's parameters
def run_customization_flow(customization, req_ingredients):
    
    # Calculate the maximum ingredients the user can add based on current stock
    avail_beans = inventory["beans"]["current_qty"] - inventory["beans"]["min_threshold"]
    max_beans = min(5, avail_beans)
    
    avail_milk = inventory["milk"]["current_qty"] - inventory["milk"]["min_threshold"]
    
    avail_syrup = inventory["syrup"]["current_qty"] - inventory["syrup"]["min_threshold"]
    max_syrup = min(5, avail_syrup)

    # Customize coffee strength
    strength = input(f"Enter coffee strength (1-{max_beans}) [{customization['coffee_strength']}]: ")
    if strength and strength.isdigit(): 
        new_strength = int(strength)
        if 1 <= new_strength <= max_beans:
            customization['coffee_strength'] = new_strength
            req_ingredients['beans'] = new_strength
        else:
            print(f"Invalid amount. Keeping at {customization['coffee_strength']}.")
    
    # Customize milk type if enough milk is available
    if avail_milk >= 5:
        print(f"\nCurrent Milk: {customization['milk_type']}")
        print("1. None\n2. Whole\n3. Oat\n4. Almond")
        milk_choice = input("Select milk type (1-4) or press Enter to skip: ")
        
        if milk_choice == '1':
            customization['milk_type'] = "None"
            req_ingredients['milk'] = 0
        elif milk_choice == '2':
            customization['milk_type'] = "Whole"
            req_ingredients['milk'] = 5
        elif milk_choice == '3':
            customization['milk_type'] = "Oat"
            req_ingredients['milk'] = 5
        elif milk_choice == '4':
            customization['milk_type'] = "Almond"
            req_ingredients['milk'] = 5
        elif milk_choice != "":
            print(f"Invalid choice. Keeping at {customization['milk_type']}.")
    else:
        print("\nInsufficient milk stock. Milk type locked to 'None'.")
        customization['milk_type'] = "None"
        req_ingredients['milk'] = 0
    
    # Customize temperature
    print(f"\nCurrent Temperature: {customization['temperature']}")
    print("1. Hot\n2. Iced")
    temp_choice = input("Select temperature (1-2) or press Enter to skip: ")
    
    if temp_choice == '1':
        customization['temperature'] = "Hot"
    elif temp_choice == '2':
        customization['temperature'] = "Iced"
    elif temp_choice != "":
        print(f"Invalid choice. Keeping at {customization['temperature']}.")
    
    # Customize syrup shots
    syrup = input(f"Enter syrup shots (0-{max_syrup}) [{customization['syrup_shots']}]: ")
    if syrup and syrup.isdigit(): 
        new_syrup = int(syrup)
        if 0 <= new_syrup <= max_syrup:
            customization['syrup_shots'] = new_syrup
            req_ingredients['syrup'] = new_syrup
        else:
            print(f"Invalid amount. Keeping at {customization['syrup_shots']}.")

    # Dynamically calculate the new price
    new_price = calculate_dynamic_price(req_ingredients, customization)
    customization['price'] = new_price
    print(f"\n[Updated Price: ${new_price:.2f}]")

    # Return the updated drink configuration
    return customization, req_ingredients