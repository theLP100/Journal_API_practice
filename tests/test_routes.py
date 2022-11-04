def test_get_all_journals_with_empty_db_returns_empty_list(client):
    #act
    response = client.get("/journal")
    response_body = response.get_json()

    #assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book_with_populated_db(client, two_saved_journals):
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

def test_post_one_journal_into_empty_database_gives_id_1(client):
    response = client.post("/journal", json = {
        "design": "pheonix",
        "dye_gradient": True,
        "dye" : "red"
    })

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {"id": 1}

def test_post_one_journal_creates_one_journal_with_new_id_in_db(client, two_saved_journals):
    #Act
    response = client.post("/journal", json={
        "design": "astrology",
        "sub_design": "taurus"
    })
    response_body = response.get_json()

    #Assert
    assert response.status_code == 201
    assert response_body == {"id": 3}

#make a test for GET route returning 404 if id not there

#make a test for GET route retuning 400 if invalid input

#make a test for PUT/PATCH route returning 404 if id not there

#make a test for PUT/PATCH route retuning 400 if invalid input

#make responses have a consistent format (look at my task_route project for ideas on this. )

