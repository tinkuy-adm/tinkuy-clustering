#from sklearn.cluster import OPTICS
#import pandas as pd

from data_io import get_tinkuy_coords_np, get_tinkuy_coords_list, get_tinkuy_coords_list_by_last_minutes
from outlier_detection import eliminate_outliers
from pyclustering.cluster import cluster_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster.kmedoids import kmedoids
from pyclustering.cluster.silhouette import silhouette_ksearch_type, silhouette_ksearch
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import sys
import numpy as np

def do_clustering(minutes,meters,minsam):
    # Read data
    points = np.array(get_tinkuy_coords_list_by_last_minutes(minutes))

    #get labels
    labels = eliminate_outliers(points,meters,minsam)

    n_clusters = max(labels) + 1
    medoid_points = []
    for i in range(n_clusters):
      center = np.median(points[labels == i], 0)
      medoid_points.append(center)

    return [list(i) for i in medoid_points]

def do_clustering_old(min_medoids, max_medoids,minutes):
    # Read data
    points = get_tinkuy_coords_list_by_last_minutes(minutes)

    #Filter outliers
    points = eliminate_outliers(points)

    # Get Optimal k
    max_score = 0
    amount = 2
    for n_clusters in range(min_medoids, max_medoids):
        clusterer = KMeans(n_clusters=n_clusters)
        preds = clusterer.fit_predict(points)
        centers = clusterer.cluster_centers_
        score = silhouette_score(points, preds)
        if(score > max_score):
            max_score = score
            amount = n_clusters

    print('Optimal k:', amount)

    # Compute clusters for optimal k
    initial_centers = kmeans_plusplus_initializer(points, amount).initialize()
    kmeans_instance = kmedoids(points, range(0, amount)).process()
    clusters = kmeans_instance.get_clusters()
    medoids = kmeans_instance.get_medoids()
    #visualizer = cluster_visualizer()
    #visualizer.append_clusters(clusters, points)
    # visualizer.show()

    # Retrieve medoid points
    print('Medoids')
    medoid_points = []
    for medoid in medoids:
        print('>', points[medoid])
        medoid_points.append(points[medoid])

    return medoid_points
