import boto3
import os
import math
import numpy as np
from data_io import get_tinkuy_cluster_list

#TODO
#Obtener medioides actuales de la BD
#Función para asignar un punto

#se recibe un punto p y la lista de centroides o mediodes
#ESTA ASIGNACIÓN SUPONE QUE SE ESTÁ USANDO K-MEANS
#Si se usa otro método, esta función fallará terriblemente
#porque simplemente se está buscando el centroide más cercano
def assign_point_k_means(p,cs):
    assert len(cs) > 0, "lista de centroides vacia"
    best_c = cs[0]
    closest_distance = euc_dis(p,best_c)
    for c in cs[1:]:
        dist = euc_dis(p,c)
        if (dist  < closest_distance):
            best_c = c
            closest_distance = dist
    return best_c, closest_distance

#Distancia euclideana entre dos listas
#(chicos, deberíamos estar guardando los puntos como numpys)
def euc_dis(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def call_assign_point_k_means(p):
    cs = get_tinkuy_cluster_list()
    return assign_point_k_means(p,cs)
