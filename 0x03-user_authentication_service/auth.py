#!/usr/bin/env python3
""" Auth module """
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ returns a hashed password """
    h_psw = bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt(4))
    return h_psw


def _generate_uuid() -> str:
    """ returns a string representation of a new UUID """
    return str(uuid.uuid4())


class Auth:
    """ Auth class """

    def __init__(self):
        """ initiallize object """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a user """
        user_exists = False
        try:
            existing_user = self._db.find_user_by(email=email)
            user_exists = True
        except Exception:
            pass
        if user_exists:
            raise ValueError(f"User {email} already exists")
        hashed_passwd = _hash_password(password)
        return self._db.add_user(email=email, hashed_password=hashed_passwd)

    def valid_login(self, email: str, password: str) -> bool:
        """ checks if login is valid """
        try:
            user = self._db.find_user_by(email=email)
            p = bytes(password, 'utf-8')
            if bcrypt.checkpw(p, user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ creates a session """
        try:
            user = self._db.find_user_by(email=email)
            s_id = _generate_uuid()
            self._db.update_user(user.id, session_id=s_id)
            return s_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """ returns a user from a session_id """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception:
            return None

    def destroy_session(self, user_id: str) -> User:
        """ removes user's session_id """
        try:
            self._db.update_user(user_id, session_id=None)
        except Exception:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ updates a users reset token field """
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates a users password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError
        hashed_p = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_p,
                             reset_token=None)
