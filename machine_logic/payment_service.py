# Handles the payment flow for the user
def process_payment():
    print("\n--- Payment Processing ---")
    print("1. NFC / Mobile Digital Wallet (Apple Pay/Google Pay)")
    print("2. Credit/Debit Card (Contactless)")
    print("3. Prepaid Employee Card")
    
    choice = input("Select a payment method (1-3): ")
    
    if choice in ["1", "2", "3"]:
        print("\n[Payment Gateway: (Simulating successful payment...)]")
        return True
    else:
        print("\n[Payment Gateway: Invalid selection. Transaction failed.]")
        return False