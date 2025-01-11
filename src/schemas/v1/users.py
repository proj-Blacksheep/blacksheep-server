"""Users schemas."""

from datetime import datetime

from pydantic import BaseModel


class UserDTO(BaseModel):
    """Data Transfer Object for User.

    This class represents the user data that can be transferred between different
    layers of the application. It includes all necessary user information while
    excluding sensitive data like passwords.

    Attributes:
        id: The unique identifier for the user.
        username: The username of the user.
        api_key: The API key associated with the user.
        is_admin: Whether the user has admin privileges.
        created_at: When the user was created.
        updated_at: When the user was last updated.
    """

    id: int
    username: str
    api_key: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""

        from_attributes = True


class UserCreateRequest(BaseModel):
    """User create request.

    Attributes:
        username: The username of the user.
        password: The password of the user.
        role: The role of the user.
    """

    username: str
    password: str
    is_admin: bool = False


class UserMeResponse(BaseModel):
    """User me response.

    Attributes:
        username: The username of the user.
        api_key: The api key of the user.
        is_admin: The role of the user.
    """

    username: str
    api_key: str
    is_admin: bool
