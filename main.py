import torch
import torchvision
import os
import torchvision.datasets as dset
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.sparse as sp
from message_pass import SparseMP
from random import random


if __name__ == "__main__":
    # Set torch device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    root = './data'
    if not os.path.exists(root):
        os.mkdir(root)

    # Generate k-regular graph
    n, k = 10000, 5
    G = nx.random_regular_graph(k, n, seed=42)
    sparse_adj = nx.adjacency_matrix(G)
    _, col = sparse_adj.nonzero()
    adj_list = torch.from_numpy(col.reshape(n, -1)).type(torch.LongTensor)
    adj = torch.ones(n, k) * 0.5
    local = torch.rand(n) - 0.5

    trans = transforms.Compose([transforms.ToTensor()])
    # if data does not exist, download mnist dataset
    train_set = dset.MNIST(root=root, train=True, transform=trans, download=True)
    model = SparseMP(adj=adj, local=local, adj_list=adj_list, epochs=1, batch_size=1)
    model.train(train_set=train_set)

    #Generate n samples from graphical model
    # n = 4
    # plt.figure(figsize=(4.2, 4))
    # X0 = torch.round(train_set[0][0].squeeze(0))
    # print(X0.size())
    # plt.subplot(n + 1, 1, 1)
    # plt.imshow(X0, cmap=plt.cm.gray_r, interpolation='nearest')
    # for i in range(1, n + 1):
    #     plt.subplot(n + 1, 1, i + 1)
    #     plt.imshow(model.gibbs(X0, 100), cmap=plt.cm.gray_r, interpolation='nearest')
    #     plt.xticks(())
    #     plt.yticks(())
    #     print("SMP: " + str(i) + " images generated.")
    # plt.suptitle('Regenerated numbers', fontsize=16)
    # plt.subplots_adjust(0.08, 0.02, 0.92, 0.85, 0.08, 0.23)
    # plt.show()
