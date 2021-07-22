import numpy as np
import matplotlib.pyplot as plt
def flow_direction(dem):
    import math 
    import numpy as np
    import seaborn as sns
    #Generate the D8 flow direction of water across the DEM surface. 
    #Input:  dem - Matrix of elevation. Has dimensions MxN 
    #Output: flow_direction - for each cell, the flow_direcion matric specifies 
    #the row, column indices of the cell to which water flow. If the cell is a 
    #local minima of the 3x3 neighborhood, it will be assigned row and column values of -1. Has dimensions MxNx2.
    #flow_direction_parents - Boolean matrix specifying whether each of the neighboring 
    #cells flow into current cell. Has size MxNn3x3. For every cell(m,n) a 3x3 matrix of 
    #neighbors is assigned boolean values based on whether or not the neighboring cell
    #flow into the current cell. 
    #this function evaluates the DEM and determines the D8 flow directions for each cell. 
    #instead of using the powers of two for each of the eight neighbors or simply 1-8, flow directions are enclosed as the index of the cell to which flow is directed. 
    
    #Create a matrix 3x3
    weights = np.array([[math.sqrt(2),1, math.sqrt(2)], [1,np.NaN,1], [ math.sqrt(2),1,math.sqrt(2)]])
    
    #Create a matrix of dem size with Not a Number value.
    flow_direction = np.empty((np.shape(dem)[0],np.shape(dem)[1]))
    flow_direction[:]= np.NaN

    #Mark the flow direction w indexes.    
    indexes_list = list(range(0,np.size(flow_direction)))
    indexes = np.reshape(indexes_list,np.shape(flow_direction))
    [numrows, numcols] = np.shape(dem)
    #fprintf('\nProcessing flow dir)
    

    for i in range(0,np.size(flow_direction)):
        [r,c] = divmod(i,np.shape(dem)[1])
        if np.isnan(dem[r][c]):
            continue
        maxr = r + 1
        minr = r - 1
        maxc = c + 1
        minc = c - 1
        wminr = 0
        wmaxr = 2
        wminc = 0
        wmaxc = 2
        
        #Border cell
        if r == numrows-1:
            maxr = numrows-1 
            wmaxr = 1
            flow_direction[r][c]= -2
            continue
        elif r == 0:
            minr = 0
            wminr = 1
            flow_direction[r][c]= -2
            continue
        if c == numcols-1:
            maxc = numcols-1
            wmaxc = 1
            flow_direction[r][c]= -2
            continue
        elif c == 0:
            minc = 0
            wminc = 1
            flow_direction[r][c]= -2
            continue
                
        a = np.ones((maxr-minr+1, maxc-minc+1), dtype = float)*dem[r][c]
        b = dem[minr:maxr+1,minc:maxc+1]
        dwd = (a-b)/weights[wminr:wmaxr+1,wminc:wmaxc+1]
        [rol, col] = np.unravel_index(np.nanargmax(dwd),dwd.shape)
        dwdMax = dwd[rol,col]
        
        if dwdMax <= 0:
           #print('maxr',maxr,'minr',minr,'minc',minc,'minr', minr )
           #print('dwdMax',dwdMax,'dwd',dwd)
           if r == maxr or r== minr or c == minc or c == maxc:
               flow_direction[r][c] = -2
               continue
           else:
                flow_direction[r][c] = -1
                continue
    
        indices = indexes[minr:maxr+1,minc:maxc+1]
        #print(indices)
        
        flow_direction[r][c]= indices[rol][col]
    #sns.heatmap(flow_direction, annot = True, cmap='YlGnBu')
    #sns.heatmap(flow_direction, cmap='YlGnBu')

    return flow_direction

fileName = 'CedarUpper_30m.tif'
from dem import elevationfile
dem,cellSize = elevationfile(fileName)
dem = np.array(dem[230:241][:,540:551])
var_flow_direction = flow_direction(dem)
