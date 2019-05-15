import os
import pytest
from datetime import datetime
from hbp_validation_framework import ModelCatalog

"""
1. Verify superuser delete privileges
"""

#1.1) Super user - Delete model, model_instance and model_image
def test_delete_superUser_modelData(request):
    ENVIRONMENT = request.config.getoption("--environment")
    model_catalog = ModelCatalog(username=os.environ.get('HBP_USER'), password=os.environ.get('HBP_PASS'), environment=ENVIRONMENT)
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "_superuser1"
    model_id = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.",
                   instances=[{"source":"https://www.abcde.com",
                               "version":"1.0", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"}])

    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model["instances"][0]["id"]
    model_image_id = model["images"][0]["id"]

    model_catalog.delete_model_instance(instance_id=model_instance_id)
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model_instance(instance_id=model_instance_id)
    assert "Error in retrieving model instance." in str(excinfo.value)

    model_catalog.delete_model_image(image_id=model_image_id)
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model_image(image_id=model_image_id)
    assert "Error in retrieving model image." in str(excinfo.value)

    model_catalog.delete_model(model_id=model_id)
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(model_id=model_id)
    assert "Error in retrieving model." in str(excinfo.value)

#1.2) Normal user - Delete model, model_instance and model_image
def test_delete_normalUser_modelData(request):
    ENVIRONMENT = request.config.getoption("--environment")
    model_catalog = ModelCatalog(username=os.environ.get('HBP_USER_NORMAL'), password=os.environ.get('HBP_PASS_NORMAL'), environment=ENVIRONMENT)
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "_superuser1"
    model_id = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.",
                   instances=[{"source":"https://www.abcde.com",
                               "version":"1.0", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"}])

    model = model_catalog.get_model(model_id=model_id)
    model_instance_id = model["instances"][0]["id"]
    model_image_id = model["images"][0]["id"]

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

#1.3) Super user - Delete test, test_instance and result


#1.4) Normal user - Delete test, test_instance and result
