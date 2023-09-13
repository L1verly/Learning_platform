from uuid import uuid4

from tests.conftest import create_test_auth_headers_for_user


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": ["ROLE_PORTAL_USER"],
    }
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] == user_data["is_active"]


async def test_get_user_id_validation_error(
    client, create_user_in_database, get_user_from_database
):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": ["ROLE_PORTAL_USER"],
    }
    await create_user_in_database(**user_data)
    resp = client.get(
        "/user/?user_id=123",
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


async def test_get_user_not_found(
    client, create_user_in_database, get_user_from_database
):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "lol@kek.com",
        "hashed_password": "SamplePassHash",
        "is_active": True,
        "roles": ["ROLE_PORTAL_USER"],
    }
    user_id_for_finding = uuid4()
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_id_for_finding}",
        headers=create_test_auth_headers_for_user(user_data["user_id"]),
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id_for_finding} not found."}


async def test_get_user_unauthorized(
    client, create_user_in_database, get_user_from_database
):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "artem@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": ["ROLE_PORTAL_USER"],
    }
    user_id = uuid4()
    bad_auth_headers = create_test_auth_headers_for_user(user_data["user_id"])
    bad_auth_headers["Authorization"] += "a"
    resp = client.get(
        f"/user/?user_id={user_id}",
        headers=bad_auth_headers,
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_get_user_bad_credentials(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Artem",
        "surname": "Budzhak",
        "email": "artem@example.com",
        "is_active": True,
        "hashed_password": "SampleHashedPass",
        "roles": ["ROLE_PORTAL_USER"],
    }
    await create_user_in_database(**user_data)
    invalid_user_id = uuid4()
    resp = client.get(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers_for_user(invalid_user_id),
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}
