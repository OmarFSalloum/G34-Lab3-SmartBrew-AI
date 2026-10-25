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
    
    print("\nHow are you feeling right now?")
    print("1. Tired / Sleepy")
    print("2. Stressed / Anxious")
    print("3. Hot / Need refreshing")
    print("4. Happy / Energetic")
    
    mood_choice = input("Select your mood (1-4): ")
    
    # Base recipe parameters before calculations
    strength = 2
    milk_type = "None"
    temp_setting = "Hot"
    syrup = 0
    name = "SmartBrew Calculated Custom"

   # 1. Apply time-of-day logic additively
    if time_of_day == "Morning":
        strength += 1
    elif time_of_day in ["Evening", "Night"]:
        strength = max(1, strength - 1)
        milk_type = "Oat"

    # 2. Apply weather logic
    if weather_desc == "Warm":
        temp_setting = "Iced"
    elif weather_desc == "Cold":
        temp_setting = "Hot"

    # 3. Apply mood logic cooperatively
    if mood_choice == "1":
        # Boosts strength on top of the time-of-day setting
        strength = min(5, strength + 2)
        name = "Maximum Wake-Up Call"
    elif mood_choice == "2":
        # Adds comfort items without reverting weather temperature
        milk_type = "Whole"
        syrup += 2
        name = "Comforting Sweet Brew"
    elif mood_choice == "3":
        # Ensures iced and adds light syrup
        temp_setting = "Iced"
        syrup += 1
        name = "Cool Refresher"
    elif mood_choice == "4":
        # Adds sweetness and oat milk for a treat
        syrup += 2
        milk_type = "Oat"
        name = "Joyful Oat Sweet Treat"
    else:
        name = "Balanced Mood Blend"
    
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