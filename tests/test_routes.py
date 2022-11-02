def test_get_all_journals_with_empty_db_returns_empty_list(client):
    #act
    response = client.get("/journal")
    response_body = response.get_json()

    #assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_journals):
    #ACT
    response = client.get("/journal/1")
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1, 
        "design": "tree of life",
        "sub_design": "", 
        "cut": True,
        "complete": True,
        "size": "A6",
        "dye": "canyon tan",
        "dye_gradient": False
    }

def test_create_one_book(client):
    #Act
    response = client.post("/journal", json={
        "design": "astrology",
        "sub_design": "taurus"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body == {"id": 1}