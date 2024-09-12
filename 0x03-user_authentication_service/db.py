#!/usr/bin/python3
"""
DB module that connects and initializes the database.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User, Base


class DB:
    """DB class."""

    def __init__(self) -> None:
        """Initialize a new DB instance."""
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object."""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a user
        with email and hashed password, save to DB, and return."""
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Filter for a user using kwargs and return."""
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
        except Exception as e:
            raise InvalidRequestError
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Find a user by ID, update attributes with kwargs, and commit."""
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if getattr(user, str(key), 'None') == 'None':
                raise ValueError
            setattr(user, str(key), val)
        self._session.commit()
