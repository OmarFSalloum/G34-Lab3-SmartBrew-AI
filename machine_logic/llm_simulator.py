from models.recipe import Recipe

def parse_natural_language_order(user_text: str):
    """
    Simulates a local LLM agent by parsing a natural language string
    using simple keyword matching to construct a Recipe object.
    """
    text = user_text.lower()
    
    # Base defaults for a standard cup of coffee
    coffee_strength = 3
    milk_type = "Regular"
    milk_amount = 2
    temperature = "Hot"
    syrup_shots = 0
    name = "LLM Custom Brew"
    
    # 1. Analyze Coffee Strength keywords
    if any(word in text for word in ["strong", "kick", "espresso", "awake", "dark"]):
        coffee_strength = 5
        name = "Strong " + name
    elif any(word in text for word in ["weak", "mild", "light"]):
        coffee_strength = 1

    # 2. Analyze Sweetness/Syrup keywords
    if any(word in text for word in ["sweet", "sugar", "syrup", "caramel", "vanilla"]):
        syrup_shots = 2
        name = "Sweet " + name

    # 3. Analyze Temperature keywords
    if any(word in text for word in ["cold", "iced", "ice", "refreshing"]):
        temperature = "Iced"

    # 4. Analyze Milk/Dairy keywords
    if any(word in text for word in ["oat", "vegan", "plant", "no dairy", "low on dairy"]):
        milk_type = "Oat Milk"
    elif any(word in text for word in ["black", "no milk", "dark"]):
        milk_type = "None"
        milk_amount = 0
    elif any(word in text for word in ["creamy", "extra milk", "latte"]):
        milk_amount = 5

    # 5. Construct and return the Recipe (price is automatically calculated in the constructor)
    return Recipe(
        name=name.strip(),
        coffee_strength=coffee_strength,
        milk_type=milk_type,
        milk_amount=milk_amount,
        temperature=temperature,
        syrup_shots=syrup_shots
    )