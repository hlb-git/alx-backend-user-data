#!/usr/bin/env python3
""" Auth class defined here """
from flask import abort, request
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """ BasicAuth class """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """doc str"""
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None

        comp = authorization_header.split(' ')
        if comp[0] != 'Basic':
            return None

        return comp[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """decode wrapper func"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            res = base64.b64decode(
                bytes(base64_authorization_header, 'utf-8')
            )
            res = res.decode('utf-8')

        except Exception as e:
            # print(e)
            res = None

        return res

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """doc str"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        # comp = decoded_base64_authorization_header.split(':')
        index_of_colon = decoded_base64_authorization_header.index(':')
        email = decoded_base64_authorization_header[:index_of_colon]
        passwd = decoded_base64_authorization_header[index_of_colon + 1:]
        return (email, passwd)

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ doc str """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None

        User.load_from_file()
        count = User.count()
        if not count:
            return None
        users = User.search({'email': user_email})
        if not users:
            return None
        user = users[0]
        if user.is_valid_password(user_pwd):
            return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ doc str """
        auth_header = self.authorization_header(request)
        credential = self.extract_base64_authorization_header(auth_header)
        plain_credential = self.decode_base64_authorization_header(credential)
        email, passwd = self.extract_user_credentials(plain_credential)
        user = self.user_object_from_credentials(email, passwd)
        print(user)
        return user
