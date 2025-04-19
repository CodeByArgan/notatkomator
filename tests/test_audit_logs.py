import pytest
from models import AuditLog


@pytest.mark.anyio
async def test_create_testing_log(client):
    response = await client.post("/audit-log/test-create")
    assert response.status_code == 200
    assert response.json() == {"message": "ok"}

    logs = await AuditLog.all()
    assert len(logs) == 1
    assert logs[0].username == "SYSTEM"

    response = await client.post("/audit-log/test-create")
    response = await client.post("/audit-log/test-create")

    logs = await AuditLog.all()
    assert len(logs) == 3
    assert logs[0].username == "SYSTEM"


@pytest.mark.anyio
async def test_get_audit_log_list(client):
    response = await client.get("/audit-log/list?page=1&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "audit_logs" in data
