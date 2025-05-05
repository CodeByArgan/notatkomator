import pytest
from models import AuditLog


@pytest.mark.anyio
async def test_create_testing_log_unauthenticated(client):
    response = await client.post("/audit-log/test-create")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_create_testing_log_authenticated(auth_client):
    for _ in range(3):
        response = await auth_client.post("/audit-log/test-create")
        assert response.status_code == 200
        assert response.json() == {"message": "ok"}

    logs = await AuditLog.all()
    assert len(logs) == 3
    assert all(log.username == "SYSTEM" for log in logs)


@pytest.mark.anyio
async def test_get_audit_log_list_unauthenticated(client):
    response = await client.get("/audit-log/list?page=1&limit=10")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_audit_log_list_authenticated(auth_client):
    response = await auth_client.get("/audit-log/list?page=1&limit=10")
    assert response.status_code == 200
    assert "list" in response.json()
