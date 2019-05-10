from hbp_validation_framework import BaseClient

HBP_USERNAME = "ValidationTester"
HBP_PASSWORD = "PyNNis2good!"

def test_baseClient_authenticate():
    base_client = BaseClient(username=HBP_USERNAME, password=HBP_PASSWORD, environment="production")
    assert base_client.token is not None
