import json

import pytest


async def test_create_user(client, get_user_from_database):
    user_data = {"name": "Artem", "surname": "Budzhak", "email": "hello@example.com"}
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["name"] == user_data["name"]
    assert data_from_resp["surname"] == user_data["surname"]
    assert data_from_resp["email"] == user_data["email"]
    assert data_from_resp["is_active"] is True
    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is True
    assert str(user_from_db["user_id"]) == data_from_resp["user_id"]


# async def test_create_user_duplicate_email_error(client, get_user_from_database):
#     user_data = {"name": "Artem", "surname": "Budzhak", "email": "hello@example.com"}
#     user_data_same = {"name": "John", "surname": "Doe", "email": "hello@example.com"}
#     # Creating first user
#     resp = client.post("/user/", data=json.dumps(user_data))
#     data_from_resp = resp.json()
#     assert resp.status_code == 200
#     assert data_from_resp["name"] == user_data["name"]
#     assert data_from_resp["surname"] == user_data["surname"]
#     assert data_from_resp["email"] == user_data["email"]
#     assert data_from_resp["is_active"] is True
#     users_from_db = await get_user_from_database(data_from_resp["user_id"])
#     assert len(users_from_db) == 1
#     user_from_db = dict(users_from_db[0])
#     assert user_from_db["name"] == user_data["name"]
#     assert user_from_db["surname"] == user_data["surname"]
#     assert user_from_db["email"] == user_data["email"]
#     assert user_from_db["is_active"] is True
#     assert str(user_from_db["user_id"]) == data_from_resp["user_id"]
#     resp = client.post("/user/", data=json.dumps(user_data_same))
#     assert resp.status_code == 503
#     assert (
#         'duplicate key value violates unique constraint "users_email_key"'
#         in resp.json()["detail"]
#     )


@pytest.mark.parametrize(
    "user_data_for_creation, expected_status_code, expected_detail",
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
                    },
                    {
                        "input": {},
                        "loc": ["body", "surname"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                    {
                        "input": {},
                        "loc": ["body", "email"],
                        "msg": "Field required",
                        "type": "missing",
                    },
                ]
            },
        ),
        (
            {"name": 123, "surname": 456, "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "input": 123,
                        "loc": ["body", "name"],
                        "msg": "Input should be a valid string",
                        "type": "string_type",
                    },
                    {
                        "input": 456,
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "type": "string_type",
                    },
                    {
                        "input": "lol",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    },
                ]
            },
        ),
        (
            {"name": "Artem", "surname": 456, "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "input": 456,
                        "loc": ["body", "surname"],
                        "msg": "Input should be a valid string",
                        "type": "string_type",
                    },
                    {
                        "input": "lol",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    },
                ]
            },
        ),
        (
            {"name": "Artem", "surname": "Budzhak", "email": "lol"},
            422,
            {
                "detail": [
                    {
                        "input": "lol",
                        "loc": ["body", "email"],
                        "msg": "value is not a valid email address: The email address is "
                        "not valid. It must have exactly one @-sign.",
                        "type": "value_error",
                    }
                ]
            },
        ),
    ],
)
async def test_create_user_validation_error(
    client, user_data_for_creation, expected_status_code, expected_detail
):
    resp = client.post("/user/", data=json.dumps(user_data_for_creation))
    data_from_resp = resp.json()
    assert resp.status_code == expected_status_code
    assert data_from_resp["detail"][0].items() >= expected_detail["detail"][0].items()
