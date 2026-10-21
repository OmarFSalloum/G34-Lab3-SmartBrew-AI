import sys
from models.user_profile import user_db
from llm_simulator import parse_natural_language_order

users = user_db()

#Import the standard menu along with inventory and waste bins
from models.data import inventory, waste_bins, standard_menu
from machine_logic.inventory_functions import get_ingredient_alerts, get_waste_alerts, refill_all_ingredients, empty_waste_bins, check_order_status, process_successful_order
from machine_logic.payment_service import process_payment

# Centralized function for browsing, customizing, and ordering
def handle_browse_and_order(active_user=None):
    print("\n--- Available Standard Menu ---")
    
    available_menu = {}
    
    # Filter the menu to only show drinks that can currently be made
    for key, drink in standard_menu.items():
        can_proceed, _ = check_order_status(inventory, waste_bins, drink["ingredients"])
        if can_proceed:
            available_menu[key] = drink
            print(f"{key}. {drink['name']}")
            
    if not available_menu:
        print("No drinks are currently available due to low stock or full waste bins.")
        return

    drink_choice = input("\nSelect a drink to view or customize: ")
    
    if drink_choice in available_menu:
        selected_drink = available_menu[drink_choice].copy()
        customization = selected_drink["customization"].copy()
        req_ingredients = selected_drink["ingredients"].copy()
        
        print(f"\n[{selected_drink['name']}]")
        print(f" - Coffee Strength: {customization['coffee_strength']}")
        print(f" - Milk Type:       {customization['milk_type']}")
        print(f" - Temperature:     {customization['temperature']}")
        print(f" - Syrup Shots:     {customization['syrup_shots']}")
        
        cust_choice = input("\nWould you like to customize this drink? (y/n): ")
        if cust_choice.lower() == 'y':
            
            # Calculate absolute maximums based on current inventory minus thresholds
            avail_beans = inventory["beans"]["current_qty"] - inventory["beans"]["min_threshold"]
            max_beans = min(5, avail_beans)
            
            avail_milk = inventory["milk"]["current_qty"] - inventory["milk"]["min_threshold"]
            
            avail_syrup = inventory["syrup"]["current_qty"] - inventory["syrup"]["min_threshold"]
            max_syrup = min(5, avail_syrup)

            # --- Coffee Strength ---
            strength = input(f"Enter coffee strength (1-{max_beans}) [{customization['coffee_strength']}]: ")
            if strength and strength.isdigit(): 
                new_strength = int(strength)
                if 1 <= new_strength <= max_beans:
                    customization['coffee_strength'] = new_strength
                    req_ingredients['beans'] = new_strength
                else:
                    print(f"Invalid amount. Keeping at {customization['coffee_strength']}.")
            
            # --- Milk Selection ---
            # Standard milk requires 5 units. If we have less than 5 available, restrict to "None".
            if avail_milk >= 5:
                print(f"\nCurrent Milk: {customization['milk_type']}")
                print("1. None")
                print("2. Whole")
                print("3. Oat")
                print("4. Almond")
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
            
            # --- Temperature ---
            print(f"\nCurrent Temperature: {customization['temperature']}")
            print("1. Hot")
            print("2. Iced")
            temp_choice = input("Select temperature (1-2) or press Enter to skip: ")
            
            if temp_choice == '1':
                customization['temperature'] = "Hot"
            elif temp_choice == '2':
                customization['temperature'] = "Iced"
            elif temp_choice != "":
                print(f"Invalid choice. Keeping at {customization['temperature']}.")
            # --- Syrup Shots ---
            syrup = input(f"Enter syrup shots (0-{max_syrup}) [{customization['syrup_shots']}]: ")
            if syrup and syrup.isdigit(): 
                new_syrup = int(syrup)
                if 0 <= new_syrup <= max_syrup:
                    customization['syrup_shots'] = new_syrup
                    req_ingredients['syrup'] = new_syrup
                else:
                    print(f"Invalid amount. Keeping at {customization['syrup_shots']}.")

        # Verify the machine can still make the customized drink
        can_proceed, message = check_order_status(inventory, waste_bins, req_ingredients)
        
        if not can_proceed:
            print(f"\n[ORDER FAILED] {message}")
        else:
            # Send the user to the payment module
            payment_successful = process_payment()
            
            if payment_successful:
                print("\n[SUCCESS] Dispensing your drink... (Not implemented)")
                process_successful_order(inventory, waste_bins, req_ingredients)
                
                # Record history and prompt to save recipe if a registered user is logged in
                if active_user:
                    active_user.record_order(selected_drink['name'])
                    save_choice = input("Would you like to save this customized recipe to your profile? (y/n): ")
                    if save_choice.lower() == 'y':
                        recipe_name = input("Enter a name for this recipe: ")
                        active_user.save_recipe(recipe_name, customization)
                        print(f"Recipe '{recipe_name}' saved to your profile!")
            else:
                print("\n[ORDER CANCELLED] Payment was not successful.")
    else:
        print("Invalid menu selection.")

def user_menu_loop(active_user):
   
    #Nested loop for the user interface. 
    #Users stay in this loop until they choose to log out.
    print("Welcome " + active_user.username + "!")

    while True:
        print("\n--- User Dashboard ---")
        print("1. Browse and Customize Drinks")
        print("2. Order Saved Custom Recipe")
        print("3. View Personalized Recommendations (Weather/Time/Mood)")
        print("4. Order via Natural-Language LLM")
        print("5. Logout")
        
        choice = input("Select an option (1-5): ")
        
        if choice == "1":
            handle_browse_and_order()
        elif choice == "2":
            print("Save and Reorder Custom Recipes: Not implemented")
            input()
        elif choice == "3":
            print("Generate Personalized/Mood Recommendations: Not implemented")
            input()
        elif choice == "4":
            print("\n--- LLM Order ---")
            prompt = input("Tell me what you're craving (e.g., 'Give me something sweet with a kick'): ")
            
            # Parse the text into a Recipe
            simulated_recipe = parse_natural_language_order(prompt)
            
            # Use the display() method from your Recipe class to show the result
            print("\nLLM parsed your request into the following instructions:")
            simulated_recipe.display()
            input()
        elif choice == "5":
            print("Logging out...")
            break  #Exits the user loop and returns to the main menu loop
        else:
            print("Invalid selection. Please try again.")
            input()

def guest_menu_loop():

    while True:
        print("\n--- Guest user Dashboard ---")
        print("1. Browse and Customize Drinks")
        print("2. Order via Natural-Language LLM")
        print("3. Exit")
            
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            print("Browse and Customize Drinks: Not implemented")
        elif choice == "2":
            print("Natural-Language Drink Ordering: Not implemented")
        elif choice == "3":
            print("Exiting...")
            break  #Exits the user loop and returns to the main menu loop
        else:
            print("Invalid selection. Please try again.")

def admin_menu_loop():
    
    #Nested loop for the admin interface.
    #Admins stay in this loop until they exit back to the main menu
    
    #Fetch active alerts
    ingredient_alerts = get_ingredient_alerts(inventory)
    waste_alerts = get_waste_alerts(waste_bins)

    #Print alerts if there are any

    if ingredient_alerts or waste_alerts:
        print("\n[ACTIVE ALERTS]")
        for alert in ingredient_alerts:
            print(f" - {alert}")
        for alert in waste_alerts:
            print(f" - {alert}")
    else:
        print("\n[System Status: OK]")

    while True:
        print("\n--- Admin Dashboard ---")
        print("\n1. Register Ingredient Refills")
        print("2. Empty Waste Bins")
        print("3. Exit Admin Mode")
        
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            refill_all_ingredients(inventory)
            print("\n[Success] All ingredients refilled to maximum capacity.")
        elif choice == "2":
            empty_waste_bins(waste_bins)
            print("\n[Success] All waste bins emptied.")
        elif choice == "3":
            print("Exiting Admin Mode...")
            break  #Exits the admin loop and returns to the main menu loop
        else:
            print("Invalid selection. Please try again.")

def main():
    
    #The main application loop (Outer Loop).
    
    while True:
        print("\n=== SmartBrew AI System ===")
        print("1. Login")
        print("2. Create Account")
        print("3. Continue as Guest")
        print("4. Admin Mode")
        print("5. Exit Simulation")
        
        choice = input("Select an option (1-4): ")
        
        if choice == "1":
            name = input("Type a username:")
            if(users.users[name]):
                user_menu_loop(users.users[name])
            else:
                print("\nError: user already exists")
                input("Press ENTER to go back to the main menu")
            
        elif choice == "2":
            name = input("Choose a username: ")
            if(users.create_user(name)):
                user_menu_loop(users.users[name])
            else:
                print("\nError: user already exists")
                input("Press ENTER to go back to the main menu")

        elif choice == "3":
            print("Guest login:")
            #Enter guest menu loop
            guest_menu_loop()
            
        elif choice == "4":
            print("Secure Administrative Access: Not implemented (Simulating successful login...)")
            #Enters the nested admin menu loop
            admin_menu_loop()
            
        elif choice == "5":
            print("Shutting down SmartBrew AI simulation. Goodbye!")
            sys.exit(0)
            
        else:
            print("Invalid selection. Please try again.")

main()