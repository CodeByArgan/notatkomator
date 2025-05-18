import pytest


@pytest.mark.anyio
async def test_notes_list_unauthenticated(client):
    response = await client.get("/notes/list")
    assert response.status_code == 401



@pytest.mark.anyio
async def test_notes_list_authenticated(auth_client):
    response = await auth_client.get("/notes/list")
    assert response.status_code == 200
    data = response.json()
    assert data['total'] == 2


@pytest.mark.anyio
async def test_notes_create_unauthenticated(client):
    response = await client.post("/notes/create")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_notes_create_authenticated(auth_client):
    response = await auth_client.post("/notes/create", json={
        "medium_id": "00000000-0000-4000-a000-000000000002"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}
    response = await auth_client.post("/notes/create", json={
        "medium_id": "00000000-0000-4000-a000-000000000002"
    })
    assert response.status_code == 409


@pytest.mark.anyio
async def test_notes_patch_unauthenticated(client):
    response = await client.patch("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_notes_patch_authenticated(auth_client):
    response = await auth_client.get("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["status"] == "backlog"

    response = await auth_client.patch("/notes/00000000-0000-4000-a000-000000000000", json={
        "status": "done"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    response = await auth_client.get("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["status"] == "done"

    response = await auth_client.patch("/notes/00000000-0000-4000-a000-000000000000", json={
        "status": "error"
    })
    assert response.status_code == 422


@pytest.mark.anyio
async def test_notes_delete_unauthenticated(client):
    response = await client.patch("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_notes_delete_authenticated(auth_client):
    response = await auth_client.get("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json()["is_removed"] == False

    response = await auth_client.delete("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    response = await auth_client.get("/notes/00000000-0000-4000-a000-000000000000")
    assert response.status_code == 404
    
