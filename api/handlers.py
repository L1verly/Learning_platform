from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.auth import get_current_user_from_token
from api.actions.user import _create_new_user
from api.actions.user import _delete_user
from api.actions.user import _get_user_by_id
from api.actions.user import _update_user
from api.actions.user import check_user_permissions
from api.schemas import DeleteUserResponse
from api.schemas import ShowUser
from api.schemas import UpdatedUserResponse
from api.schemas import UpdateUserRequest
from api.schemas import UserCreate
from db.models import User
from db.session import get_db

logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(
    body: UserCreate, session: AsyncSession = Depends(get_db)
) -> ShowUser:
    try:
        return await _create_new_user(body, session)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, session)
    if user_for_deletion is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    if not check_user_permissions(
        target_user=user_for_deletion, current_user=current_user
    ):
        raise HTTPException(status_code=403, detail="Forbidden")
    deleted_user_id = await _delete_user(user_id, session)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} is not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, session)
    # Checks if user exists
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.model_dump(exclude_none=True)
    # Checks if there are any parameters passed for update
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, session)
    # Checks if user was found
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if user_id != current_user.user_id:
        if check_user_permissions(
            target_user=user_for_update, current_user=current_user
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    # Ensures there is no error during updating user
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=session, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.patch("/admin_privilege", response_model=UpdatedUserResponse)
async def grant_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    # Checks if current user is super-admin
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    # Ensures user cannot manage his own privileges
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    # Checks if user already admin or super-admin
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already promoted to admin / super-admin.",
        )
    # Checks if user for promotion exists
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {"roles": user_for_promotion.add_admin_privileges_to_model()}
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/admin_privilege", response_model=UpdatedUserResponse)
async def revoke_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    # Checks if current user is super-admin
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    # Ensures user cannot manage his own privileges
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_admin_privileges_revoke = await _get_user_by_id(user_id, db)
    # Checks if user has any admin privileges to delete
    if not user_for_admin_privileges_revoke.is_admin:
        raise HTTPException(
            status_code=409, detail=f"User with id {user_id} has no admin privileges."
        )
    # Checks if user for privilege revoking exists
    if user_for_admin_privileges_revoke is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_admin_privileges_revoke.remove_admin_privileges_from_model()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
