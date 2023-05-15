from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.routing import APIRoute

# Since FastAPI dependency calls are cached, it won't validate the token
# format again, and it will just return the token.
from src.dependencies.token import get_token


async def authorization(
    request: Request, token: Annotated[str, Depends(get_token)]
) -> bool:
    permissions = {
        ("GET", "/api/v2/courses/{course_id}/activities"): "activity_view",
        (
            "GET",
            "/api/v2/courses/{course_id}/activities/{activity_id}",
        ): "activity_view",
        ("GET", "/api/v2/courses/{course_id}/categories"): "activity_view",
        (
            "GET",
            "/api/v2/courses/{course_id}/categories/{category_id}",
        ): "activity_view",
    }

    route: APIRoute = request.scope["route"]
    path = route.path
    method = request.method

    # If the endpoint is not in the permissions dictionary we bypass authorization
    if not (method, path) in permissions:
        return True

    # TODO
    # This is just a dummy authorization dependency,
    # once the RPL users server is implemented
    # it should add the users permissions for each course
    # to the jwt or we should call that service to get the
    # permissions over a specific course.
    #
    # For now we are using this dummy "user_permissions" list
    # with admin permissions.
    user_permissions = [
        "course_delete",
        "course_view",
        "course_edit",
        "activity_view",
        "activity_manage",
        "activity_submit",
        "user_view",
        "user_manage",
    ]

    if not permissions[(method, path)] in user_permissions:
        raise HTTPException(
            status_code=403,
            detail=f"The user does not have permissions to access to {method} {request.scope['path']}",
        )

    return True
