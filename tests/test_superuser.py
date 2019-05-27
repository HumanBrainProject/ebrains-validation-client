import os
import pytest
import platform
from datetime import datetime
from hbp_validation_framework import ModelCatalog, TestLibrary, sample

"""
1. Verify superuser delete privileges
"""

#1.1) Super user - Delete model, model_instance, model_image, test, test_instance and result
def test_delete_superUser(request):
    ENVIRONMENT = request.config.getoption("--environment")
    model_catalog = ModelCatalog(username=os.environ.get('HBP_USER'), password=os.environ.get('HBP_PASS'), environment=ENVIRONMENT)
    model_name = "Model_{}_{}_py{}_superuser1".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), model_catalog.environment, platform.python_version())
    model_id = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Validation Tester", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Validation Tester", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.",
                   instances=[{"source":"https://www.abcde.com",
                               "version":"1.0", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"}])

    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model["instances"][0]["id"]
    model_image_id = model["images"][0]["id"]
    model = sample.SampleModel(model_uuid=model_id, model_version=model["instances"][0]["version"])

    test_library = TestLibrary.from_existing(model_catalog)
    test_name = "Test_{}_{}_py{}_superuser2".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), test_library.environment, platform.python_version())
    test_id = test_library.add_test(name="IGNORE - Test Test - " + test_name, alias=test_name, author="Validation Tester",
                    species="Mus musculus", age="", brain_region="basal ganglia", cell_type="granule cell",
                    data_modality="electron microscopy", test_type="network structure", score_type="Other", protocol="Later",
                    data_location="https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/sp6_validation_data/test.txt",
                    data_type="Mean, SD", publication="Testing et al., 2019",
                    version="1.0", repository="https://github.com/HumanBrainProject/hbp-validation-client.git", path="hbp_validation_framework.sample.SampleTest")

    test = test_library.get_test_definition(test_id=test_id)
    test_instance_id = test["codes"][0]["id"]
    test = test_library.get_validation_test(test_id=test_id)

    score = test.judge(model)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder_name = "results_{}_{}_{}".format(model.name, model.model_uuid[:8], timestamp)
    result_id = test_library.register_result(score, project = "52468") # Collab ID = 52468

    test_library.delete_result(result_id=result_id)
    result = test_library.get_result(result_id=result_id)
    assert len(result["results"]) == 0

    model_catalog.delete_model_instance(instance_id=model_instance_id)
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.get_model_instance(instance_id=model_instance_id)
    assert "Error in retrieving model instance." in str(excinfo.value)

    model_catalog.delete_model_image(image_id=model_image_id)
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.get_model_image(image_id=model_image_id)
    assert "Error in retrieving model image." in str(excinfo.value)

    model_catalog.delete_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(model_id=model_id)
    assert "Error in retrieving model." in str(excinfo.value)

    test_library.delete_test_instance(instance_id=test_instance_id)
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.get_test_instance(instance_id=test_instance_id)
    assert "Error in retrieving test instance." in str(excinfo.value)

    test_library.delete_test(test_id=test_id)
    with pytest.raises(Exception) as excinfo:
        test = test_library.get_test_definition(test_id=test_id)
    assert "Error in retrieving test definition." in str(excinfo.value)

#1.2) Normal user - Delete model, model_instance, model_image, test, test_instance and result
def test_delete_normalUser(request):
    ENVIRONMENT = request.config.getoption("--environment")
    model_catalog = ModelCatalog(username=os.environ.get('HBP_USER_NORMAL'), password=os.environ.get('HBP_PASS_NORMAL'), environment=ENVIRONMENT)
    model_name = "Model_{}_{}_py{}_normaluser1".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), model_catalog.environment, platform.python_version())
    model_id = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Validation Tester", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Validation Tester", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.",
                   instances=[{"source":"https://www.abcde.com",
                               "version":"1.0", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"}])

    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model["instances"][0]["id"]
    model_image_id = model["images"][0]["id"]
    model = sample.SampleModel(model_uuid=model_id, model_version=model["instances"][0]["version"])

    test_library = TestLibrary.from_existing(model_catalog)
    test_name = "Test_{}_{}_py{}_normaluser2".format(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), test_library.environment, platform.python_version())
    test_id = test_library.add_test(name="IGNORE - Test Test - " + test_name, alias=test_name, author="Validation Tester",
                    species="Mus musculus", age="", brain_region="basal ganglia", cell_type="granule cell",
                    data_modality="electron microscopy", test_type="network structure", score_type="Other", protocol="Later",
                    data_location="https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/sp6_validation_data/test.txt",
                    data_type="Mean, SD", publication="Testing et al., 2019",
                    version="1.0", repository="https://github.com/HumanBrainProject/hbp-validation-client.git", path="hbp_validation_framework.sample.SampleTest")

    test = test_library.get_test_definition(test_id=test_id)
    test_instance_id = test["codes"][0]["id"]
    test = test_library.get_validation_test(test_id=test_id)

    score = test.judge(model)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder_name = "results_{}_{}_{}".format(model.name, model.model_uuid[:8], timestamp)
    result_id = test_library.register_result(score, project = "52468") # Collab ID = 52468

    with pytest.raises(Exception) as excinfo:
        test_library.delete_result(result_id=result_id)
    assert "Only SuperUser accounts can delete data." in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        model_catalog.delete_model_instance(instance_id=model_instance_id)
    assert "Only SuperUser accounts can delete data." in str(excinfo.value)

    # see: https://github.com/HumanBrainProject/hbp-validation-framework/issues/242
    # with pytest.raises(Exception) as excinfo:
    #     model_catalog.delete_model_image(image_id=model_image_id)
    # assert "Only SuperUser accounts can delete data." in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        model_catalog.delete_model(model_id=model_id)
    assert "Only SuperUser accounts can delete data." in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        test_library.delete_test_instance(instance_id=test_instance_id)
    assert "Only SuperUser accounts can delete data." in str(excinfo.value)

    with pytest.raises(Exception) as excinfo:
        test_library.delete_test(test_id=test_id)
    assert "Only SuperUser accounts can delete data." in str(excinfo.value)
