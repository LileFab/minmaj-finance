def test_create_account(client):
    payload = {"name": "PEA Boursorama", "type": "pea"}
    response = client.post("/accounts/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "PEA Boursorama"
    assert data["type"] == "pea"
    assert "id" in data
