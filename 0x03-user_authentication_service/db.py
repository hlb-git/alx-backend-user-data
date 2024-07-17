#!/usr/bin/env python3
""" database module """
import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import TypeVar, Type, Mapping, Dict
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """ DB class """

    def __init__(self) -> None:
        """ constructor """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """ creates a session if not exists """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ adds a user to the database """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, *args, **kwargs) -> User:
        """ find a user by the key-value pairs """
        if not kwargs:
            raise NoResultFound
        valid_keys = ['email', 'id', 'hashed_password',
                      'session_id', 'reset_token']
        for key in kwargs:
            if key not in valid_keys:
                raise InvalidRequestError
        query = self._session.query(User)
        for key in kwargs:
            if key == 'email':
                query = query.filter(
                            User.email == kwargs[key]
                            )
            elif key == 'id':
                query = query.filter(
                            User.id == kwargs[key]
                            )
            elif key == 'hashed_password':
                query = query.filter(
                            User.hashed_password == kwargs[key]
                            )
            elif key == 'session_id':
                query = query.filter(
                            User.session_id == kwargs[key]
                            )
            elif key == 'reset_token':
                query = query.filter(
                            User.reset_token == kwargs[key]
                            )
        all_users = query.all()
        if not all_users:
            raise NoResultFound
        return all_users[0]

    def update_user(self, user_id: int, *args, **kwargs) -> None:
        """ update a user in the database """
        valid_keys = ['email', 'id', 'hashed_password',
                      'session_id', 'reset_token']
        user = self.find_user_by(id=user_id)
        for key in kwargs:
            if key not in valid_keys:
                raise ValueError
            user.__setattr__(key, kwargs[key])
        self._session.commit()
