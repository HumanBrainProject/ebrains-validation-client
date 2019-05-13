import os
import pytest
import uuid
from hbp_validation_framework import ModelCatalog
from datetime import datetime

HBP_USERNAME = os.environ.get('HBP_USER')
HBP_PASSWORD = os.environ.get('HBP_PASS')

@pytest.mark.dependency()
def test_mc_authenticate():
    model_catalog = ModelCatalog(username=HBP_USERNAME, password=HBP_PASSWORD, environment="production")
    assert model_catalog.app_name == "Model Catalog"


"""
1] Retrieve a model description by its model_id or alias.
"""

#1.1) Without model_id or alias
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_none(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model()
    assert excinfo.value.message == "Model ID or alias needs to be provided for finding a model."

#1.2) Using model_id
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_id(params):
    model_catalog, model_id = params
    model = model_catalog.get_model(model_id=model_id)
    assert model["id"] ==  model_id

#1.3) Using alias
@pytest.mark.dependency(depends=["test_mc_authenticate", "test_getModel_id"])
def test_getModel_alias(params):
    model_catalog, model_id = params
    model = model_catalog.get_model(model_id=model_id)
    model = model_catalog.get_model(alias=model["alias"])
    assert model["id"] ==  model_id

#1.4) Using model_id and alias
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_both(params):
    model_catalog, model_id = params
    model = model_catalog.get_model(model_id=model_id)
    model = model_catalog.get_model(model_id=model_id, alias=model["alias"])
    assert model["id"] ==  model_id

#1.5) Using invalid model_id format
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_invalid_id_format(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(model_id="abcde")
    assert "Error in retrieving model." in excinfo.value.message

#1.6) Using invalid model_id value
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_invalid_id_value(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(model_id=str(uuid.uuid4()))
    assert "Error in retrieving model." in excinfo.value.message

#1.7) Using invalid alias
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_invalid_alias(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(alias="<>(@#%^)")
    assert "Error in retrieving model description." in excinfo.value.message

#1.8) Using empty model_id
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_empty_id(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(model_id="")
    assert "Model ID or alias needs to be provided for finding a model." in excinfo.value.message

#1.9) Using empty alias
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_empty_alias(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.get_model(alias="")
    assert "Model ID or alias needs to be provided for finding a model." in excinfo.value.message

#1.10) Hide instances
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_hide_instances(params):
    model_catalog, model_id = params
    model = model_catalog.get_model(model_id=model_id, instances=False)
    assert "instances" not in model.keys()

#1.11) Hide images
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getModel_hide_images(params):
    model_catalog, model_id = params
    model = model_catalog.get_model(model_id=model_id, images=False)
    assert "images" not in model.keys()


"""
2] List models satisfying all specified filters
"""

#2.1) No filters
@pytest.mark.dependency(depends=["test_mc_authenticate"])
@pytest.mark.skip
def test_getList_none(params):
    model_catalog, model_id = params
    models = model_catalog.list_models()
    assert isinstance(models, list)
    assert len(models) > 0

#2.2) Single filter
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getList_one(params):
    model_catalog, model_id = params
    models = model_catalog.list_models(app_id="359330")
    assert isinstance(models, list)
    assert len(models) > 0

#2.3) Multiple filters
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getList_many(params):
    model_catalog, model_id = params
    models = model_catalog.list_models(cell_type="granule cell",
                                       brain_region="basal ganglia",
                                       app_id="359330")
    assert isinstance(models, list)
    assert len(models) > 0

#2.4) Invalid filter
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getList_invalid(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        models = model_catalog.list_models(abcde="12345")
    assert "The specified filter 'abcde' is an invalid filter!" in excinfo.value.message

#2.5) Filter with no matches
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getList_nomatch(params):
    model_catalog, model_id = params
    models = model_catalog.list_models(app_id="ABCDE")
    assert isinstance(models, list)
    assert len(models) == 0


"""
3] Display list of valid values for fields
"""

#3.1) No parameters (all)
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getValid_none(params):
    model_catalog, model_id = params
    data = model_catalog.get_attribute_options()
    assert isinstance(data, dict)
    assert len(data.keys()) > 0

#3.2) One parameter
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getValid_one(params):
    model_catalog, model_id = params
    data = model_catalog.get_attribute_options("cell_type")
    assert isinstance(data, dict)
    assert len(data.keys()) == 1
    assert "cell_type" in data.keys()
    assert isinstance(data["cell_type"], list)
    assert len(data["cell_type"]) > 0

#3.3) Multiple parameters
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getValid_many(params):
    model_catalog, model_id = params
    with pytest.raises(TypeError) as excinfo:
        data = model_catalog.get_attribute_options("cell_type", "brain_region")
    assert "takes at most 2 arguments" in excinfo.value.message

#3.4) Invalid parameter
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_getValid_invalid(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        data = model_catalog.get_attribute_options("abcde")
    assert "Specified attribute 'abcde' is invalid." in excinfo.value.message

"""
4] Register a new model on the model catalog
"""

#4.1) No parameters
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_none(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model = model_catalog.register_model()

#4.2) Missing mandatory parameter (author)
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_missingParam(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        model = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                       alias=model_name, organization="HBP-SP6",
                       private=False, cell_type="granule cell", model_scope="single cell",
                       abstraction_level="spiking neurons",
                       brain_region="basal ganglia", species="Mus musculus",
                       owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                       description="This is a test entry! Please ignore.")
    assert "This field may not be blank." in excinfo.value.message

#4.3) Invalid value for parameter (brain_region)
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_invalidParam(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        model = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                       alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                       private=False, cell_type="granule cell", model_scope="single cell",
                       abstraction_level="spiking neurons",
                       brain_region="ABCDE", species="Mus musculus",
                       owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                       description="This is a test entry! Please ignore.")
    assert "brain_region = 'ABCDE' is invalid." in excinfo.value.message

#4.4) Valid model without alias; without instances and images
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_valid_noalias_nodetails(params):
    model_catalog, model_id = params
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    model = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.")
    assert isinstance(uuid.UUID(model, version=4), uuid.UUID)

#4.5) Valid model with alias; without instances and images
# Note: using current timestamp as alias to ensure uniqueness
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_valid_withalias_nodetails(params):
    model_catalog, model_id = params
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    model = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.")
    assert isinstance(uuid.UUID(model, version=4), uuid.UUID)

#4.6) Valid model with repeated alias; without instances and images
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_repeat_alias_nodetails(params):
    model_catalog, model_id = params
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + "ABCDE"
    model1 = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.")
    with pytest.raises(Exception) as excinfo:
        model2 = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                       alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                       private=False, cell_type="granule cell", model_scope="single cell",
                       abstraction_level="spiking neurons",
                       brain_region="basal ganglia", species="Mus musculus",
                       owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                       description="This is a test entry! Please ignore.")
    assert "model with this alias already exists." in excinfo.value.message

#4.7) Valid model with alias; with instances and images
# Note: using current timestamp as alias to ensure uniqueness
@pytest.mark.dependency(depends=["test_mc_authenticate"])
def test_addModel_valid_withalias_withdetails(params):
    model_catalog, model_id = params
    model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    model = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
                   alias=model_name, author="Shailesh Appukuttan", organization="HBP-SP6",
                   private=False, cell_type="granule cell", model_scope="single cell",
                   abstraction_level="spiking neurons",
                   brain_region="basal ganglia", species="Mus musculus",
                   owner="Shailesh Appukuttan", project="SP 6.4", license="BSD 3-Clause",
                   description="This is a test entry! Please ignore.",
                   instances=[{"source":"https://www.abcde.com",
                               "version":"1.0", "parameters":""},
                              {"source":"https://www.12345.com",
                               "version":"2.0", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"},
                           {"url":"https://collab.humanbrainproject.eu/assets/hbp_diamond_120.png",
                            "caption":"HBP Logo"}])
    assert isinstance(uuid.UUID(model, version=4), uuid.UUID)