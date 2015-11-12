from peewee import *

db = SqliteDatabase("sexton.db")

class BaseModel(Model):
    class Meta:
        database = db # uses sexton.db

class Person(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    connection = CharField(null=True)
    employer = CharField(null=True)
    role = CharField(null=True)
    city = CharField(null=True)
    contact = CharField(null=True)
    notes = TextField(null=True)
    tags = TextField(null=True)

    def __dict__(self):
            person_dict = {}
            person_dict['id'] = self.id
            person_dict['name'] = self.name
            person_dict['employer'] = self.employer
            person_dict['role'] = self.role
            person_dict['connection'] = self.connection
            person_dict['contact'] = self.contact
            person_dict['notes'] = self.notes
            person_dict['tags'] = self.tags
            person_dict['score'] = 0
            return person_dict

class User(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(unique=True, max_length=12)
    password = CharField(max_length=12)

def initialize_db():
    db.connect()
    db.create_tables([Person, User], safe=True)
