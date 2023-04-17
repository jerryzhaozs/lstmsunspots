from PIL import Image
import matplotlib
import numpy as np
import time
import torch
import torch.optim as optim
from torchvision import transforms, models

strt = time.time()
# 获得与训练完成的vgg参数
vgg = models.vgg19(pretrained=True).features

# 冻结参数以避免在迭代中参数改变
for param in vgg.parameters():
    param.requires_grad_(False)
# 选择cpu为计算设施
device = torch.device("cpu")
vgg.to(device)

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

# 加载content文件
content= load_image('I:/lijuan/imgs/input.jpg').to(device)
# 加载style图片，设置大小与content文件相同
style= load_image('I:/lijuan/imgs/starry_night.jpg', shape=content.shape[-2:]).to(device)

#%%
def im_convert(tensor):
    """
        将tensor转化为图片
    """
    
    image = tensor.to("cpu").clone().detach() #去除梯度
    image = image.numpy().squeeze() # 减小一维
    image = image.transpose(1,2,0) # 调整维度顺序
    # 将归一化用于tensor张量
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)# 设置值区间0-1之间
    return image

def get_features(image, model, layers=None):
    """ 
        使图片从模型各模块通过，并保存需要模块的输出
    """
    # structure = torch.nn.Sequential(*list(vgg.children())[:])
    # print(structure)
    if layers is None:
        layers = {'0': 'conv1_1',
                  '5': 'conv2_1', 
                  '10': 'conv3_1', 
                  '19': 'conv4_1',
                  '28': 'conv5_1'}
        
    features = {}
    x = image
    # 使图片x通过每个模块，如果name在layers中则将feature保存到features中
    for name, layer in model._modules.items():
        print(name)
        x = layer(x)
        if name in layers:
            features[layers[name]] = x # key为层数名字，value为tensor张量
        if name=='28': # 获取结束跳出循环
            break
    return features

def gram_matrix(tensor):
    """
        计算gram matrix
    """
    # 获取vgg19中规定的tensor格式数据（batch_size，depth，height和width）
    _, d, h, w = tensor.size()
    
    # reshape来计算每个channel之间的积
    tensor = tensor.view(d, h * w)
    
    # 计算gram matrix
    gram = torch.mm(tensor, tensor.t())
    
    return gram
#%%

# 在开始生成图片前获取content和style的特征
content_features = get_features(content, vgg)
style_features = get_features(style, vgg)

# 为每一层的style计算gram matrix
style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

# 创建目标图片令其与content相同并逐步更新改变其style
target = content.clone().requires_grad_(True).to(device)

style_weights = {'conv1_1': 0.2,
                 'conv2_1': 0.4,
                 'conv3_1': 0.2,
                 'conv4_1': 0.1,
                 'conv5_1': 0.1}

content_weight = 1  # content权重
style_weight = 1e12  # style权重比content大很多是因为style图片需要更深入的了解才能捕获到其特征而content的特征很容易就可以捕获到

# 设置更新器
optimizer = optim.Adam([target], lr=0.2)
steps = 1  # 迭代更新目标图片的次数

for ii in range(1, steps+1):
    
    # 获取目标图片每一层的特征
    target_features = get_features(target, vgg)
    
    # 计算content损失
    content_loss = torch.mean((target_features['conv4_1'] - content_features['conv4_1'])**2)
    
    # 初始化style损失为0
    style_loss = 0
    # 在每一层中计算style损失并添加到总style损失中
    for layer in style_weights:
        # 为目标层的目标图片的特征计算gram matrix
        target_feature = target_features[layer]
        target_gram = gram_matrix(target_feature)
        _, d, h, w = target_feature.shape
        # 获取相应层图像的gram matrix
        style_gram = style_grams[layer]
        # 根据每一层的权重计算每一层中的style损失
        layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram)**2)
        # 添加到总style loss中
        style_loss += layer_style_loss / (d * h * w) # 消去图片大小对loss的影响
        
    # 计算损失和 total loss
    total_loss = content_weight * content_loss + style_weight * style_loss
    print(f"content loss:{content_weight * content_loss}")
    print(f"style loss:{style_weight * style_loss}")
    # 更新目标图片
    optimizer.zero_grad()# 清空梯度
    total_loss.backward()# 反向传播计算梯度
    optimizer.step()# 更新
    print(f"epoch:{ii}")
#%%

# 将tensor张量转化为图片
final = im_convert(target)
matplotlib.image.imsave('I:/lijuan/imgs/result.jpg', final)
# 花费时间
end = time.time()
print(f"cost time:{end-strt}")