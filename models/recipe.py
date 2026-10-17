class Recipe:
    def __init__(self, name: str, coffee_strength: int, milk_type: str, milk_amount: int, temperature: str, syrup_shots: int):
        self.name = name
        self.coffee_strength = coffee_strength
        self.milk_type = milk_type
        self.milk_amount = milk_amount
        self.temperature = temperature
        self.syrup_shots = syrup_shots

    def to_dict(self):
        #Converts the recipe to a dictionary for easy storage in the session dictionaries
        return {
            "name": self.name,
            "coffee_strength": self.coffee_strength,
            "milk_type": self.milk_type,
            "milk_amount": self.milk_amount,
            "temperature": self.temperature,
            "syrup_shots": self.syrup_shots
        }

    def display(self):
        #Prints the recipe configuration in a readable format
        print(f"\n[Recipe: {self.name}]")
        print(f" - Coffee Strength: {self.coffee_strength}/5")
        print(f" - Milk:            {self.milk_amount}/5 ({self.milk_type})")
        print(f" - Temperature:     {self.temperature}")
        print(f" - Syrup Shots:     {self.syrup_shots}")