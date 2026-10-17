class User:
    def __init__(self, username):

        self.username = username
        self.preferences = {}
        self.saved_recipes = {}
        self.order_history = []

    def save_recipe(self, recipe_name, recipe_details):
        self.saved_recipes[recipe_name] = recipe_details

    def record_order(self, drink_name):
        self.order_history.append(drink_name)

