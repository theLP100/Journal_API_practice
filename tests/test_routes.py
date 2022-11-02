def test_get_all_journals_with_no_records(client):
    #act
    response = client.get("/journal")
    response_body = response.get_json()

    #assert
    assert response.status_code == 200
    assert response_body == []