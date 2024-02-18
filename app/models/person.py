from app.extensions import database


class Person(database.Model):  # type: ignore
    """
    Represents a person in the database.

    :ivar person_id: The ID of the person.
    :ivar name: The name of the person.
    :ivar surname: The surname of the person.
    :ivar pnr: The personal number of the person.
    :ivar email: The email of the person.
    :ivar password: The password of the person.
    :ivar role_id: The role ID of the person.
    :ivar username: The username of the person.
    """

    __tablename__ = 'person'

    person_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
    surname = database.Column(database.String(255))
    pnr = database.Column(database.String(255))
    email = database.Column(database.String(255))
    password = database.Column(database.String(255))
    role_id = database.Column(database.Integer)
    username = database.Column(database.String(255))

    def to_dict(self) -> dict:
        """
        Convert the person to a dictionary.

        :returns: A dictionary representation of the person.
        """
        return {
            'id': self.person_id,
            'name': self.name,
            'surname': self.surname,
            'pnr': self.pnr,
            'email': self.email,
            'username': self.username,
            'role': self.role_id
        }
