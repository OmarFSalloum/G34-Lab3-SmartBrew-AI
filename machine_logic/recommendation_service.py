import json
import urllib.request
from datetime import datetime

# Fetches current weather for Västerås, Sweden using Open-Meteo
def get_current_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=59.6162&longitude=16.5528&current_weather=true"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            temp = data["current_weather"]["temperature"]
            
            if temp >= 20:
                return "Warm", temp
            elif temp >= 10:
                return "Mild", temp
            else:
                return "Cold", temp
    except Exception:
        # Fallback if the API fails or there is no internet connection
        return "Unknown", 0.0

# Determines the general time of day
def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 22:
        return "Evening"
    else:
        return "Night"

# Dynamically calculates a bespoke recipe based on environment and mood
def get_recommendation(active_user=None):
    print("\n--- Personalized Recommendation ---")
    
    time_of_day = get_time_of_day()
    weather_desc, temp = get_current_weather()
    
    print(f"[Context] Time: {time_of_day} | Weather: {weather_desc} ({temp}°C)")

    # Personalize greeting using order history
    if active_user and active_user.order_history:
        recent_drink = active_user.order_history[-1]
        print(f"[History] We see you recently enjoyed a '{recent_drink}'. Let's build on that!")
    
    print("\nHow are you feeling right now?")
    print("1. Tired / Sleepy")
    print("2. Stressed / Anxious")
    print("3. Hot / Need refreshing")
    print("4. Happy / Energetic")
    
    mood_choice = input("Select your mood (1-4): ")
    
    # 1. Establish the baseline recipe
    # If the user is logged in and has preferences, start with those
    if active_user and active_user.preferences:
        strength = active_user.preferences.get("coffee_strength", 2)
        milk_type = active_user.preferences.get("milk_type", "None")
        temp_setting = active_user.preferences.get("temperature", "Hot")
        syrup = active_user.preferences.get("syrup_shots", 0)
        name = f"{active_user.username}'s Dynamic Brew"
    else:
        # Default baseline for guests
        strength = 2
        milk_type = "None"
        temp_setting = "Hot"
        syrup = 0
        name = "SmartBrew Calculated Custom"

    # 2. Apply time-of-day logic additively
    if time_of_day == "Morning":
        strength = min(5, strength + 1)
    elif time_of_day in ["Evening", "Night"]:
        strength = max(1, strength - 1)
        # Suggest oat milk for evening comfort if they normally drink black coffee
        if milk_type == "None":
            milk_type = "Oat"

    # 3. Apply weather logic
    if weather_desc == "Warm":
        temp_setting = "Iced"
    elif weather_desc == "Cold":
        temp_setting = "Hot"

    # 4. Apply mood logic cooperatively to the baseline
    if mood_choice == "1":
        strength = min(5, strength + 2)
        name = "Maximum Wake-Up Call" if not active_user else f"{active_user.username}'s Wake-Up Boost"
    elif mood_choice == "2":
        milk_type = "Whole" if milk_type == "None" else milk_type
        syrup = min(5, syrup + 2)
        name = "Comforting Sweet Brew" if not active_user else f"{active_user.username}'s Comfort Brew"
    elif mood_choice == "3":
        temp_setting = "Iced"
        syrup = min(5, syrup + 1)
        name = "Cool Refresher" if not active_user else f"{active_user.username}'s Cool Refresher"
    elif mood_choice == "4":
        syrup = min(5, syrup + 2)
        milk_type = "Oat" if milk_type == "None" else milk_type
        name = "Joyful Sweet Treat" if not active_user else f"{active_user.username}'s Joyful Treat"

    # 5. Check against saved recipes
    # If the calculated attributes perfectly match a saved recipe, use that recipe's name instead
    match_found = False
    if active_user and active_user.saved_recipes:
        for saved_name, saved_cust in active_user.saved_recipes.items():
            if (saved_cust.get("coffee_strength") == strength and 
                saved_cust.get("milk_type") == milk_type and 
                saved_cust.get("temperature") == temp_setting and
                saved_cust.get("syrup_shots") == syrup):
                
                name = saved_name
                match_found = True
                break
    
    
    # Bundle the calculated parameters into dictionaries for the checkout flow
    customization = {
        "coffee_strength": strength,
        "milk_type": milk_type,
        "temperature": temp_setting,
        "syrup_shots": syrup
    }
    
    req_ingredients = {
        "beans": strength,
        "water": 5,
        "milk": 5 if milk_type != "None" else 0,
        "syrup": syrup,
        "cups": 1
    }
    
    # Display the calculated recipe to the user just like the standard menu
    print(f"\n[Calculated Recipe: {name}]")
    if match_found:
        print("(This perfectly matches one of your saved recipes!)")
    print(f" - Coffee Strength: {customization['coffee_strength']}/5")
    print(f" - Milk Type:       {customization['milk_type']}")
    print(f" - Temperature:     {customization['temperature']}")
    print(f" - Syrup Shots:     {customization['syrup_shots']}/5")
    
    # Return as a dictionary matching the standard_menu format
    return {
        "name": name,
        "customization": customization,
        "ingredients": req_ingredients
    }