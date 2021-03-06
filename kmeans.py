import numpy as np
import pylab as pl
import math
from sklearn.metrics import confusion_matrix, accuracy_score
#Regression program for k-means and fuzzy c-means
#by spencer Duncan

clusters = 4
rounds = 10

def readdata(filename):
    temparray = []
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        line = line.split('  ')
        temparray.append(line)
    data = np.asarray(temparray, float)
    return data

#update clusters
def e(w, data, centroids):
    for i in range(data.shape[0]):
        norms = np.linalg.norm(centroids-data[i], axis=1)
        w[i] = np.argmin(norms, axis=0)
    return

#calc new centroids
def m(w, data, centroids):
    global clusters
    clusterRange = clusters
    for i in range(clusterRange):
        pred = w[:] == i
        cluster = data[pred]
        if(cluster.shape[0] == 0):
            np.delete(centroids, i)
            clusters = clusters-1
        else:
            centroids[i] = np.mean(cluster, axis=0)
    return

def display(w, data, centroids):
    colors = w/clusters
    pl.scatter(data[:,0], data[:,1],c=colors)
    pl.scatter(centroids[:,0], centroids[:,1], c='r')
    pl.show()

def calcError(w, data, centroids):
    sum = 0
    for i in range(clusters):
        pred = w[:] == i
        cluster = data[pred]
        diff = np.linalg.norm(cluster-centroids[i], axis=1)
        diff = np.square(diff)
        diff = np.sum(diff)
        sum += diff
    return sum

def regress(data, absCord):
    datasize = data.shape[0]
    centroids = np.random.uniform(low=-absCord, high=absCord, size=(clusters,2))
    w = np.random.randint(clusters,size=datasize)
    pError = 0
    error = 0
    deltError = 100
    while(deltError > 1):
        m(w, data, centroids)
        e(w, data, centroids)
        error = calcError(w, data, centroids)
        deltError = abs(pError-error)
        pError = error
    display(w, data, centroids)
    return w, centroids, error

def main():
    filename = "cluster_dataset.txt"
    data = readdata(filename)
    absCord = max(abs(np.min(data[:,0])),abs(np.max(data[:,0])),abs(np.min(data[:,1])),abs(np.max(data[:,1])))
    bestLabels = 0
    bestCentroids = 0
    bestError = 50000
    for i in range(rounds):
        labels, centroids, error = regress(data,absCord)
        if error < bestError:
            bestLabels = labels
            bestCentroids = centroids
            bestError = error
    print("final")
    display(bestLabels, data, bestCentroids)
    
main()