import pytest
import uuid

"""
Add an image to a model
"""

#1) With valid details
def test_addImage_valid(params):
    model_catalog, model_id = params
    model_image = model_catalog.add_model_image(model_id=model_id,
                                                url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                caption="NEURON Logo")
    assert isinstance(uuid.UUID(model_image, version=4), uuid.UUID)

#2) With no model_id
def test_addImage_no_id(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.add_model_image(url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert excinfo.value.message == "Model ID needs to be provided for finding the model."

#3) With invalid model_id format
def test_addImage_invalid_id_format(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.add_model_image(model_id="blahblah",
                                                    url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in excinfo.value.message

#4) With invalid model_id value
def test_addImage_invalid_id_value(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.add_model_image(model_id=str(uuid.uuid4()),
                                                    url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in excinfo.value.message

#5) With missing info (url), but valid model_id
def test_addImage_missing(params):
    model_catalog, model_id = params
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.add_model_image(model_id=model_id,
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in excinfo.value.message
