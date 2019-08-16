import numpy as np
import pandas as pd
import plotly
from plotly.graph_objs import Scatter

def read_csv(file_name):
    data = pd.read_csv(file_name)
    data.columns = ['y']
    return data

def preprocess(data):
    intensity = data['y']
    data['n'] = data['y'][:]
    intensity_mean = np.mean(intensity)
    i_sq = pow(intensity-intensity_mean,2)
    data['y'] = i_sq
    return data

    
def sampled(data):
    l = int(len(data['y'])/100)
    temp = [0]*l
    for i in range(l):
        if i is 0:
            continue
        temp[i] = max(data['y'][(i-1)*100:i*100])
    temp = pd.DataFrame(temp)
    temp.columns = ['y']
    return temp

def max_curvature(sorted_temp):
    second_derivative = []
    for i in range(len(sorted_temp)-1):
        if i is not 0:
            second_derivative.append(sorted_temp[i+1]+sorted_temp[i-1]-2*sorted_temp[i])
    return second_derivative.index(max(second_derivative))

def classify(data):
    data['n'] = data['y'][:]
    sort_temp = list(data['n'])
    sort_temp.sort()
    threshold_cutoff = max_curvature(sort_temp)
    for i in range(len(data['y'])):
        if data['y'][i] < 2*threshold_cutoff:
            data['n'][i] = 0
        else:
            data['y'][i] = 0
    return data

def postprocess(data, signal):
    temp = pd.DataFrame(signal)
    temp.columns = ['y']
    temp['n'] = temp['y'][:]
    for i in range(len(data['y'])):
        if data['y'][i] == 0:
            temp['y'][i*100:(i+1)*100] = 0
        else:
            temp['n'][i*100:(i+1)*100] = 0
    return temp

def plot_data(data):
    data_intensity = list(data['y'])
    data_int = list(data['n'])
    plotly.offline.plot({
        "data":[Scatter(
            x=list(range(len(data_intensity))),
            y=data_intensity),
                Scatter(
                    x=list(range(len(data_intensity))),
                    y=data_int)]})

file_names = ['test1.csv','test2.csv','test3.csv','test4.csv','test5.csv']
for file in file_names:
    data = read_csv(file)
    original_signal = data['y'][:]
    data = preprocess(data)
    data = sampled(data)
    data = classify(data)
    data = postprocess(data, original_signal)
    plot_data(data)
    del data
