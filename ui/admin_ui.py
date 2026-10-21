from models.data import inventory, waste_bins
from machine_logic.inventory_functions import get_ingredient_alerts, get_waste_alerts, refill_all_ingredients, empty_waste_bins

# Loop for the secure technician dashboard
def admin_menu_loop():
    
    # Check the data files for low stock or full bins
    ingredient_alerts = get_ingredient_alerts(inventory)
    waste_alerts = get_waste_alerts(waste_bins)

    # Display active warnings to the technician immediately
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
            # Reset all ingredient quantities back to maximum capacity
            refill_all_ingredients(inventory)
            print("\n[Success] All ingredients refilled to maximum capacity.")
        elif choice == "2":
            # Reset all waste bin quantities back to 0
            empty_waste_bins(waste_bins)
            print("\n[Success] All waste bins emptied.")
        elif choice == "3":
            print("Exiting Admin Mode...")
            # Break the loop to return to the main menu
            break 
        else:
            print("Invalid selection. Please try again.")