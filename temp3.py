import torch
from torchvision import models
resnetv101 = models.resnet101()
print(resnetv101.fc)