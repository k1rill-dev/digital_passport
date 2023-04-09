import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
from PIL import Image, ImageOps
import os
import torch.nn as nn
from facenet_pytorch import MTCNN
import base64
import io
import re

mtcnn = MTCNN()

transformation = transforms.Compose([transforms.Resize((100, 100)),
                                     transforms.ToTensor()
                                     ])


class SiameseNetwork(nn.Module):

    def __init__(self):
        super(SiameseNetwork, self).__init__()

        # Setting up the Sequential of CNN Layers
        self.cnn1 = nn.Sequential(
            nn.Conv2d(1, 96, kernel_size=11, stride=4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, stride=2),

            nn.Conv2d(96, 256, kernel_size=5, stride=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, stride=2),

            nn.Conv2d(256, 384, kernel_size=3, stride=1),
            nn.ReLU(inplace=True)
        )

        # Setting up the Fully Connected Layers
        self.fc1 = nn.Sequential(
            nn.Linear(384, 1024),
            nn.ReLU(inplace=True),

            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),

            nn.Linear(256, 2)
        )

    def forward_once(self, x):
        # This function will be called for both images
        # It's output is used to determine the similiarity
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        # In this function we pass in both images and obtain both vectors
        # which are returned
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)

        return output1, output2


def photo_format(photo):
    im = Image.open(photo)
    f, e = os.path.splitext(photo)
    print(f, e)
    im = mtcnn(im, save_path=f + e)
    im = Image.open(f + e)
    imResize = im.resize((92, 112))
    imResize = ImageOps.grayscale(imResize)
    imResize.save(f + 'cropped' + e, quality=100)
    return imResize


# %%
def find_difference(first_photo, second_photo):
    first = transformation(photo_format(first_photo)).unsqueeze(0)
    second = transformation(Image.open(second_photo)).unsqueeze(0)
    output1, output2 = model(first, second)
    euclidean_distance = F.pairwise_distance(output1, output2)
    return euclidean_distance.item()


model = SiameseNetwork()
model.load_state_dict(torch.load('/home/kirill-dev/PycharmProjects/digital_password/passport/model5.pth',
                                 map_location=torch.device('cpu')))
