from app.extensions import database


class Competence(database.Model):  # type: ignore
    """
    Represents a competence in the database.

    :ivar competence_id: The ID of the competence.
    :ivar name: The name of the competence.
    """

    __tablename__ = 'competence'

    competence_id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255))
