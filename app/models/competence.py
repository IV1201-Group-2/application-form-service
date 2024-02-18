from app.extensions import database


class Competence(database.Model):  # type: ignore
    """
    Represents a competence in the database.

    :ivar competence_id: The ID of the competence.
    :ivar i18n_key: The i18n key of the competence.
    """

    __tablename__ = 'competence'

    competence_id = database.Column(database.Integer, primary_key=True)
    i18n_key = database.Column(database.String(255), name='i18n-key')

    def to_dict(self) -> dict:
        """
        Converts the competence to a dictionary.

        :return: A dictionary containing the competence.
        """
        return {
            'competence_id': self.competence_id,
            'i18n-key': self.i18n_key
        }
