from enum import Enum
from typing import Literal  # For type hinting (optional, but good practice)

class ModelName(str, Enum):
    ALEXNET = "alexnet"
    RESNET = "resnet"
    VGG = "vgg"

def load_model(model_name: ModelName):  # Type hint: model_name must be one of the enum members
    if model_name == ModelName.ALEXNET:
        print("Loading AlexNet...")
    elif model_name == ModelName.RESNET:
        print("Loading ResNet...")
    elif model_name == ModelName.VGG:
        print("Loading VGG...")
    else:
        raise ValueError("Invalid model name")

# Using the enum:
model = ModelName.RESNET
load_model(model)  # Works perfectly!

# Because ModelName inherits from str, you can also do this:
model_str = str(ModelName.RESNET)  # model_str will be "resnet"
print("kk",model_str)

# Error prevention:
# load_model("resnet")  # This would cause a type error (if using mypy) because "resnet" is a str, not ModelName
# load_model(ModelName.RESNET2) # This would cause an AttributeError because RESNET2 is not defined in ModelName

# Iterating through enum members:
for model in ModelName:
    print(f"Model: {model.name}, Value: {model.value}")