import sys
from models.user_profile import user_db

users = user_db()
from models.data import inventory, waste_bins
from machine_logic.inventory_functions import get_ingredient_alerts, get_waste_alerts, refill_all_ingredients, empty_waste_bins

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
            print("Browse and Customize Drinks: Not implemented")
            input()
        elif choice == "2":
            print("Save and Reorder Custom Recipes: Not implemented")
            input()
        elif choice == "3":
            print("Generate Personalized/Mood Recommendations: Not implemented")
            input()
        elif choice == "4":
            print("Natural-Language Drink Ordering: Not implemented")
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