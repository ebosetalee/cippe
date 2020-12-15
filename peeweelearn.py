from peewee import *


cippe_db = SqliteDatabase("cippedb.db")

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
    quantity = TextField()
    Type = TextField()
    requirements = TextField()
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

cippe_db.connect()

data = {
        "name": "Shinkafa2",
        "description": "Shinkafa (Rice Fufu)2 is a northern Nigerian fufu recipe that is prepared with the soft rice variety. It is usually served with Northern Nigerian soups: Miyan Kuka, Miyan Taushe etc. It goes well with other Nigerian Soups. The rice used for Tuwo Shinkafa should be the a soft rice variety that becomes sticky when cooked. This is so that the grains can be easily mashed to make a mass of fufu (tuwo).",
        "top image": "https://guardian.ng/wp-content/uploads/2019/07/Tuwo-Shinkafa-PHOTO-Instagram-1728x1152.jpeg",
        "bottom image": "https://scontent.flos7-1.fna.fbcdn.net/v/t1.0-9/12647352_1049780168376222_4455610281711881610_n.jpg?_nc_cat=104&ccb=2&_nc_sid=9267fe&_nc_ohc=K5Znhv7PHwAAX-JMoeL&_nc_ht=scontent.flos7-1.fna&oh=d743d21bd9f5e3b98d1b3ad3fcf2ebae&oe=5FC3E439"
        }

# Recipie.create(food_name=data["name"], description = data["description"], top_image = data["top image"], bottom_image = data["bottom image"])
# Recipie.save(self)


# query = (Step.select().where(Step.food_id == 2).dicts())
# style = []
# # print(query)
# for item in query:
#     style.append(item)
#     # print(item, "\n")
# # print(set(style))
# # print(style)
name = "Spring Roll"

query = Recipie.select().where(Recipie.food_name == name).tuples()
# print(query)
stamp = []
for ite in query:
    stamp.append(ite)
    # print(ite)
print(stamp)

# if Recipie.get(Recipie.food_name == "Shinkafa2"):
#     print("true")

Recipie.get_or_none(Recipie.food_name == "african salad")
