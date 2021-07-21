import numpy as np
import math as math
import pandas as pd
import matplotlib.pyplot as plt

def d8FlowDirectionParents(dem):
    from flow_dir import flow_direction
    flow_dir_var = np.array(flow_direction(dem))

    FlowDirectionParent = np.empty(np.shape(flow_dir_var), dtype = object)
    for i in np.ndindex(FlowDirectionParent.shape): FlowDirectionParent[i] = []

 

    for i in range(0, np.shape(FlowDirectionParent)[0]):
        for j in range(0,np.shape(FlowDirectionParent)[1]):
            if np.isnan(flow_dir_var[i][j]) or (flow_dir_var[i][j] < 0) :
                continue 
            child = np.array(flow_dir_var[i][j], dtype = int)
            [r, c] = np.unravel_index(child,np.shape(flow_dir_var))
            parent = np.ravel_multi_index([i,j], np.shape(flow_dir_var))
            FlowDirectionParent[r][c].append(parent)
            
    return FlowDirectionParent

fileName = 'CedarUpper_30m.tif'
from dem import elevationfile
dem,cellSize = elevationfile(fileName)
#dem = np.array(dem[230:241][:,540:551])
d8FlowDirectionParents(dem)                                