import pytest


@pytest.mark.anyio
async def test_medium_list_unauthenticated(client):
    response = await client.get("/medium/list")
    assert response.status_code == 401



@pytest.mark.anyio
async def test_medium_list_authenticated(auth_client):
    response = await auth_client.get("/medium/list")
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 3


@pytest.mark.anyio
async def test_medium_create_unauthenticated(client):
    response = await client.post("/medium/create")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_medium_create_authenticated(auth_client):
    response = await auth_client.post("/medium/create", json={
        "name": "C",
        "type": "game"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
    response = await auth_client.post("/medium/create", json={
        "name": "C",
        "type": "error"
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_medium_patch_unauthenticated(client):
    response = await client.patch("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_medium_patch_authenticated(auth_client):
    response = await auth_client.get("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["name"] == "A"

    response = await auth_client.patch("/medium/00000000-0000-4000-a000-000000000000", json={
        "name": "X"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    response = await auth_client.get("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["name"] == "X"

    response = await auth_client.patch("/medium/00000000-0000-4000-a000-000000000000", json={
        "type": "error"
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_medium_delete_unauthenticated(client):
    response = await client.patch("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_medium_delete_authenticated(auth_client):
    response = await auth_client.get("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["is_removed"] == False

    response = await auth_client.delete("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    response = await auth_client.get("/medium/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 404
    
