import main_run

db = main_run.db


class FoodNutrients(db.Model):
    __tablename__ = "food_nutrients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    energy = db.Column(db.Text, nullable=False)
    proteins = db.Column(db.Text, nullable=False)
    carbs = db.Column(db.Text, nullable=False)
    fats = db.Column(db.Text, nullable=False)
    fiber = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Potravina {name} ID {id}>".format(name=self.name, id=self.id)

    def __str__(self):
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber)

    @staticmethod
    def save_nutrients(**kwargs):
        f = FoodNutrients(**kwargs)

        return f


class NutriRecipes(db.Model):
    __tablename__ = "nutri_recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    energy = db.Column(db.Text, nullable=False)
    proteins = db.Column(db.Text, nullable=False)
    carbs = db.Column(db.Text, nullable=False)
    fats = db.Column(db.Text, nullable=False)
    fiber = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    procedure = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "<Recept {name} ID {id}>".format(name=self.name, id=self.id)

    def __str__(self):
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber)

    @staticmethod
    def save_recipes(**kwargs):
        r = NutriRecipes(**kwargs)

        return r
