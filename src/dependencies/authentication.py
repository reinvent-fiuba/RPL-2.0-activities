from typing import Annotated

from fastapi import Depends

# It will go and look in the request for that Authorization header,
# check if the value is Bearer plus some token, and will return the
# token as a str.
from src.dependencies.token import get_token


async def authentication(token: Annotated[str, Depends(get_token)]) -> bool:
    # TODO
    # This is just a dummy authentication dependency,
    # once the RPL users server is implemented
    # we should call that service to validate that the
    # token is actually valid.

    return True
