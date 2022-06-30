from enum import Enum

class Tags(Enum):
    items = "items"
    users = "users"

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"