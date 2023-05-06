import torch
from torchvision import models
def trans_model():
    #在以下begin-end之间完成resnet50模型的下载和迁移过程
    ###############begin################
    model = models.resnet50(pretrained=True)
    num_ftrs = model.fc.in_features
    for param in model.parameters():
        param.requires_grad=False

    model.fc = torch.nn.Linear(in_features=num_ftrs, out_features=2, bias=True)

    #################end################
    
    return model