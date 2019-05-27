import pytest
import platform
import uuid
from hbp_validation_framework import sample
from hbp_validation_framework.datastores import CollabDataStore
from datetime import datetime


"""
1. Register a test result
"""

#1.1) With valid details
def test_register_result_valid(modelCatalog, testLibrary, myModelID, myTestID):
    model_catalog = modelCatalog
    model_id = myModelID
    test_library = testLibrary
    test_id = myTestID

    model = model_catalog.get_model(model_id=model_id)
    model = sample.SampleModel(model_uuid=model_id, model_version=model["instances"][0]["version"])

    test_name = "Test_{}_{}_py{}_getValTest_1".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), test_library.environment, platform.python_version())
    test_id = test_library.add_test(name="IGNORE - Test Test - " + test_name, alias=test_name, author="Validation Tester",
                    species="Mus musculus", age="", brain_region="basal ganglia", cell_type="granule cell",
                    data_modality="electron microscopy", test_type="network structure", score_type="Other", protocol="Later",
                    data_location="https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/sp6_validation_data/test.txt",
                    data_type="Mean, SD", publication="Testing et al., 2019",
                    version="1.0", repository="https://github.com/HumanBrainProject/hbp-validation-client.git", path="hbp_validation_framework.sample.SampleTest")
    test = test_library.get_validation_test(test_id=test_id)

    score = test.judge(model)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder_name = "results_{}_{}_{}".format(model.name, model.model_uuid[:8], timestamp)

    result_id = test_library.register_result(score, project = "52468") # Collab ID = 52468
    assert isinstance(uuid.UUID(result_id, version=4), uuid.UUID)


"""
2. Get a test result
"""

#2.1) With valid details - default order = results
def test_get_result_valid_order_default(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id)
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "results"

#2.2) With valid details - order = test
def test_get_result_valid_order_test(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id, order="test")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "tests"

#2.3) With valid details - order = model
def test_get_result_valid_order_model(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id, order="model")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "models"

#2.4) With valid details - order = test_code
def test_get_result_valid_order_test_code(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id, order="test_code")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "test_codes"

#2.5) With valid details - order = model_instance
def test_get_result_valid_order_model_instance(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id, order="model_instance")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "model_instances"

#2.6) With valid details - order = score_type
def test_get_result_valid_order_score_type(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    result = test_library.get_result(result_id=result_id, order="score_type")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "score_type"

#2.7) With invalid order
def test_get_result_invalid_order(testLibrary, myResultID):
    test_library = testLibrary
    result_id = myResultID
    with pytest.raises(Exception) as excinfo:
        result = test_library.get_result(result_id=result_id, order="abcde")
    assert "order needs to be specified from" in str(excinfo.value)


"""
3. List results satisfying specified filters
"""

#3.1) With valid details - default order = results
def test_list_results_valid_order_default(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id)
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "results"

#3.2) With valid details - order = test
def test_list_results_valid_order_test(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id, order="test")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "tests"

#3.3) With valid details - order = model
def test_list_results_valid_order_model(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id, order="model")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "models"

#3.4) With valid details - order = test_code
def test_list_results_valid_order_test_code(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id, order="test_code")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "test_codes"

#3.5) With valid details - order = model_instance
def test_list_results_valid_order_model_instance(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id, order="model_instance")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "model_instances"

#3.6) With valid details - order = score_type
def test_list_results_valid_order_score_type(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    result = test_library.list_results(test_id=test_id, order="score_type")
    assert isinstance(result, dict)
    assert len(result.keys()) == 1
    assert list(result.keys())[0] == "score_type"

#3.7) With invalid order
def test_list_results_invalid_order(testLibrary, myTestID, myResultID):
    test_library = testLibrary
    test_id = myTestID
    with pytest.raises(Exception) as excinfo:
        result = test_library.list_results(test_id=test_id, order="abcde")
    assert "order needs to be specified from" in str(excinfo.value)
