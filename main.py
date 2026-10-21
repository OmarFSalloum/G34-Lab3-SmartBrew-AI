import sys
from models.user_profile import user_db
from ui.user_ui import user_menu_loop, guest_menu_loop
from ui.admin_ui import admin_menu_loop

#Initialize the mock database for users
users = user_db()

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
            print("(To tap NFC just press enter without typing anything)")
            name = input("Tap your NFC card or type a username:")
            if name in users.users:
                user_menu_loop(users.users[name.strip()])
            else:
                print("\nError: user already exists")
                input("Press ENTER to go back to the main menu")
            
        elif choice == "2":
            name = input("Choose a username: ")
            if(users.create_user(name.strip())):
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