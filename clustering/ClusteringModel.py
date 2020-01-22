import numpy as np
import pandas as pd
import math


MAX_CLUSTER_ITERATIONS = 50


def get_initial_centers(data, n):
    print(data)
    # indexes = random.sample(range(0, len(data.index)), n)
    # return data.reset_index().loc[indexes].reset_index(drop=True).drop('Date', axis=1)
    indexes = np.linspace(0.1,0.9, num = n)
    centers = pd.DataFrame()
    for i in range(0,n):
        center = data.quantile(q=indexes[i])
        center['Cluster'] = i
        centers = centers.append(center, ignore_index=True)
    return centers.set_index('Cluster', drop=True)



def mod(val):
    return math.fabs(val)


def get_empty_cluster_assignments(n):
    cluster_assignment = {}
    for i in range(0, n):
        cluster_assignment[i] = np.array([])
    return cluster_assignment


def get_empty_named_cluster_assignments(n):
    cluster_assignment = {}
    for i in range(0, n):
        cluster_assignment['cluster_'+str(i)] = np.array([])
    return cluster_assignment


def invert_data_point(data):
    return np.array([data["percent_d"], data["rsi"], mod(data["percent_r"])])


def reassign_cluster_center(data, clusters, cluster_centers):
    for cluster in clusters:
        cluster_data = data.loc[clusters[cluster]]
        cluster_centers.loc[cluster] = cluster_data.mean()


def find_cluster_convergence(old_clusters, new_clusters):
    convergence_reached = np.zeros(len(old_clusters), dtype=bool)
    for i in range(0, len(old_clusters)):
        difference = np.setdiff1d(old_clusters[i], new_clusters[i])
        if (float(len(difference)) <= 0.035 * len(old_clusters[i])):
            convergence_reached[i] = True
    print(convergence_reached)
    return np.all(convergence_reached)


def create_clusters(data, n):
    cluster_centers = get_initial_centers(data, n)
    old_clusters = clustering_iteration(data, cluster_centers, n)
    for i in range(0, MAX_CLUSTER_ITERATIONS):
        print('Iteration ' , i)
        reassign_cluster_center(data, old_clusters, cluster_centers)
        new_clusters = clustering_iteration(data, cluster_centers, n)
        if (i == (MAX_CLUSTER_ITERATIONS - 1)):
            return [new_clusters, cluster_centers]
        if (not find_cluster_convergence(old_clusters, new_clusters)):
            old_clusters = new_clusters
        else:
            return [new_clusters, cluster_centers]


def clustering_iteration(data, centers, n):
    cluster_assigment = get_empty_cluster_assignments(n)
    for index in data.index:
        distance_vector = np.full((n), np.inf)
        for i in range(0, len(centers)):
            center = centers.loc[i]
            data_point = data.loc[index]
            distance_vector[i] = np.linalg.norm(center - data_point)
        cluster_assigned = np.argmin(distance_vector)
        cluster_assigment[cluster_assigned] = np.append(cluster_assigment[cluster_assigned], index)
    return cluster_assigment



def assign_out_of_sample_clusters(data_point, centers):
    distance_vector = pd.Series(np.full((len(centers.index)), np.inf), index = centers.index)
    for cluster in centers.index:
        center = centers.loc[cluster]
        distance_vector.loc[cluster] = np.linalg.norm(center - data_point)
    print(distance_vector)
    return distance_vector.idxmin()