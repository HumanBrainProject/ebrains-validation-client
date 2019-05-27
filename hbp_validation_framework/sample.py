import sciunit
from sciunit import Model, Test, Score

import quantities
import os


class SampleScore(Score):
    """For testing purposes"""
    @classmethod
    def compute(cls):
        return SampleScore(1.0)


class SampleTest(Test):
    """For testing purposes"""

    score_type = SampleScore

    def __init__(self,
                 observation={},
                 name="Sample Test"):
        required_capabilities = ()
        sciunit.Test.__init__(self, observation, name)

    def validate_observation(self, observation):
        pass

    def generate_prediction(self, model, verbose=False):
        return 1.0

    def compute_score(self, observation, prediction, verbose=False):
        return SampleScore.compute()

class SampleModel(Model):
    """For testing purposes"""
    def __init__(self, name = "Test Model", model_uuid="", model_version="", model_instance_uuid=""):
        sciunit.Model.__init__(self, name=name)
        self.model_uuid = model_uuid
        self.model_version = model_version
        self.model_instance_uuid = model_instance_uuid
