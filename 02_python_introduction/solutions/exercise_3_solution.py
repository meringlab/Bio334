#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Question 3

import numpy as np

def create_initial_centroids(data, k):
    np.random.seed(5)
    centroids = np.zeros((k,2))
    centroids[:,0] = np.random.uniform(np.min(data[:,0]), np.max(data[:,0]), size = k)
    centroids[:,1] = np.random.uniform(np.min(data[:,1]), np.max(data[:,1]), size = k)
    return centroids

def compute_distances_to_centroids(data, centroids):
    distanceMatrix = np.zeros((len(data), len(centroids)), dtype=float)
    
    for centroidIndex, centroid in enumerate(centroids):
        distanceMatrix[:,centroidIndex] = ((data[:,0] - centroid[0])**2 + (data[:,1]- centroid[1])**2)**0.5
    return distanceMatrix

def assign_cluster_labels(distanceMatrix, k):
    clusterLabels = np.zeros((len(distanceMatrix)), dtype = int) 
    
    for centroidIndex in range(k):
        clusterLabels[distanceMatrix[:,centroidIndex] == np.min(distanceMatrix, axis=1)]=centroidIndex
    return clusterLabels
    
def calculate_new_centroids(data, clusterLabels, k):
    centroids = np.zeros((k,2), dtype=float)
    for i in range(k):
        centroids[i,0] = np.mean(data[clusterLabels == i,0])
        centroids[i,1] = np.mean(data[clusterLabels == i,1])
    return centroids

def compute_kmeans_clustering(data, startingCentroids, k, iterations):
    centroids = startingCentroids
    for i in range(iterations):
        distanceMatrix = compute_distances_to_centroids(data, centroids)
        clusterLabels = assign_cluster_labels(distanceMatrix, k)
        centroids = calculate_new_centroids(data, clusterLabels, k)
    return clusterLabels, centroids



## read and parse data
f = open('../exercises/data.csv')
lines = f.readlines()
f.close()

data = np.zeros((len(lines),2), dtype=float)
for i, line in enumerate(lines):
    data[i] = line.strip().split(',')

## task k-means clustering for k=3 and 15 iterations:
k = 3
n_iterations = 15
initialCentroids = create_initial_centroids(data, k)
clusterLabels, newCentroids = compute_kmeans_clustering(data, initialCentroids, k, n_iterations)
for centroid in newCentroids:
    print("{:5.2f} {:5.2f}".format(centroid[0],centroid[1]))


