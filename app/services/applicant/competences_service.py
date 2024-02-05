from sqlalchemy.exc import SQLAlchemyError

from app.models.applicant.competence_profile import CompetenceProfile
from app.repositories.applicant.competences_repository import \
    insert_competences_in_db


def store_applicant_competences(user_id: int, competence_id: int,
                                experience: float) -> dict[str, str]:
    """
    Store applicant competences in the database.

    This function stores the applicant's competences in the database.

    :param user_id: The ID of the user to associate the competence with.
    :param competence_id: The ID of the competence to store.
    :param experience: The years of experience in the competence.
    :returns: A dict containing the stored applicant competence information.
    :raises SQLAlchemyError: If there is an error with the database operation,
            an SQLAlchemyError is raised.
    """
    try:
        applicant_competence = CompetenceProfile(user_id, competence_id,
                                                 experience)
        insert_competences_in_db(applicant_competence)
        return __applicant_competence_to_dict(applicant_competence)
    except SQLAlchemyError as exception:
        raise exception


def __applicant_competence_to_dict(
        applicant_competence: CompetenceProfile) -> dict:
    """
    Convert an applicant competence object to a dictionary.

    This function takes an ApplicantCompetence object and converts it into a
    dictionary  containing relevant information.

    :param applicant_competence: The ApplicantCompetence object to convert.
    :returns: A dictionary representation of the applicant competence.
    """

    return {
        'person_id': applicant_competence.person_id,
        'competence_id': applicant_competence.competence_id,
        'years_of_experience': applicant_competence.years_of_experience
    }
