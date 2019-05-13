import pytest
from hbp_validation_framework import ModelCatalog
from datetime import datetime

HBP_USERNAME = os.environ.get('HBP_USER')
HBP_PASSWORD = os.environ.get('HBP_PASS')

@pytest.fixture(scope="session")
def params():
   model_catalog = ModelCatalog(username=HBP_USERNAME, password=HBP_PASSWORD, environment="production")
   model_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
   model_id = model_catalog.register_model(app_id="359330", name="IGNORE - Test Model - " + model_name,
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
   return model_catalog, model_id

# def pytest_sessionfinish(session, exitstatus):
#    model_catalog = ModelCatalog(username=HBP_USERNAME, password=HBP_PASSWORD, environment="production")
#    models = model_catalog.list_models(app_id="359330", author="Shailesh Appukuttan")
#    for model in models:
#       model_catalog.delete_model(model["id"])
