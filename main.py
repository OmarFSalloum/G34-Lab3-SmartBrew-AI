import sys
from models.user_profile import User
from models.data import user_db

def user_menu_loop(active_user):
   
    #Nested loop for the user interface. 
    #Users stay in this loop until they choose to log out.
    print("Welcome " + active_user + "!")

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
        elif choice == "2":
            print("Save and Reorder Custom Recipes: Not implemented")
        elif choice == "3":
            print("Generate Personalized/Mood Recommendations: Not implemented")
        elif choice == "4":
            print("Natural-Language Drink Ordering: Not implemented")
        elif choice == "5":
            print("Logging out...")
            break  #Exits the user loop and returns to the main menu loop
        else:
            print("Invalid selection. Please try again.")

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
    

    while True:
        print("\n--- Admin Dashboard ---")
        print("1. Register Ingredient Refills")
        print("2. Monitor Waste and Coffee-Ground Bins")
        print("3. Exit Admin Mode")
        
        choice = input("Select an option (1-3): ")
        
        if choice == "1":
            print("Register Ingredient Refills: Not implemented")
        elif choice == "2":
            print("Monitor Waste and Coffee-Ground Bins: Not implemented")
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
            if(user_db[name]):
                user_menu_loop(name)
            
        elif choice == "2":
            print("Create User Account: Not implemented")

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