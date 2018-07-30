# import scipy.sparse
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as mpl
import scipy.sparse.linalg
import json
import tsne

# Import DBSCAN-related things
from sklearn.cluster import DBSCAN
from sklearn import metrics

# Read files in
merged_mbtr = np.loadtxt('merged_mbtr.txt')
print(merged_mbtr)
n = (1/4)*len(merged_mbtr[0])
print(n)

file = open('nodes.json')
nodes = json.load(file)
file.close()

# Implement t-SNE method
X = merged_mbtr
print(X.shape)
#labels = nodes
Y = tsne.tsne(X, 2, int(n), 5.0)
print(Y)

# Add X and Y to node dictionary
for i, loc in enumerate(Y):
    i_node = nodes[i]
    i_node['x'] = loc[0]
    i_node['y'] = loc[1]

file = open('nodes_json.json','w')
json.dump(nodes,file)
file.close()

mpl.scatter(Y[:, 0], Y[:, 1],s = 20)
mpl.show()
