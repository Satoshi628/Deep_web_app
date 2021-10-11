import os
import re

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from PIL import Image
import torchvision.transforms as transforms
import torchvision.models as models

import copy

device = torch.device("cuda:0")

def image_transpose(Style_image_list, Content_image_list):
    style_tensor = []
    content_tensor = []
    for item_style, item_content in zip(Style_image_list, Content_image_list):
        style_image = image = Image.open(
            "Style_Image/{}".format(item_style)).convert('RGB')
        content_image = image = Image.open(
            "Content_Image/{}".format(item_content)).convert('RGB')
        # Content_imageに大きさを合わせる
        content_size = content_image.size[-2:]
        # データ変換
        preprocess_image = transforms.Compose([
            transforms.Resize(content_size[::-1]),
            transforms.ToTensor()
        ])
        style_tensor.append(preprocess_image(
            style_image).unsqueeze(0).cuda(device))
        content_tensor.append(preprocess_image(
            content_image).unsqueeze(0).cuda(device))
    return style_tensor, content_tensor

class ContentLoss(nn.Module):
    def __init__(self, target,):
        super(ContentLoss, self).__init__()
        self.target = target.detach()

    def forward(self, inputs):
        self.loss = F.mse_loss(inputs, self.target)
        return inputs


def gram_matrix(inputs):
    a, b, c, d = inputs.size()
    features = inputs.view(a * b, c * d)
    G = torch.mm(features, features.t())
    return G.div(a * b * c * d)


class StyleLoss(nn.Module):
    def __init__(self, target_feature):
        super(StyleLoss, self).__init__()
        self.target = gram_matrix(target_feature).detach()

    def forward(self, inputs):
        G = gram_matrix(inputs)
        self.loss = F.mse_loss(G, self.target)
        return inputs


class Normalization(nn.Module):
    def __init__(self):
        super(Normalization, self).__init__()
        mean = torch.tensor([0.485, 0.456, 0.406]).to(device)
        std = torch.tensor([0.229, 0.224, 0.225]).to(device)
        self.mean = mean.view(-1, 1, 1)
        self.std = std.view(-1, 1, 1)

    def forward(self, img):
        # normalize img
        return (img - self.mean) / self.std


def make_model(style_tensor, content_tensor):
    content_layers_default = [11]
    style_layers_default = [1, 3, 5, 8, 11]
    cnn = models.vgg19(pretrained=True).features.to(device).eval()
    content_losses = []
    style_losses = []
    model = nn.Sequential(Normalization())
    i = 0
    for item in cnn.children():
        if isinstance(item, nn.Conv2d):
            i += 1
            model.add_module("Conv2d:{}".format(i), item)
            if i in content_layers_default:
                target = model(content_tensor)
                content_loss = ContentLoss(target)
                model.add_module("content_loss:{}".format(i), content_loss)
                content_losses.append(content_loss)

            if i in style_layers_default:
                target = model(style_tensor)
                style_loss = StyleLoss(target)
                model.add_module("style_loss:{}".format(i), style_loss)
                style_losses.append(style_loss)
        if isinstance(item, nn.ReLU):
            model.add_module("ReLU:{}".format(i), nn.ReLU(inplace=False))
        if isinstance(item, nn.MaxPool2d):
            model.add_module("pool:{}".format(i), item)

    for i in range(len(model) - 1, -1, -1):
        if isinstance(model[i], ContentLoss) or isinstance(model[i], StyleLoss):
            break

    model = model[:(i + 1)]
    return model, style_losses, content_losses


def run_transfor(style_tensor, content_tensor, step=300, style_weight=1e6, content_weight=1):
    input_tensor = content_tensor
    model, style_losses, content_losses = make_model(style_tensor, content_tensor)
    optimizer = optim.LBFGS([input_tensor.requires_grad_()])

    # 高速化コードただし計算の再現性は無くなる
    torch.backends.cudnn.benchmark = True
    #closureを使う際、for文だと処理が重複している？
    #またrun = [0]じゃないとclusure内でrun変数が使えなくなる
    #理由不明
    run = [0]
    while run[0] <= step:
        def closure():
            # correct the values of updated input image
            input_tensor.data.clamp_(0, 1)

            optimizer.zero_grad()
            model(input_tensor)
            style_score = 0
            content_score = 0

            for sl in style_losses:
                style_score += sl.loss
            for cl in content_losses:
                content_score += cl.loss

            style_score *= style_weight
            content_score *= content_weight

            loss = style_score + content_score
            loss.backward()
            run[0] += 1
            if run[0] % 50 == 0:
                print("iteration:{}:".format(run[0]))
                print('Style Loss : {:4f} Content Loss: {:4f}'.format(
                    style_score.item(), content_score.item()))
                print()

            return style_score + content_score

        optimizer.step(closure)
    input_tensor.data.clamp_(0, 1)

    return input_tensor


if __name__ == "__main__":
    # 模様と入力画像は同じ枚数でなくてはいけない
    Style_image_list = sorted(os.listdir("Style_Image"))
    Content_image_list = sorted(os.listdir("Content_Image"))
    C_name = [re.sub('^\d+', '', item).split('.')[0] for item in Content_image_list]
    style_tensor, content_tensor = image_transpose(Style_image_list, Content_image_list)
    """
    output = run_transfor(style_tensor[1], content_tensor[1])
    output = 255 * output.permute(0, 2, 3, 1).squeeze()
    output = output.to('cpu').detach().numpy().astype(np.uint8)
    plt.figure()
    plt.imshow(output)
    plt.savefig('Output_Image/{}.png'.format(C_name[1]))
    plt.close()
    """
    
    for S_tensor, C_tensor, name in zip(style_tensor, content_tensor, C_name):
        output = run_transfor(S_tensor, C_tensor)
        output = 255 * output.permute(0, 2, 3, 1).squeeze()
        output = output.to('cpu').detach().numpy().astype(np.uint8)
        img = Image.fromarray(output)
        img.save('Output_Image/{}.png'.format(name))
