class User:
    def __init__(self, username, nfc_id=None):
        self.username = username
        self.nfc_id = nfc_id  # Stores the simulated NFC chip ID
        self.preferences = {}
        self.saved_recipes = {}
        self.order_history = []

    def save_recipe(self, recipe_name, recipe_details):
        self.saved_recipes[recipe_name] = recipe_details

    def record_order(self, drink_name):
        self.order_history.append(drink_name)

class user_db:
    def __init__(self):
        # Initialize the database with Alice
        alice = User("Alice", nfc_id="NFC-A1")
        alice.save_recipe("Alice's Morning Kick", {
            "coffee_strength": 5,
            "milk_type": "None",
            "temperature": "Hot",
            "syrup_shots": 0,
            "price": 3.50
        })

        # Initialize the database with Bob
        bob = User("Bob", nfc_id="NFC-B2")
        bob.save_recipe("Bob's Sweet Treat", {
            "coffee_strength": 2,
            "milk_type": "Oat",
            "temperature": "Iced",
            "syrup_shots": 3,
            "price": 6.50
        })
        
        self.users = {
            "Alice": alice,
            "Bob": bob,
            "" : User("")
        }
        
    def create_user(self, name):
        if name in self.users:
            return False
        self.users[name] = User(name)
        return True

    def find_by_nfc(self, nfc_id):
        """Searches the database for a matching NFC ID."""
        for user in self.users.values():
            if user.nfc_id == nfc_id:
                return user
        return None