#!/usr/bin/env python3
"""Contains authentication methods for users."""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4
from typing import Optional


def _hash_password(password: str) -> bytes:
    """Return salted hash of the input password string."""
    pass_bytes = password.encode()
    hash_passwd = bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
    return hash_passwd


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize authentication instances."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user, hash the password, and return the user."""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(user.email))
        except (InvalidRequestError, NoResultFound):
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Check if login is valid by matching the password for a user."""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except (InvalidRequestError, NoResultFound):
            return False

    def _generate_uuid(self) -> str:
        """Generate and return a new UUID string."""
        return str(uuid4())

    def create_session(self, email: str) -> Optional[str]:
        """Generate session_id for a user and store it in the database."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """Return user corresponding to session_id or None if not found."""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Update user session_id to None for the given user_id."""
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except Exception as e:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate and set reset_token for a user or raise ValueError."""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return user.reset_token
        except Exception as e:
            raise ValueError
