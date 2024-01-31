from app.extensions import database


class Person(database.Model):
    __tablename__ = 'person'

    person_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    surname = database.Column(database.String(255))
    pnr = database.Column(database.String(255))
    email = database.Column(database.String(255))
    password = database.Column(database.String(255))
    role_id = database.Column(database.Integer)
    username = database.Column(database.String(255))
