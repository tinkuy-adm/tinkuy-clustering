from sklearn.cluster import DBSCAN
import numpy as np

#CONSTANTES
#METERS = 80
#MIN_SAMPLES = 10

#Se recibe una lista de listas ([longitud,latitud])
#Se devuelven los labels de los puntos (los que tengan -1 son outliers)
def eliminate_outliers(points,meters,minsam):
    array = np.array(points)
    lat_distance = (meters/1000)/111.32
    clustering = DBSCAN(eps=lat_distance, min_samples=minsam).fit(array)
    return clustering.labels_
