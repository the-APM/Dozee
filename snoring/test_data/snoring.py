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
    second_derivative = [0]
    for i in range(len(intensity)-1):
        if i is not 0:
            second_derivative.append(abs(intensity[i+1]+intensity[i-1]-2*intensity[i]))
    second_derivative.append(0)
    data['y'] = second_derivative[:]
    return data

    
def sampled(data):
    l = int(len(data['y'])/100)
    temp = [0]*l
    for i in range(l-1):
        temp[i] = np.mean(data['y'][i*100:(i+1)*100])
    temp = pd.DataFrame(temp)
    temp.columns = ['y']
    temp['n'] = temp['y'][:]
    return temp

def classify(data):
    sort_temp = list(data['y'])
    sort_temp.sort()
    threshold_cutoff = np.median(sort_temp)
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
        if data['y'][i] != 0:
            temp['n'][(i-1)*100:(i)*100] = 0
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
    original_signal = list(data['y'][:])
    data = preprocess(data)
    data = sampled(data)
    data = classify(data)
    data = postprocess(data, original_signal)
    plot_data(data)
    del data
