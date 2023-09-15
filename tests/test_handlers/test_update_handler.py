from uuid import uuid4

import pytest

from db.models import PortalRole
from tests.conftest import create_test_auth_headers_for_user


@pytest.mark.parametrize(
    "user_roles",
    (
        [PortalRole.ROLE_PORTAL_SUPERADMIN],
        [PortalRole.ROLE_PORTAL_ADMIN],
        [PortalRole.ROLE_PORTAL_USER],
        [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_SUPERADMIN],
    ),
)
async def test_update_user(
    client, create_user_in_database, get_user_from_database, user_roles
):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": user_roles,
    }
    user_data_updated = {
        "name": "Arnold",
        "surname": "Schwarzenegger",
        "email": "cheburek@kek.com",
    }
    await create_user_in_database(**user_data)
    await _patch_and_validate_user(
        client, user_data, user_data_updated, get_user_from_database
    )


async def test_update_user_check_one_is_updated(
    client, create_user_in_database, get_user_from_database
):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Arnold",
        "surname": "Schwarzenegger",
        "email": "arnie@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_3 = {
        "user_id": uuid4(),
        "name": "Tom",
        "surname": "Ford",
        "email": "tommy@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_updated = {
        "name": "Cooper",
        "surname": "Hunter",
        "email": "cheburek@kek.com",
    }
    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    await _patch_and_validate_user(
        client, user_data_1, user_data_updated, get_user_from_database
    )

    # check other users that data has not been changed
    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_2["name"]
    assert user_from_db["surname"] == user_data_2["surname"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_3["name"]
    assert user_from_db["surname"] == user_data_3["surname"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


@pytest.mark.parametrize(
    "user_data_updated, expected_status_code, expected_detail",
    [
        (
            {},
            422,
            {
                "detail": [
                    {
                        "input": {},
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                ]
            },
        ),
        ({"name": "123"}, 422, {"detail": "Name should contain only letters"}),
        (
            {"email": ""},
            422,
            {
                "detail": [
                    {
                        "input": {"email": ""},
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "input": {"email": ""},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "ctx": {
                            "reason": "The email address is not valid. It must have "
                            "exactly one @-sign."
                        },
                        "input": "",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    },
                ]
            },
        ),
        (
            {"surname": ""},
            422,
            {
                "detail": [
                    {
                        "input": {"surname": ""},
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "ctx": {"min_length": 1},
                        "input": "",
                        "loc": ["body", "surname"],
                        "msg": "String should have at least 1 characters",
                        "type": "string_too_short",
                        "url": "https://errors.pydantic.dev/2.3/v/string_too_short",
                    },
                    {
                        "input": {"surname": ""},
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                ]
            },
        ),
        (
            {"name": ""},
            422,
            {
                "detail": [
                    {
                        "ctx": {"min_length": 1},
                        "input": "",
                        "loc": ["body", "name"],
                        "msg": "String should have at least 1 characters",
                        "type": "string_too_short",
                        "url": "https://errors.pydantic.dev/2.3/v/string_too_short",
                    },
                    {
                        "input": {"name": ""},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "input": {"name": ""},
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                ]
            },
        ),
        ({"surname": "123"}, 422, {"detail": "Name should contain only letters"}),
        (
            {"email": "123"},
            422,
            {
                "detail": [
                    {
                        "input": {"email": "123"},
                        "loc": ["body", "name"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "input": {"email": "123"},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.3/v/missing",
                    },
                    {
                        "ctx": {
                            "reason": "The email address is not valid. It must have "
                            "exactly one @-sign."
                        },
                        "input": "123",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    },
                ]
            },
        ),
    ],
)
async def test_update_user_validation_error(
    client,
    create_user_in_database,
    get_user_from_database,
    user_data_updated,
    expected_status_code,
    expected_detail,
):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == expected_status_code
    resp_data = resp.json()
    assert resp_data == expected_detail


async def test_update_user_id_validation_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "artem@example.com",
        "hashed_password": "SampleHashedPass",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_data_updated = {
        "name": "John",
        "surname": "Doe",
        "email": "johny@kek.com",
    }
    resp = client.patch(
        "/user/?user_id=123",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 422
    data_from_response = resp.json()
    assert (
        data_from_response["detail"][0].items()
        >= {
            "input": "123",
            "loc": ["query", "user_id"],
            "msg": "Input should be a valid UUID, invalid length: expected "
            "length 32 for simple format, found 3",
            "type": "uuid_parsing",
        }.items()
    )


async def test_update_user_not_found_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "artem@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    await create_user_in_database(**user_data)
    user_data_updated = {
        "name": "John",
        "surname": "Doe",
        "email": "johny@kek.com",
    }
    user_id = uuid4()
    resp = client.patch(
        f"/user/?user_id={user_id}",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 404
    resp_data = resp.json()
    assert resp_data == {"detail": f"User with id {user_id} not found."}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "John",
        "surname": "Doe",
        "email": "johny@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": [PortalRole.ROLE_PORTAL_USER],
    }
    user_data_updated = {
        "name": "Robert",
        "surname": "Show",
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 503
    assert (
        'duplicate key value violates unique constraint "users_email_key"'
        in resp.json()["detail"]
    )


async def test_admin_update_other_admin(
    client, create_user_in_database, get_user_from_database
):
    user_for_update = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "artem@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
    }
    user_data_who_updates = {
        "user_id": uuid4(),
        "name": "Arnold",
        "surname": "Schwarzenegger",
        "email": "arnie@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": [PortalRole.ROLE_PORTAL_USER, PortalRole.ROLE_PORTAL_ADMIN],
    }
    user_data_updated = {
        "name": "Leo",
        "surname": "Vinci",
        "email": "cheburek@kek.com",
    }
    for user_data in [user_for_update, user_data_who_updates]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/admin_privilege?user_id={user_for_update['user_id']}",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_for_update["user_id"]),
    )
    data_from_resp = resp.json()
    assert resp.status_code == 403
    assert data_from_resp == {"detail": "Forbidden."}
    not_updated_user_from_db = await get_user_from_database(user_for_update["user_id"])
    # Check that only one user was not changed
    assert len(not_updated_user_from_db) == 1
    not_updated_user_from_db = dict(not_updated_user_from_db[0])
    # Check if correct user was not updated
    assert not_updated_user_from_db["user_id"] == user_for_update["user_id"]


async def _patch_and_validate_user(
    client, user_data: dict, user_data_updated, get_user_from_database
):
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        json=user_data_updated,
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]
