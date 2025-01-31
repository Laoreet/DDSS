from domain.entities.model import Model
from domain.entities.model_results import ModelResults
from domain.entities.attention_maps import AttentionMaps


class ModelAggregate:
    def __init__(self, model: Model, model_results: ModelResults = None,
                 attention_maps: AttentionMaps = None):
        self.model = model
        self.model_results = model_results
        self.attention_maps = attention_maps
