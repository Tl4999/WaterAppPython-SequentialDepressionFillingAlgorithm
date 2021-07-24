import numpy as np 
import matplotlib.pyplot as plt
def flowAccumulation(flow_direction, flow_direction_parent):
    
    flow_accumulation = np.empty((np.shape(flow_direction)))
    flow_accumulation[:] = np.NaN
    
    flow_accumulation[~np.isnan(flow_direction)] = 0
    
    def recurssive(r,c):
        flow_accumulation[r][c] = flow_accumulation[r][c] + 1  
        parents = flow_direction_parent[r][c]
        for parent in parents:
            [pr,pc] = np.unravel_index(parent,np.shape(flow_direction))
            #print(flow_accumulation[pr,pc])
            if flow_accumulation[pr,pc] == 0:
                parentSum = recurssive(pr,pc)
            else:
                parentSum = flow_accumulation[pr,pc]
            #print('r', r,'c',c)
            #print('parentSum',parentSum)
            #print('left', flow_accumulation[r][c] + parentSum)
            flow_accumulation[r][c] = flow_accumulation[r][c] + parentSum
        return flow_accumulation[r][c]
    
    for i in range(0, np.shape(flow_direction)[0]):
        for j in range(0, np.shape(flow_direction)[1]):
            if flow_accumulation[i][j] == 0:
                r = i 
                c = j
                flow_accumulation[r][c] = recurssive(r,c)
    return flow_accumulation
    
fileName = 'Feldun.tif'
from dem import elevationfile
dem,cellSize = elevationfile(fileName)

from flow_dir import flow_direction
flow_direction = flow_direction(dem)

from d8FlowDirectionParents import d8FlowDirectionParents
flow_direction_parent = d8FlowDirectionParents(dem)

output = flowAccumulation(flow_direction, flow_direction_parent)

