#!/usr/bin/env python3
"""
DB module for interacting with the database.
"""

from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from user import Base, User


class DB:
    """
    DB class for handling database operations.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance, setting up the database and session.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object for database interactions.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.
        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by arbitrary keyword arguments.

        Returns:
            User: The first User object found that matches the filter.

        Raises:
            NoResultFound: If no user matches the filter.
            InvalidRequestError: If invalid query arguments are provided.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided for query")

        query = self._session.query(User)
        try:
            return query.filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the given parameters")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid arguments for query")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes and commit changes to the database.

        Returns:
            None

        Raises:
            ValueError: If an argument does not correspond to a valid user attribute.
        """
        user = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} does not exist on User")
            setattr(user, key, value)

        self._session.commit()
