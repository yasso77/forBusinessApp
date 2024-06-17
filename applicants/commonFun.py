from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, password_hash: str):
    return bcrypt.verify(password, password_hash)