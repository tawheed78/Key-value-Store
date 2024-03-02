from pydantic import BaseModel

class Key_value_Db(BaseModel):
    key : str
    value : dict
    