#!/usr/bin/env python3
""" encrypt password module """
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """ hash a password """
    b = password.encode()
    hashed = hashpw(b, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if a password is valid """
    return bcrypt.checkpw(password.encode(), hashed_password)
