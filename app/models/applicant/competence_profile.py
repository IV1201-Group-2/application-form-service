from app.extensions import database


class CompetenceProfile(database.Model):  # type: ignore
    """
    Represents a competence profile in the database.

    :ivar competence_profile_id: The unique ID of the competence profile.
    :ivar person_id: The ID of the person associated with this profile.
    :ivar competence_id: The ID of the competence associated with this profile.
    :ivar years_of_experience: The number of years of experience in the given
          competence.
    """

    __tablename__ = 'competence_profile'

    competence_profile_id = database.Column(database.Integer, primary_key=True)
    person_id = database.Column(database.Integer)
    competence_id = database.Column(database.Integer)
    years_of_experience = database.Column(
            database.Numeric(precision=4, scale=2))

    def __init__(self, person_id, competence_id, years_of_experience):
        """
        Initializes a new CompetenceProfile object.

        :param person_id: The ID of the person associated with this profile.
        :param competence_id: The ID of the competence associated with profile.
        :param years_of_experience: The number of years of experience in the
               given competence.
        """
        self.person_id = person_id
        self.competence_id = competence_id
        self.years_of_experience = years_of_experience
