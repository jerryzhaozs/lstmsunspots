# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:44:13 2023

@author: Administrator
"""

import torch
import torchvision.transforms as transforms
from PIL import Image
from torch import nn
device='cpu'
def load_image(img_path, max_size=400, shape=None):
    '''
        加载图片
        图片格式设置： 高/宽<=400px
    '''
    image = Image.open(img_path).convert('RGB')
    
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
    
    if shape is not None:
        size = shape
        
    in_transform = transforms.Compose([
                        transforms.Resize(size),
                        transforms.ToTensor(),# 转换为一个tensor张量 值(0-255)转换成0-1
                        transforms.Normalize((0.485, 0.456, 0.406), # 将张量的像素值标准化为指定的平均值和标准偏差。这些值是基于训练VGG19模型的ImageNet数据集预先确定的。
                                             (0.229, 0.224, 0.225))])

    # 处理content文件设置其大小，转化为tenso并将张量的像素值标准化为指定的平均值和标准偏差
    image= in_transform(image)
    image=image[:3,:,:]# 保留RGB三通道量
    image=image.unsqueeze(0)# VGG19模型期望输入图像在开始时具有批次维度（即，输入形状应为（batch_size、num_channels、height、width）所以应该在开头添加一个新的维度
    return image
class model(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Conv2d(3,3,(3,3)),
            nn.MaxPool2d((3,3),stride=4),
            nn.Conv2d(3, 3, (3,3)),
            nn.MaxPool2d((3,3),stride=2),
            nn.Flatten()
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits

model = model().to(device)
structure = torch.nn.Sequential(*list(model.children())[:])
print(structure)
for a,b in model._modules.items():
    print(f'{a}--{b}')