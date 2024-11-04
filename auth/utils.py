from datetime import datetime, timedelta
import jwt

import bcrypt

from config import PUBLIC_KEY, PRIVATE_KEY


def encode_jwt(
        payload: dict,
        expire_minutes: int,
        private_key: str = PRIVATE_KEY,
        algorithm: str = 'RS256',

):
    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(
        token: str | bytes,
        public_key: str = PUBLIC_KEY,
        algorithm: str = 'RS256'
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded

def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int,
):
    jwt_payload = {'token_type': token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
    )

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
