# Handles the payment flow for the user
def process_payment(active_user = None):

    # Automatically process payment for logged-in users via NFC/Profile
    if active_user is not None and active_user.username != "":
            print(f"\n[Payment Gateway: Automatically charging NFC profile for {active_user.username}...]")
            print("[SUCCESS] Payment approved.")
            return True
        
    # Loop ensures the user must pick a valid option or cancel
    while True:
        print("\n--- Payment Processing ---")
        print("1. NFC / Mobile Digital Wallet (Apple Pay/Google Pay)")
        print("2. Credit/Debit Card (Contactless)")
        print("3. Prepaid Employee Card")
        print("4. Simulate failed transaction")
        print("5. Cancel transaction")

        choice = input("Select a payment method (1-5): ")

        if choice in ["1", "2", "3"]:
            print("\n[Payment Gateway: (Simulating successful payment...)]")
            return True
        elif choice in ["4"]:
            print("\[Transation failed]")
            return False
        elif choice == "5":
            print("\n[Transaction cancelled by user]")
            return False
        else:
            print("\n[Invalid selection. Please try again.]")