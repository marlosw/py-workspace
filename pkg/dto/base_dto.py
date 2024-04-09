import json


class BaseDTO(dict):
    def __init__(self, **kwargs):
      pass  

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
class BaseDTOEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__