"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from database import db, PkModel


class CsNutriRecipes(PkModel):
    __tablename__ = "cs_nutri_recipes"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    energy = db.Column(db.Text, nullable=False)
    proteins = db.Column(db.Text, nullable=False)
    carbs = db.Column(db.Text, nullable=False)
    fats = db.Column(db.Text, nullable=False)
    fiber = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    portions = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return "<Recept {name} ID {id} recipe ID {recipe_id}>".format(
            name=self.name, id=self.id, recipe_id=self.recipe_id)

    def __str__(self) -> str:
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber} {url}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber, url=self.url)


class EnNutriRecipes(PkModel):
    __tablename__ = "en_nutri_recipes"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    energy = db.Column(db.Text, nullable=False)
    proteins = db.Column(db.Text, nullable=False)
    carbs = db.Column(db.Text, nullable=False)
    fats = db.Column(db.Text, nullable=False)
    fiber = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    portions = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return "<Recept {name} ID {id} recipe ID {recipe_id}>".format(
            name=self.name, id=self.id, recipe_id=self.recipe_id)

    def __str__(self) -> str:
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber} {url}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber, url=self.url)


class DeNutriRecipes(PkModel):
    __tablename__ = "de_nutri_recipes"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    energy = db.Column(db.Text, nullable=False)
    proteins = db.Column(db.Text, nullable=False)
    carbs = db.Column(db.Text, nullable=False)
    fats = db.Column(db.Text, nullable=False)
    fiber = db.Column(db.Text, nullable=False)
    tags = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    recipe_id = db.Column(db.Integer, nullable=False)
    portions = db.Column(db.Integer, nullable=False)

    def __repr__(self) -> str:
        return "<Recept {name} ID {id} recipe ID {recipe_id}>".format(
            name=self.name, id=self.id, recipe_id=self.recipe_id)

    def __str__(self) -> str:
        return "<{id} {name} {energy} {proteins} {carbs} {fats} {fiber} {url}>".format(
            id=self.id, name=self.name, energy=self.energy, proteins=self.proteins, carbs=self.carbs, fats=self.fats,
            fiber=self.fiber, url=self.url)
