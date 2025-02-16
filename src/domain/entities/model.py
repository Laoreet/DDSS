from utils.base_uuid import BaseId


class ModelId(BaseId):
    pass


class Model:
    def __init__(
        self,
        model_id: "ModelId",
        model_path: str
    ):
        self.model_id = model_id
        self.model_path = model_path

    def __eq__(self, other: "Model"):
        return self.model_id == other.model_id

    def __ne__(self, other: "Model"):
        return self.model_id != other.model_id
