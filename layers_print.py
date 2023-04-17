# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:19:28 2023

@author: Administrator
"""

from torchvision import models
import torch
vgg = models.vgg19(pretrained=True).features

structure = torch.nn.Sequential(*list(vgg.children())[:])
print(structure)