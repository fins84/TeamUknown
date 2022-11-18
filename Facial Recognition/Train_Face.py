import cv2 as cv
import torch

model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet50', pretrained=True)