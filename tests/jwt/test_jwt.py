from utils.jwt import create_access_token, decode_token, JWTToken
from datetime import datetime


async def test_jwt_token(anyio_backend):
    subject = "test"
    token = create_access_token(subject=subject)
    decoded_token = decode_token(token=token.access_token)
    assert type(token) is JWTToken
    assert token.token_type == "bearer"
    assert type(token.access_token) is str
    assert type(decoded_token.get("exp")) is int
    assert datetime.utcfromtimestamp(decoded_token.get("exp")) > datetime.utcnow()
    assert subject == decoded_token.get("sub")
