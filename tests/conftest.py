import os
import pytest
from hbp_validation_framework import ModelCatalog
from datetime import datetime

HBP_USERNAME = os.environ.get('HBP_USER')
HBP_PASSWORD = os.environ.get('HBP_PASS')

def pytest_addoption(parser):
    parser.addoption(
        "--environment", action="store", default="production", help="options: production or dev"
    )

@pytest.fixture(scope="session")
def params(request):
   ENVIRONMENT = request.config.getoption("--environment")
   model_catalog = ModelCatalog(username=HBP_USERNAME, password=HBP_PASSWORD, environment=ENVIRONMENT)
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
                              {"source":"https://www.abcde.com",
                               "version":"1.0a", "parameters":""},
                              {"source":"https://object.cscs.ch/v1/AUTH_c0a333ecf7c045809321ce9d9ecdfdea/sp6_validation_data/test.txt",
                               "version":"2.0a", "parameters":""},
                              {"source":"https://collab.humanbrainproject.eu/#/collab/8123/nav/61645?state=uuid%3D753ef79e-3fca-4084-939b-c6987b73c9f9",
                               "version":"2.0b", "parameters":""}],
                   images=[{"url":"http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                            "caption":"NEURON Logo"},
                           {"url":"https://collab.humanbrainproject.eu/assets/hbp_diamond_120.png",
                            "caption":"HBP Logo"}])
   return model_catalog, model_id

#
# def pytest_sessionfinish(session, exitstatus):
#    model_catalog = ModelCatalog(username=HBP_USERNAME, password=HBP_PASSWORD, environment="production")
#    models = model_catalog.list_models(app_id="359330", author="Shailesh Appukuttan")
#    for model in models:
#       model_catalog.delete_model(model["id"])
