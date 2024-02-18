from app.extensions import database


class ApplicationStatus(database.Model):  # type: ignore
    """
    Represents the status of an application in the database.

    :ivar person_id: The unique ID of the person associated with this
    application status.
    :ivar status: The current status of the application.
    """

    __tablename__ = 'application_status'

    person_id = database.Column(database.Integer, primary_key=True)
    status = database.Column(database.String)

    def __init__(self, person_id: int) -> None:
        """
        Initializes a new ApplicationStatus object.

        :param person_id: The ID of the user associated with this
        application status.
        """

        self.person_id = person_id
        self.status = 'UNHANDLED'

    def to_dict(self) -> dict:
        """
        Convert the application status to a dictionary.

        :returns: A dictionary representation of the application status.
        """
        return {
            'status': self.status
        }
