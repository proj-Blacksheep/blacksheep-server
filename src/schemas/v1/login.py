"""Login schemas."""

from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    """Token response model.

    Attributes:
        access_token: The JWT access token.
        token_type: The type of token (e.g., 'bearer').
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Data structure for decoded token payload.

    Args:
        username: The username extracted from the token.
        exp: The expiration timestamp of the token.
    """

    username: str
    exp: datetime
