import pytest
import uuid

"""
1. Get an image associated with a model
"""

#1.1) With valid details
def test_getImage_valid(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_image = model_catalog.get_model_image(image_id=model["images"][0]["id"])
    assert model_image["id"] == model["images"][0]["id"]

#1.2) With no image_id
def test_getImage_no_id(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.get_model_image()
    assert str(excinfo.value) == "image_id needs to be provided for finding a specific model image (figure)."

#1.3) With invalid image_id format
def test_getImage_invalid_id_format(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.get_model_image(image_id="blahblah")
    assert "Error in retrieving model images (figures)." in str(excinfo.value)

#1.4) With invalid image_id value
def test_getImage_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image = model_catalog.get_model_image(image_id=str(uuid.uuid4()))
    assert "Error in retrieving model image." in str(excinfo.value)


"""
2. List all images associated with a model
"""

#2.1) With valid details - model_id
def test_listImages_valid_id(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_images = model_catalog.list_model_images(model_id=model_id)
    assert isinstance(model_images, list)
    assert len(model_images) > 0

#2.2) With valid details - alias
def test_listImages_valid_alias(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_images = model_catalog.list_model_images(alias=model["alias"])
    assert isinstance(model_images, list)
    assert len(model_images) > 0

#2.3) With no model_id or alias
def test_listImages_no_id(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_images = model_catalog.list_model_images()
    assert str(excinfo.value) == "model_id or alias needs to be provided for finding model images."

#2.4) With invalid model_id format
def test_listImages_invalid_id_format(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_images = model_catalog.list_model_images(model_id="blahblah")
    assert "Error in retrieving model images (figures)." in str(excinfo.value)

#2.5) With invalid model_id value
def test_listImages_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_images = model_catalog.list_model_images(model_id=str(uuid.uuid4()))
    assert "Error in retrieving model images (figures)." in str(excinfo.value)

#2.6) With invalid alias value
@pytest.mark.xfail
def test_listImages_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_images = model_catalog.list_model_images(alias=str(uuid.uuid4()))
    assert "Error in retrieving model images (figures)." in str(excinfo.value)

"""
3. Add an image to a model
"""

#3.1) With valid details
def test_addImage_valid(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_image_id = model_catalog.add_model_image(model_id=model_id,
                                                url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                caption="NEURON Logo")
    assert isinstance(uuid.UUID(model_image_id, version=4), uuid.UUID)

#3.2) With no model_id
def test_addImage_no_id(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.add_model_image(url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert str(excinfo.value) == "Model ID needs to be provided for finding the model."

#3.3) With invalid model_id format
def test_addImage_invalid_id_format(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.add_model_image(model_id="blahblah",
                                                    url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in str(excinfo.value)

#3.4) With invalid model_id value
def test_addImage_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.add_model_image(model_id=str(uuid.uuid4()),
                                                    url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in str(excinfo.value)

#3.5) With missing info (url), but valid model_id
def test_addImage_missing(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.add_model_image(model_id=model_id,
                                                    caption="NEURON Logo")
    assert "Error in adding image (figure)." in str(excinfo.value)


#3.6) With valid dauplicate data
def test_addImage_valid_duplicate(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model_image_id = model_catalog.add_model_image(model_id=model_id,
                                                url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                caption="NEURON Logo Double")
    assert isinstance(uuid.UUID(model_image_id, version=4), uuid.UUID)
    model_image_id = model_catalog.add_model_image(model_id=model_id,
                                                url="http://www.neuron.yale.edu/neuron/sites/default/themes/xchameleon/logo.png",
                                                caption="NEURON Logo Double")
    assert isinstance(uuid.UUID(model_image_id, version=4), uuid.UUID)

"""
4. Edit an image associated with a model
"""

#4.1) With valid details
def test_editImage_url_valid(modelCatalog, myModelID):
    model_catalog = modelCatalog
    model_id = myModelID
    model = model_catalog.get_model(model_id=model_id)
    model_image_id = model_catalog.edit_model_image(image_id=model["images"][0]["id"],
                                                url="http://www.abcde.com/logo_1.png",
                                                caption="New Caption 1")
    assert model_image_id == model["images"][0]["id"]
    model_image = model_catalog.get_model_image(image_id=model_image_id)
    assert model_image["url"] == "http://www.abcde.com/logo_1.png"
    assert model_image["caption"] == "New Caption 1"

#4.2) With no image_id
def test_editImage_no_id(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.edit_model_image(url="http://www.abcde.com/logo_2.png",
                                                    caption="New Caption 2")
    assert str(excinfo.value) == "Image ID needs to be provided for finding the image (figure)."

#4.3) With invalid image_id format
def test_editImage_invalid_id_format(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.edit_model_image(image_id="blahblah",
                                                    url="http://www.abcde.com/logo_3.png",
                                                    caption="New Caption 3")
    assert "Error in retrieving model images (figures)." in str(excinfo.value)

#4.4) With invalid image_id value
def test_editImage_invalid_id_value(modelCatalog):
    model_catalog = modelCatalog
    with pytest.raises(Exception) as excinfo:
        model_image_id = model_catalog.edit_model_image(image_id=str(uuid.uuid4()),
                                                    url="http://www.abcde.com/logo_4.png",
                                                    caption="New Caption 4")
    assert "Error in retrieving model image." in str(excinfo.value)
