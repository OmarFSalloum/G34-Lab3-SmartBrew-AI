from models.data import inventory, waste_bins
from machine_logic.inventory_functions import check_order_status, process_successful_order
from machine_logic.payment_service import process_payment

# Handles final verification, payment, dispensing, and saving the recipe
def run_checkout_flow(active_user, drink_name, customization, req_ingredients):
    
    # Verify the machine can still make the customized drink
    can_proceed, message = check_order_status(inventory, waste_bins, req_ingredients)
    
    # Block the order if ingredients dropped too low
    if not can_proceed:
        print(f"\n[ORDER FAILED] {message}")
        return

    # Extract the price from the customization dictionary (default to $3.00 if missing)
    price = customization.get("price", 3.00)

    # Process the simulated payment, passing the calculated price
    payment_successful = process_payment(price, active_user)
    
    if payment_successful:
        print("\n[SUCCESS] Dispensing your drink...")
        
        # Deduct stock and add waste
        process_successful_order(inventory, waste_bins, req_ingredients)
        
        # Check if a logged-in user is making the order
        if active_user:
            active_user.record_order(drink_name)
            save_choice = input("Would you like to save this customized recipe to your profile? (y/n): ")
            
            # Save the recipe to the user profile
            if save_choice.lower() == 'y':
                recipe_name = input("Enter a name for this recipe: ")
                active_user.save_recipe(recipe_name, customization)
                print(f"Recipe '{recipe_name}' saved to your profile!")
    else:
        print("\n[ORDER CANCELLED] Payment was not successful.")