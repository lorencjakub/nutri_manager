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

    # reprezentace souborů při requestu
    def __repr__(self):
        return "<Potravina {name} ID {id}>".format(name=self.name, id=self.id)

    # detail uživatele při requestu
    def __str__(self):
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber)

    # vložení nových průřezových souborů do databáze
    @staticmethod
    def save_nutrients(**kwargs):
        f = FoodNutrients(**kwargs)

        return f
