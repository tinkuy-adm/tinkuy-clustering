import boto3
import pandas as pd
import os
import numpy as np
import time
import math

from boto3.dynamodb.conditions import Attr

REFRESH_INTERVAL = 900 #seconds

def get_tinkuy_coords_df():
    dynamodb = boto3.client('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    response = dynamodb.scan(TableName='tinkuy-coords')
    df = pd.DataFrame.from_dict(response['Items'])
    return df

def get_tinkuy_coords_np():
    dynamodb = boto3.client('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    response = dynamodb.scan(TableName='tinkuy-coords')
    
    points = []
    i = 1
    for item in response['Items']:
        #print(item)
        point = [float(item['latitud']['S']),float(item['longitud']['S'])]
        print(point)
        i += 1
        points.append(points)
        
    return np.array(points)

def get_tinkuy_coords_list_by_last_minutes(minutes=15):
    dynamodb = boto3.resource('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    table = dynamodb.Table('tinkuy-coords-qas')
    ts = math.floor(time.time())
    ts_minus15 = int(ts - minutes*60)
    response = table.scan(Select='ALL_ATTRIBUTES', FilterExpression=Attr('tstamp').gte(ts_minus15))
    
    points = []
    i = 1
    for item in response['Items']:
        try:
            point = [float(item['latitud']),float(item['longitud'])]
            i += 1
            points.append(point)
        except:
            print("Point:", item, "ignored")
    i -= 1
    print("Number of retrieved points:",i)

    return points

def clean_tinkuy_coords_before_last_minutes(minutes=15):
    dynamodb = boto3.resource('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    table = dynamodb.Table('tinkuy-coords-qas')
    ts = math.floor(time.time())
    ts_minus15 = int(ts - minutes*60)

    response = table.scan(Select='ALL_ATTRIBUTES', FilterExpression=Attr('tstamp').lt(ts_minus15))
    
    i = 1
    for item in response['Items']:
        try:
            table.delete_item(
                Key={
                    'usr_tlg': item['usr_tlg']['S']
                }
            )
            i += 1
        except:
            print("Point:", item, "ignored")
    i -= 1
    print("Number of cleaned points:",i)

    return points


def get_tinkuy_coords_list():
    dynamodb = boto3.client('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    response = dynamodb.scan(TableName='tinkuy-coords')
    
    points = []
    i = 1
    for item in response['Items']:
        try:
            point = [float(item['latitud']['S']),float(item['longitud']['S'])]
            #print(point)
            i += 1
            points.append(point)
        except:
            print("Point:", item, "ignored")
    i -= 1
    print("Number of retrieved points:",i)
        
    return points

def get_tinkuy_cluster_list():
    dynamodb = boto3.client('dynamodb',\
                      aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],\
                      aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'],\
                      region_name = os.environ['AWS_DEFAULT_REGION'])
    response = dynamodb.scan(TableName='tinkuy-clusters')
    
    str_points = [obj['SS'] for obj in response['Items'][0]['points']['L']]
    float_cluster = [list(map(float,o)) for o in str_points]
    return float_cluster
