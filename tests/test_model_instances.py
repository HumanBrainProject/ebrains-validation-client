import os
import pytest
import uuid

"""
1. Get an instance of a model
"""

#1.1) With valid details - instance_id
def test_getInstance_valid_id(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance = model_catalog.get_model_instance(instance_id=model["instances"][0]["id"])
    assert model_instance["id"] == model["instances"][0]["id"]

#1.2) With valid details - model_id, version
def test_getInstance_valid_model_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance = model_catalog.get_model_instance(model_id=model_id, version=model["instances"][0]["version"])
    assert model_instance["id"] == model["instances"][0]["id"]

#1.3) With valid details - alias, version
def test_getInstance_valid_alias_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance = model_catalog.get_model_instance(alias=model["alias"], version=model["instances"][0]["version"])
    assert model_instance["id"] == model["instances"][0]["id"]

#1.4) With invalid details - only model_id
def test_getInstance_invalid_only_model(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.get_model_instance(model_id=model_id)
    assert str(excinfo.value) == "instance_path or instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."

#1.5) With invalid details - only alias
def test_getInstance_invalid_only_alias(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.get_model_instance(alias=model["alias"])
    assert str(excinfo.value) == "instance_path or instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."

#1.6) With invalid details - only version
def test_getInstance_invalid_only_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.get_model_instance(version=model["instances"][0]["version"])
    assert str(excinfo.value) == "instance_path or instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."


"""
2. List all instances of a model
"""

#2.1) With valid details - model_id, version
def test_listInstances_valid_model_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instances = model_catalog.list_model_instances(model_id=model_id)
    assert isinstance(model_instances, list)
    assert len(model_instances) > 0

#2.2) With valid details - alias, version
def test_listInstances_valid_alias_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instances = model_catalog.list_model_instances(alias=model["alias"])
    assert isinstance(model_instances, list)
    assert len(model_instances) > 0

#2.3) With invalid details - no model_id or alias
def test_listInstances_invalid_noInput(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_instances = model_catalog.list_model_instances()
    assert str(excinfo.value) == "instance_path or model_id or alias needs to be provided for finding model instances."


"""
3. Add an instance to a model
"""

#3.1) With valid details
def test_addInstance_valid(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_instance = model_catalog.add_model_instance(model_id=model_id,
                                                       source="https://www.12345.com",
                                                       version="3.0",
                                                       parameters="",
                                                       code_format="",
                                                       hash="",
                                                       morphology="",
                                                       description="")
    assert isinstance(uuid.UUID(model_instance, version=4), uuid.UUID)

#3.2) With no model_id
def test_addInstance_no_id(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(source="https://www.12345.com",
                                                            version="4.0",
                                                            parameters="",
                                                            code_format="",
                                                            hash="",
                                                            morphology="",
                                                            description="")
    assert str(excinfo.value) == "Model ID needs to be provided for finding the model."

#3.3) With invalid model_id format
def test_addInstance_invalid_id_format(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(model_id="abcde",
                                                           source="https://www.12345.com",
                                                           version="5.0",
                                                           parameters="",
                                                           code_format="",
                                                           hash="",
                                                           morphology="",
                                                           description="")
    assert "Error in adding model instance." in str(excinfo.value)

#3.4) With invalid model_id value
def test_addInstance_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(model_id=str(uuid.uuid4()),
                                                           source="https://www.12345.com",
                                                           version="6.0",
                                                           parameters="",
                                                           code_format="",
                                                           hash="",
                                                           morphology="",
                                                           description="")
    assert "Error in adding model instance." in str(excinfo.value)

#3.5) With duplicate version number
def test_addInstance_duplicate_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_instance = model_catalog.add_model_instance(model_id=model_id,
                                                       source="https://www.12345.com",
                                                       version="7.0",
                                                       parameters="",
                                                       code_format="",
                                                       hash="",
                                                       morphology="",
                                                       description="")
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(model_id=model_id,
                                                           source="https://www.12345.com",
                                                           version="7.0",
                                                           parameters="",
                                                           code_format="",
                                                           hash="",
                                                           morphology="",
                                                           description="")
    assert "Error in adding model instance." in str(excinfo.value)


"""
4. Edit an instance of a model
"""

#4.1) With valid details - instance_id
def test_editInstance_valid_id(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model_catalog.edit_model_instance(instance_id=model["instances"][0]["id"],
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert model_instance_id == model["instances"][0]["id"]
    model_instance = model_catalog.get_model_instance(instance_id=model_instance_id)
    assert model_instance["source"] == "https://www.abcde.com"
    assert model_instance["parameters"] == "a"
    assert model_instance["code_format"] == "b"
    assert model_instance["hash"] == "c"
    assert model_instance["morphology"] == "d"
    assert model_instance["description"] == "e"

#4.2) With valid details - model_id, version
def test_editInstance_valid_model_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model_catalog.edit_model_instance(model_id=model_id, version=model["instances"][0]["version"],
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert model_instance_id == model["instances"][0]["id"]
    model_instance = model_catalog.get_model_instance(instance_id=model_instance_id)
    assert model_instance["source"] == "https://www.abcde.com"
    assert model_instance["parameters"] == "a"
    assert model_instance["code_format"] == "b"
    assert model_instance["hash"] == "c"
    assert model_instance["morphology"] == "d"
    assert model_instance["description"] == "e"

#4.3) With valid details - alias, version
@pytest.mark.xfail
def test_editInstance_valid_alias_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model_catalog.edit_model_instance(alias=model["alias"], version=model["instances"][0]["version"],
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert model_instance_id == model["instances"][0]["id"]
    model_instance = model_catalog.get_model_instance(instance_id=model_instance_id)
    assert model_instance["source"] == "https://www.abcde.com"
    assert model_instance["parameters"] == "a"
    assert model_instance["code_format"] == "b"
    assert model_instance["hash"] == "c"
    assert model_instance["morphology"] == "d"
    assert model_instance["description"] == "e"

#4.4) With invalid details - only model_id
def test_editInstance_invalid_only_model(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.edit_model_instance(model_id=model_id,
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."

#4.5) With invalid details - only alias
def test_editInstance_invalid_only_alias(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.edit_model_instance(alias=model["alias"],
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."

#4.6) With invalid details - only version
def test_editInstance_invalid_only_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.edit_model_instance(version=model["instances"][0]["version"],
                                                        source="https://www.abcde.com",
                                                        parameters="a",
                                                        code_format="b",
                                                        hash="c",
                                                        morphology="d",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (model_id, version) or (alias, version) needs to be provided for finding a model instance."

#4.7) With valid details - change version
def test_editInstance_valid_change_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_instance = model_catalog.get_model_instance(model_id=model_id, version="1.0a")
    model_instance_id = model_catalog.edit_model_instance(instance_id=model_instance["id"],
                                                        version="a.1")
    assert "1.0a" not in [i["id"] for i in model["instances"]]


"""
5. Download an instance of a model
"""

#5.1) With valid details in current directory - instance_id, public swift storage
def test_downloadInstance_valid_id_cscs(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_instance = model_catalog.get_model_instance(model_id=model_id, version="2.0a")
    file_path = model_catalog.download_model_instance(instance_id=model_instance["id"])
    assert os.path.isfile(file_path)

#5.2) With valid details in current directory - instance_id, collab storage
def test_downloadInstance_valid_id_collab(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_instance = model_catalog.get_model_instance(model_id=model_id, version="2.0b")
    file_path = model_catalog.download_model_instance(instance_id=model_instance["id"])
    assert os.path.isfile(file_path)

#5.3) With valid details in specified directory - instance_id
def test_downloadInstance_valid_id_directory(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_instance = model_catalog.get_model_instance(model_id=model_id, version="2.0a")
    file_path = model_catalog.download_model_instance(instance_id=model_instance["id"], local_directory="./temp")
    assert os.path.isfile(file_path)
    assert "/temp".encode() in os.path.dirname(file_path)

#5.4) With valid details - model_id, version
def test_downloadInstance_valid_model_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    file_path = model_catalog.download_model_instance(model_id=model_id, version="2.0a")
    assert os.path.isfile(file_path)

#5.5) With valid details - alias, version
def test_downloadInstance_valid_alias_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    file_path = model_catalog.download_model_instance(alias=model["alias"], version="2.0a")
    assert os.path.isfile(file_path)


"""
6. Create a new instance of model, if not already exists
"""

#6.1) With valid details - existing instance id
def test_findCreateInstance_valid_exist_instance_id(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    class testModel:
        def __init__(self, model_instance_uuid=""):
            self.model_instance_uuid = model_instance_uuid
    model = model_catalog.get_model(model_id=model_id)
    test_model = testModel(model_instance_uuid=model["instances"][0]["id"])
    model_instance_id = model_catalog.find_model_instance_else_add(test_model)
    assert isinstance(uuid.UUID(model_instance_id, version=4), uuid.UUID)

#6.2) With valid details - existing model id and version
def test_findCreateInstance_valid_exist_modelID_version(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    class testModel:
        def __init__(self, model_uuid="", model_version=""):
            self.model_uuid = model_uuid
            self.model_version = model_version
    model = model_catalog.get_model(model_id=model_id)
    test_model = testModel(model_uuid=model_id, model_version=model["instances"][0]["version"])
    model_instance_id = model_catalog.find_model_instance_else_add(test_model)
    assert isinstance(uuid.UUID(model_instance_id, version=4), uuid.UUID)

def test_findCreateInstance_valid_create(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    class testModel:
        def __init__(self, model_uuid="", model_version=""):
            self.model_uuid = model_uuid
            self.model_version = model_version
    model = model_catalog.get_model(model_id=model_id)
    test_model = testModel(model_uuid=model_id, model_version=model["instances"][0]["version"]+"_new")
    model_instance_id = model_catalog.find_model_instance_else_add(test_model)
    assert isinstance(uuid.UUID(model_instance_id, version=4), uuid.UUID)
