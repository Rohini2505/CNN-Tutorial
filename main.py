import argparse
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
from torch.autograd import Variable
from data import classes, basicTransform, augmentedTransform
from train_and_eval import train, evaluate
from model import CNN

'''Setup command line arguments'''
parser = argparse.ArgumentParser(description='CNN tutorial')
parser.add_argument('--lr', type=float, default=0.001,
                    help='learning rate (default: 0.001)')
parser.add_argument('--bs', type=int, default=32,
                    help='batch size (default 32)')
parser.add_argument('--epochs', type=int, default=10,
                    help='number epochs (default 10)')
parser.add_argument('--transforms', type=str, default='basic',
                    help='which transforms to use (default = "basic", others opts: "augmented")')
parser.add_argument('--cuda', type=int, default=1,
                    help='whether to use cuda')
parser.add_argument('--device', type=int, default=0,
                    help='select GPU device')
parser.add_argument('--nettype', type=int, default=0,
                    help='which type of CNN to use (default = 0: basic, 1 = VGG like, 2 = ResNet)')
parser.add_argument('--dropout', type=float, default=0.4,
                    help='dropout percentage (default: 0.4)')
args = parser.parse_args()
print(args)

'''Setup hyperparameters from command line options'''
batch_size = args.bs
num_epochs = args.epochs
learning_rate = args.lr
cuda = args.cuda
cuda_device = args.device
dropout = args.dropout
transform = augmentedTransform if args.transforms == 'augmented' else basicTransform
nclasses = 10

'''Load training and test data'''
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                          shuffle=True, num_workers=2)

testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                         shuffle=False, num_workers=2)

'''Initialize network, optimizer, and loss function'''
if args.nettype == 0:
    net = CNN(dropout, nclasses)
    name = 'basicCNN'
elif args.nettype == 1:
    print("Not implemented yet")
    sys.exit()
elif args.nettype == 2:
    print("Not implmented yet")
    sys.exit()
else:
    print("Unknown net type")
    sys.exit()
print(net)
optimizer = optim.Adam(net.params, lr=learning_rate)
criterion = nn.CrossEntropyLoss()

'''Convert to cuda if available'''
if torch.cuda.is_available() and cuda:
    print("CUDA is available, training on GPU")
    print("Number of available devices: {}".format(torch.cuda.device_count()))
    print("Using device: {}".format(cuda_device))
    torch.cuda.device(args.device)
    net.cuda()
    loss = loss.cuda()
else:
    print("CUDA is NOT available, training on CPU")

'''Train and evaluate model'''
for i in range(1, num_epochs + 1):
    train(i, net, trainloader, criterion, optimizer, cuda, batch_size)
    evaluate(i, net, testloader, criterion, optimizer, cuda, batch_size)
    torch.save(net.state_dict(), "./models/" + name + "_" + str(i) + ".pth")
