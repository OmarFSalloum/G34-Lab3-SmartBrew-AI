# Handles the payment flow for the user
def process_payment(amount, active_user=None):
    print(f"\n--- Payment Processing (Total: ${amount:.2f}) ---")
    
    print("1. NFC / Mobile Digital Wallet (Apple Pay/Google Pay)")
    print("2. Credit/Debit Card (Contactless)")
    
    # Only show the employee card option if they are logged in
    if active_user and getattr(active_user, 'username', None):
        print("3. Prepaid Employee Card (Simulation Only)")
        choice = input("Select a payment method (1-3): ")
    else:
        choice = input("Select a payment method (1-2): ")

    # Approve all valid choices without checking user funds or reducing balances
    if choice in ["1", "2", "3"]:
        print(f"\n[Payment Gateway: Processing ${amount:.2f}... Simulating successful payment]")
        return True
    else:
        print("\n[Payment Gateway: Invalid selection. Transaction failed.]")
        return False