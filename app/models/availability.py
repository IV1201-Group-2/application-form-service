from datetime import datetime

from app.extensions import database


class Availability(database.Model):  # type: ignore
    """
    Represents availability in the database.

    :ivar availability_id: The unique ID of the availability.
    :ivar person_id: The ID of the person associated with this availability.
    :ivar from_date: The start date of the availability.
    :ivar to_date: The end date of the availability.
    """

    __tablename__ = 'availability'

    availability_id = database.Column(database.Integer, primary_key=True)
    person_id = database.Column(database.Integer)
    from_date = database.Column(database.Date)
    to_date = database.Column(database.Date)

    def __init__(self, person_id: int,
                 from_date: datetime, to_date: datetime) -> None:
        """
        Initializes a new Availability object.

        :param person_id: The ID of the user associated with this availability.
        :param from_date: The start date of the availability.
        :param to_date: The end date of the availability.
        """
        self.person_id = person_id
        self.from_date = from_date
        self.to_date = to_date

    def to_dict(self) -> dict:
        """
        Convert the availability to a dictionary.

        :returns: A dictionary representation of the availability.
        """
        return {
            'from_date': self.from_date.strftime('%Y-%m-%d'),
            'to_date': self.to_date.strftime('%Y-%m-%d')
        }
