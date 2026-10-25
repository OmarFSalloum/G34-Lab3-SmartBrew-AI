from ui.menu_ui import handle_browse_menu
from ui.checkout_ui import run_checkout_flow
from machine_logic.llm_simulator import parse_natural_language_order
from machine_logic.recommendation_service import get_recommendation

def get_ingredients_from_recipe(recipe):
    """Helper function to calculate inventory cost of an LLM recipe."""
    return {
        "beans": recipe.coffee_strength,
        "water": 5, 
        "cups": 1,
        "syrup": recipe.syrup_shots,
        "milk": recipe.milk_amount
    }

def get_ingredients_from_customization(customization):
    """Helper function to calculate inventory cost of a saved dictionary recipe."""
    return {
        "beans": customization.get("coffee_strength", 2),
        "water": 5, 
        "cups": 1,
        "syrup": customization.get("syrup_shots", 0),
        "milk": 5 if customization.get("milk_type") not in ["None", None] else 0
    }

# Loop for authenticated users with profile access
def user_menu_loop(active_user):
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
            # Pass the active user so recipes can be saved to their profile
            handle_browse_menu(active_user)
        elif choice == "2":
            print("\n--- Saved Custom Recipes ---")
            
            # Check if the user has any saved recipes
            if not active_user.saved_recipes:
                print("You have no saved recipes yet.")
            else:
                # Display the recipes
                recipes = list(active_user.saved_recipes.items())
                for i, (name, cust) in enumerate(recipes):
                    print(f"{i+1}. {name} (${cust.get('price', 3.00):.2f})")
                    
                # Handle selection
                rec_choice = input("\nSelect a recipe to order (or press Enter to cancel): ")
                if rec_choice.isdigit() and 1 <= int(rec_choice) <= len(recipes):
                    selected_name, customization = recipes[int(rec_choice)-1]
                    
                    print(f"\n[Ordering: {selected_name}]")
                    # Calculate inventory requirements from the dictionary
                    req_ingredients = get_ingredients_from_customization(customization)
                    # Pass to checkout and SKIP the save prompt since it's already saved
                    run_checkout_flow(active_user, selected_name, customization, req_ingredients, prompt_save=False)
                else:
                    print("\n[Order Cancelled]")
            input("\nPress Enter to continue...")
        elif choice == "3":
            # Generate recommendation
            recommended_drink = get_recommendation(active_user)
            
            if recommended_drink:
                order_choice = input("\nWould you like to order this recommendation? (y/n): ")
                if order_choice.lower() == 'y':
                    # Send directly to the checkout flow
                    run_checkout_flow(
                        active_user, 
                        recommended_drink['name'], 
                        recommended_drink['customization'].copy(), 
                        recommended_drink['ingredients'].copy()
                    )
        elif choice == "4":
            print("\n--- LLM Order ---")
            prompt = input("Tell me what you're craving (e.g., 'Give me something sweet with a kick'): ")
            
            # Pass the text to the LLM simulator
            simulated_recipe = parse_natural_language_order(prompt)
            print("\nLLM parsed your request into the following instructions:")
            
            # Print the resulting parsed recipe
            simulated_recipe.display()
            
            # Connect the LLM order to the checkout system
            confirm = input("\nWould you like to order this drink? (y/n): ")
            if confirm.lower() == 'y':
                customization = simulated_recipe.to_dict()
                req_ingredients = get_ingredients_from_recipe(simulated_recipe)
                run_checkout_flow(active_user, simulated_recipe.name, customization, req_ingredients)
            else:
                print("\n[ORDER CANCELLED] Returning to menu.")
                
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("Logging out...")
            # Break the loop to return to the main menu
            break
        else:
            print("Invalid selection. Please try again.")
            input("Press Enter to continue...")

# Loop for unauthenticated guest users
def guest_menu_loop():
    while True:
        print("\n--- Guest user Dashboard ---")
        print("1. Browse and Customize Drinks")
        print("2. Order via Natural-Language LLM")
        print("3. View Personalized Recommendations")
        print("4. Exit")
            
        choice = input("Select an option (1-4): ")
        
        if choice == "1":
            # Pass None so the system does not try to save the recipe
            handle_browse_menu(None)
        elif choice == "2":
            print("\n--- LLM Order ---")
            prompt = input("Tell me what you're craving (e.g., 'Give me something sweet with a kick'): ")
            
            # Pass the text to the LLM simulator
            simulated_recipe = parse_natural_language_order(prompt)
            print("\nLLM parsed your request into the following instructions:")
            simulated_recipe.display()
            
            confirm = input("\nWould you like to order this drink? (y/n): ")
            if confirm.lower() == 'y':
                customization = simulated_recipe.to_dict()
                req_ingredients = get_ingredients_from_recipe(simulated_recipe)
                run_checkout_flow(None, simulated_recipe.name, customization, req_ingredients)
            else:
                print("\n[ORDER CANCELLED] Returning to menu.")
                
            input("\nPress Enter to continue...")
        elif choice == "3":
            # Generate recommendation for guest
            recommended_drink = get_recommendation(None)
            
            if recommended_drink:
                order_choice = input("\nWould you like to order this recommendation? (y/n): ")
                if order_choice.lower() == 'y':
                    # Send to checkout with None as the active user
                    run_checkout_flow(
                        None, 
                        recommended_drink['name'], 
                        recommended_drink['customization'].copy(), 
                        recommended_drink['ingredients'].copy()
                    )
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid selection. Please try again.")