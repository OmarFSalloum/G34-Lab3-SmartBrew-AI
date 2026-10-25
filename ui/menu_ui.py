from models.data import inventory, waste_bins, standard_menu
from machine_logic.inventory_functions import check_order_status
from ui.customization_ui import run_customization_flow
from ui.checkout_ui import run_checkout_flow
from models.recipe import Recipe

# Displays the menu and chains the customization and checkout flows together
def handle_browse_menu(active_user=None):
    print("\n--- Available Standard Menu ---")
    
    available_menu = {}
    
    # Filter the menu to only show drinks that can currently be made
    for key, drink in standard_menu.items():
        can_proceed, _ = check_order_status(inventory, waste_bins, drink["ingredients"])
        if can_proceed:
            # Generate a temporary recipe just to calculate the true OOP price!
            cust = drink["customization"]
            temp_recipe = Recipe(
                name=drink["name"],
                coffee_strength=cust["coffee_strength"],
                milk_type=cust["milk_type"],
                milk_amount=drink["ingredients"].get("milk", 0),
                temperature=cust["temperature"],
                syrup_shots=cust["syrup_shots"]
            )
            
            # Inject the calculated price so the rest of the UI doesn't break
            drink["customization"]["price"] = temp_recipe.price
            
            available_menu[key] = drink
            print(f"{key}. {drink['name']} (${temp_recipe.price:.2f})")
            
    # Stop the process if the machine cannot make anything
    if not available_menu:
        print("No drinks are currently available due to low stock or full waste bins.")
        return

    drink_choice = input("\nSelect a drink to view or customize: ")
    
    # Proceed if the user selected a valid drink from the list
    if drink_choice in available_menu:
        
        # Create copies to prevent overwriting the base menu data
        selected_drink = available_menu[drink_choice].copy()
        customization = selected_drink["customization"].copy()
        req_ingredients = selected_drink["ingredients"].copy()
        
        # Display the default recipe parameters
        print(f"\n[{selected_drink['name']} - ${customization['price']:.2f}]")
        print(f" - Coffee Strength: {customization['coffee_strength']}")
        print(f" - Milk Type:       {customization['milk_type']}")
        print(f" - Temperature:     {customization['temperature']}")
        print(f" - Syrup Shots:     {customization['syrup_shots']}")
        
        cust_choice = input("\nWould you like to customize this drink? (y/n): ")
        if cust_choice.lower() == 'y':
            # Route to the customization module
            customization, req_ingredients = run_customization_flow(customization, req_ingredients)

        # Route to the checkout module
        run_checkout_flow(active_user, selected_drink['name'], customization, req_ingredients)
        
    else:
        print("Invalid menu selection.")