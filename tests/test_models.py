from app.models.journal import Journal

#test that to_dict() makes a dictionary with expected input. 
def test_to_dict_no_missing_data():
    test_data = Journal(
        id= 1, 
        design= "tree of life",
        sub_design= "", 
        cut= True,
        complete= True,
        size= "A6",
        dye= "canyon tan",
        dye_gradient= False
    )
    result = test_data.to_dict()

    assert len(result) == 8
    assert result["id"] == 1
    assert result["design"] == "tree of life"
    assert result["sub_design"] == ""
    assert result["cut"] == True
    assert result["complete"] == True
    assert result["size"] == "A6"
    assert result["dye"] == "canyon tan"
    assert result["dye_gradient"] == False


#test that to_dict() doesn't work when passed in the wrong stuff....

#test that the method from_dict successfully creates a class object when given a dictionary of field values. 