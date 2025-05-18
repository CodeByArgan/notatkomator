import pytest


@pytest.mark.anyio
async def test_auth_me_unauthenticated(client):
    response = await client.get("/auth/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_auth_logout_unauthenticated(client):
    response = await client.get("/auth/logout")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_auth_me_authenticated(auth_client):
    response = await auth_client.get("/auth/me")
    assert response.status_code == 200
    assert response.json() == {"email": "user@system.com", "role": "user"}


@pytest.mark.anyio
async def test_auth_logout_authenticated(auth_client):
    response = await auth_client.get("/auth/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
