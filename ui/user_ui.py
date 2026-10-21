from ui.menu_ui import handle_browse_menu
from machine_logic.llm_simulator import parse_natural_language_order

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
            print("Save and Reorder Custom Recipes: Not implemented")
            input()
        elif choice == "3":
            print("Generate Personalized/Mood Recommendations: Not implemented")
            input()
        elif choice == "4":
            print("\n--- LLM Order ---")
            prompt = input("Tell me what you're craving (e.g., 'Give me something sweet with a kick'): ")
            
            # Pass the text to the LLM simulator
            simulated_recipe = parse_natural_language_order(prompt)
            print("\nLLM parsed your request into the following instructions:")
            
            # Print the resulting parsed recipe
            simulated_recipe.display()
            input()
        elif choice == "5":
            print("Logging out...")
            # Break the loop to return to the main menu
            break
        else:
            print("Invalid selection. Please try again.")
            input()

# Loop for unauthenticated guest users
def guest_menu_loop():
    while True:
        print("\n--- Guest user Dashboard ---")
        print("1. Browse and Customize Drinks")
        print("2. Order via Natural-Language LLM")
        print("3. Exit")
            
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            # Pass None so the system does not try to save the recipe
            handle_browse_menu(None)
        elif choice == "2":
            print("Natural-Language Drink Ordering: Not implemented")
        elif choice == "3":
            print("Exiting...")
            # Break the loop to return to the main menu
            break
        else:
            print("Invalid selection. Please try again.")