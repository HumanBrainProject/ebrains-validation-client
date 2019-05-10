import pytest
import uuid

"""
Add a model instance
"""

#1) With valid details
def test_addInstance_valid(params):
    model_catalog, model_id = params
    model_instance = model_catalog.add_model_instance(model_id=model_id,
                                                       source="https://www.12345.com",
                                                       version="3.0",
                                                       parameters="",
                                                       code_format="",
                                                       hash="",
                                                       morphology="",
                                                       description="")
    assert isinstance(uuid.UUID(model_instance, version=4), uuid.UUID)

#2) With no model_id
def test_addInstance_no_id(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(source="https://www.12345.com",
                                                            version="4.0",
                                                            parameters="",
                                                            code_format="",
                                                            hash="",
                                                            morphology="",
                                                            description="")
    assert excinfo.value.message == "Model ID needs to be provided for finding the model."

#3) With invalid model_id format
def test_addInstance_invalid_id_format(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(model_id="abcde",
                                                           source="https://www.12345.com",
                                                           version="5.0",
                                                           parameters="",
                                                           code_format="",
                                                           hash="",
                                                           morphology="",
                                                           description="")
    assert "Error in adding model instance." in excinfo.value.message

#4) With invalid model_id value
def test_addInstance_invalid_id_value(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_instance = model_catalog.add_model_instance(model_id=str(uuid.uuid4()),
                                                           source="https://www.12345.com",
                                                           version="6.0",
                                                           parameters="",
                                                           code_format="",
                                                           hash="",
                                                           morphology="",
                                                           description="")
    assert "Error in adding model instance." in excinfo.value.message

#5) With duplicate version number
def test_addInstance_duplicate_version(params):
    model_catalog, model_id = params
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
    assert "Error in adding model instance." in excinfo.value.message
