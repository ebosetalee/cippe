from peewee import *


cippe_db = SqliteDatabase("cippedb.db", autorollback=True)

class BaseModel(Model):
    class Meta:
        database = cippe_db


class Recipie(BaseModel):
    id = AutoField()
    food_name = TextField(unique=True)
    description =TextField()
    top_image = TextField()
    bottom_image = TextField()
    class Meta:
        table_name = "recipies"

class Ingredient(BaseModel):
    id = AutoField()
    food_id = ForeignKeyField(Recipie, backref="ingredients")
    category = TextField()
    name = TextField()
    quantity = TextField()
    ingredient_type = TextField()
    requirement = TextField()
    size = TextField()
    class Meta:
        table_name = "ingredients"


class Step(BaseModel):
    id = AutoField()
    food_id = ForeignKeyField(Recipie, backref="steps")
    category = TextField()
    name = TextField()
    action = TextField()
    image = TextField()
    class Meta:
        table_name = "steps"

def Connector():
    return cippe_db.connect()

Connector()