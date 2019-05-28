import pytest
import uuid

"""
1. Get an instance of a test
"""

#1.1) With valid details - instance_id
def test_getTestInstance_valid_id(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance = test_library.get_test_instance(instance_id=test["codes"][0]["id"])
    assert test_instance["id"] == test["codes"][0]["id"]

#1.2) With valid details - test_id, version
def test_getTestInstance_valid_test_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance = test_library.get_test_instance(test_id=test_id, version=test["codes"][0]["version"])
    assert test_instance["id"] == test["codes"][0]["id"]

#1.3) With valid details - alias, version
def test_getTestInstance_valid_alias_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance = test_library.get_test_instance(alias=test["alias"], version=test["codes"][0]["version"])
    assert test_instance["id"] == test["codes"][0]["id"]

#1.4) With valid details - only test_id, retrieve latest
def test_getTestInstance_invalid_only_test(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test_instance = test_library.get_test_instance(test_id=test_id)
    assert test_instance["version"] == "2.0"


#1.5) With valid details - only alias, retrieve latest
def test_getTestInstance_invalid_only_alias(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance = test_library.get_test_instance(alias=test["alias"])
    assert test_instance["version"] == "2.0"

#1.6) With invalid details - only version
def test_getTestInstance_invalid_only_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.get_test_instance(version=test["codes"][0]["version"])
    assert str(excinfo.value) == "instance_path or instance_id or test_id or alias needs to be provided for finding a test instance."


"""
2. List all instances of a test
"""

#2.1) With valid details - test_id
def test_listTestInstances_valid_test_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instances = test_library.list_test_instances(test_id=test_id)
    assert isinstance(test_instances, list)
    assert len(test_instances) > 0

#2.2) With valid details - alias
def test_listTestInstances_valid_alias_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instances = test_library.list_test_instances(alias=test["alias"])
    assert isinstance(test_instances, list)
    assert len(test_instances) > 0

#2.3) With invalid details - no test_id or alias
def test_listTestInstances_invalid_noInput(testLibrary):
    test_library = testLibrary
    with pytest.raises(Exception) as excinfo:
        test_instances = test_library.list_test_instances()
    assert str(excinfo.value) == "instance_path or test_id or alias needs to be provided for finding test instances."


"""
3. Add an instance to a test
"""

#3.1) With valid details
def test_addTestInstance_valid(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test_instance = test_library.add_test_instance(test_id=test_id, version="3.0",
                                                    repository="http://www.12345.com",
                                                    path="hbp_validation_framework.sample.SampleTest",
                                                    parameters="",
                                                    description="")
    assert isinstance(uuid.UUID(test_instance, version=4), uuid.UUID)

#3.2) With no test_id
def test_addTestInstance_no_id(testLibrary):
    test_library = testLibrary
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.add_test_instance(version="4.0",
                                                        repository="http://www.12345.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="",
                                                        description="")
    assert str(excinfo.value) == "test_id needs to be provided for finding the test."

#3.3) With invalid test_id format
def test_addTestInstance_invalid_id_format(testLibrary):
    test_library = testLibrary
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.add_test_instance(test_id="abcde", version="5.0",
                                                        repository="http://www.12345.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="",
                                                        description="")
    assert "Error in adding test instance." in str(excinfo.value)

#3.4) With invalid test_id value
def test_addTestInstance_invalid_id_value(testLibrary):
    test_library = testLibrary
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.add_test_instance(test_id=str(uuid.uuid4()), version="6.0",
                                                        repository="http://www.12345.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="",
                                                        description="")
    assert "Error in adding test instance." in str(excinfo.value)

#3.5) With duplicate version
def test_addTestInstance_duplicate_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test_instance = test_library.add_test_instance(test_id=test_id, version="7.0",
                                                    repository="http://www.12345.com",
                                                    path="hbp_validation_framework.sample.SampleTest",
                                                    parameters="",
                                                    description="")
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.add_test_instance(test_id=test_id, version="7.0",
                                                    repository="http://www.12345.com",
                                                    path="hbp_validation_framework.sample.SampleTest",
                                                    parameters="",
                                                    description="")
    assert "Error in adding test instance." in str(excinfo.value)


"""
4. Edit an instance of a test
"""

#4.1) With valid details - instance_id
def test_editTestInstance_valid_id(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance_id = test_library.edit_test_instance(instance_id=test["codes"][0]["id"],
                                                        repository="http://www.12345.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="d",
                                                        description="e")["id"]
    assert test_instance_id == test["codes"][0]["id"]
    test_instance = test_library.get_test_instance(instance_id=test_instance_id)
    assert test_instance["repository"] == "http://www.12345.com"
    assert test_instance["path"] == "hbp_validation_framework.sample.SampleTest"
    assert test_instance["parameters"] == "d"
    assert test_instance["description"] == "e"

#4.2) With valid details - test_id, version
@pytest.mark.xfail # see https://github.com/HumanBrainProject/hbp-validation-framework/issues/168
def test_editTestInstance_valid_test_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance_id = test_library.edit_test_instance(test_id=test_id, version=test["codes"][0]["version"],
                                                        repository="http://www.12345.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="d",
                                                        description="e")
    assert test_instance_id == test["codes"][0]["id"]
    test_instance = test_library.get_test_instance(test_id=test_instance_id)
    assert test_instance["repository"] == "https://www.12345.com"
    assert test_instance["path"] == "hbp_validation_framework.sample.SampleTest"
    assert test_instance["parameters"] == "d"
    assert test_instance["description"] == "e"

#4.3) With valid details - alias, version
@pytest.mark.xfail # see https://github.com/HumanBrainProject/hbp-validation-framework/issues/168
def test_editTestInstance_valid_alias_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    test_instance_id = test_library.edit_test_instance(alias=test["alias"], version=test["codes"][0]["version"],
                                                        repository="https://www.abcde.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="d",
                                                        description="e")
    assert test_instance_id == test["codes"][0]["id"]
    test_instance = test_library.get_test_instance(instance_id=test_instance_id)
    assert test_instance["repository"] == "https://www.12345.com"
    assert test_instance["path"] == "hbp_validation_framework.sample.SampleTest"
    assert test_instance["parameters"] == "d"
    assert test_instance["description"] == "e"

#4.4) With invalid details - only test_id
def test_editTestInstance_invalid_only_test(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.edit_test_instance(test_id=test_id,
                                                        repository="https://www.abcde.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="a",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (test_id, version) or (alias, version) needs to be provided for finding a test instance."

#4.5) With invalid details - only alias
def test_editTestInstance_invalid_only_alias(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.edit_test_instance(alias=test["alias"],
                                                        repository="https://www.abcde.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="a",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (test_id, version) or (alias, version) needs to be provided for finding a test instance."

#4.6) With invalid details - only version
def test_editTestInstance_invalid_only_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test = test_library.get_test_definition(test_id=test_id)
    with pytest.raises(Exception) as excinfo:
        test_instance = test_library.edit_test_instance(version=test["codes"][0]["version"],
                                                        repository="https://www.abcde.com",
                                                        path="hbp_validation_framework.sample.SampleTest",
                                                        parameters="a",
                                                        description="e")
    assert str(excinfo.value) == "instance_id or (test_id, version) or (alias, version) needs to be provided for finding a test instance."

#4.7) With valid details - change version
def test_editTestInstance_valid_change_version(testLibrary, myTestID):
    test_library = testLibrary
    test_id = myTestID
    test_instance_id = test_library.add_test_instance(test_id=test_id, version="1.0_edit",
                                                    repository="http://www.12345.com",
                                                    path="hbp_validation_framework.sample.SampleTest",
                                                    parameters="",
                                                    description="")
    test_instance_id = test_library.edit_test_instance(instance_id=test_instance_id,
                                                        version="a.1_edit")
    test_instances = test_library.list_test_instances(test_id=test_id)
    assert "1.0_edit" not in [i["version"] for i in test_instances] and "a.1_edit" in [i["version"] for i in test_instances]
