# Handles the payment flow for the user
def process_payment(amount, active_user=None):

    # Automatically process payment for logged-in users via NFC/Profile
    if active_user is not None and getattr(active_user, 'username', "") != "":
        print(f"\n[Payment Gateway: Automatically charging NFC profile for {active_user.username} (Total: ${amount:.2f})...]")
        print("[SUCCESS] Payment approved.")
        return True
        
    # Loop ensures the user must pick a valid option or cancel
    while True:
        print(f"\n--- Payment Processing (Total: ${amount:.2f}) ---")
        print("1. NFC / Mobile Digital Wallet (Apple Pay/Google Pay)")
        print("2. Credit/Debit Card (Contactless)")
        print("3. Prepaid Employee Card")
        print("4. Simulate failed transaction")
        print("5. Cancel transaction")

        choice = input("Select a payment method (1-5): ")

        if choice in ["1", "2", "3"]:
            print(f"\n[Payment Gateway: Processing ${amount:.2f}... Simulating successful payment]")
            return True
        elif choice == "4":
            print("\n[Transaction failed]")
            return False
        elif choice == "5":
            print("\n[Transaction cancelled by user]")
            return False
        else:
            print("\n[Invalid selection. Please try again.]")
