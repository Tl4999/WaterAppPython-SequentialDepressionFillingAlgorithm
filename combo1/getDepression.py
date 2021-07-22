import numpy as np
def getDepression(dem, flow_direction, flow_direction_parent, cellSize):
   #Define variable
    pits = np.array(np.empty((np.shape(dem)[0],np.shape(dem)[1])))
    pits[:]=np.NaN
    pit_count = np.nansum(flow_direction == -1)
    edgepit_count = np.nansum(flow_direction == -2)
    pitID = np.int32(np.array(range(1,pit_count + 1), dtype = int)) # pit cellID
    #pit bottom cell index
    #pitCell = [pitCell for (pitCell, val) in enumerate(np.ravel(flow_direction, order = 'F')) if (val == -1)]
    pitCell = np.where(flow_direction == -1)
    edgePitId =np.int32(np.flip(np.array(range(-edgepit_count,0), dtype = int)))
    edgePitCell = np.where(flow_direction == -2)
    areaCount = np.zeros((pit_count,1),dtype = int) #integer number of cell
    spilloverElevation = np.zeros((pit_count,1),dtype = float)#meter
    vca = np.zeros((pit_count,1),dtype = float)#volume to contributing area ratio (hours)
    volume = np.zeros((pit_count,1),dtype = float)#cubic meters
    filledVolume = np.zeros((pit_count,1),dtype = float)#cubic meters
    cellOverflowInto = np.int32(np.zeros((pit_count,2),dtype = float))#cell index of overflow location
    
    #Pits must be identified in the pit matrix in order to return the 
    #correct pit ID that each pit flows into (if not, many of these pits will 
    #flow into yet unidentifed pits that have ID 0)
    
    #Fill out the pit ID image/matrix
    pits[~np.isnan(dem)] = 0 #if pits' element == NaN change the cell to 0 
    pits[pitCell] = pitID
    pits[edgePitCell] = edgePitId
    
    cellIndexes = [ [] for _ in range(pit_count)] #create a list within an list

    for p in range(0,np.shape(pitCell)[1]):
        pID = p + 1
        j = 0
        i = 0
        chunk = 50
        cellIndexes[p] = np.empty((chunk,2), dtype = object) 
        cellIndexes[p][0][0] = pitCell[0][p]
        cellIndexes[p][0][1] = pitCell[1][p]
        
        
        while i <= j:
            parent = flow_direction_parent[cellIndexes[p][i][0]][cellIndexes[p][i][1]]
            if len(parent) != 0:
                uparent = np.unravel_index(parent,np.shape(dem))
                pits[uparent] = pID 
                k = j + np.size(parent)
                #print('kbefore',k,'jbefore',j,'chunkbefore',chunk-1)
                if k > (np.shape(cellIndexes[p])[0]-1):
                    cellIndexes[p] = np.append(cellIndexes[p],np.empty((chunk,2),dtype = object),axis =0)  
                cellIndexes[p][j+1:k+1] = np.swapaxes(uparent,0,1)
                j = k  
            i = i + 1
        
        #print('sizebefore',np.shape(cellIndexes[p]))
        cellIndexes[p] = np.delete(cellIndexes[p],range(j+1,np.shape(cellIndexes[p])[0]),axis = 0) #Delete Empty or NaN array 
        #print('cellIndexes',cellIndexes[p])
        #print('length', np.shape(cellIndexes[p])[0], 'j+1',j+1, 'size', np.shape(cellIndexes[p]))
        cellIndexes[p] = cellIndexes[p].astype(int)
        areaCount[p] = j + 1
    
    
    #EDGE PITCELL
    for p in range(0,np.shape(edgePitCell)[1]):
        edgeID = edgePitId[p]
        j = 0
        i = 0
        chunk = 50
        edgeIndexes = np.empty((chunk,2), dtype = object) 
        
        edgeIndexes[0][0] = edgePitCell[0][p]
        edgeIndexes[0][1] = edgePitCell[1][p]
                
        while i <= j:
            parent = flow_direction_parent[edgeIndexes[i][0]][edgeIndexes[i][1]]
            if len(parent) != 0:
                uparent = np.unravel_index(parent,np.shape(dem))
                pits[uparent] = edgeID 
                k = j + np.size(parent)
                if k > (np.shape(edgeIndexes)[0]-1):
                    edgeIndexes = np.append(edgeIndexes,np.empty((chunk,2),dtype= object), axis = 0)
                edgeIndexes[j+1:k+1] = np.swapaxes(uparent,0,1)
                j = k  
            i = i + 1   
    
    indexes = indexes_list = list(range(0,np.size(flow_direction)))
    indexes = np.reshape(indexes_list,np.shape(flow_direction))
    pairs = [ [] for _ in range(pit_count)] #create a list within an list
    [numrows, numcols] = np.shape(dem)
    for p in range(0,np.size(cellIndexes)):
        pairs[p] = np.empty((np.shape(cellIndexes[p])[0]*8,4), dtype = int)
        l = 0
        for i in range(0,np.shape(cellIndexes[p])[0]): #Walk Through Indices To Check
            [r, c] = [cellIndexes[p][i][0],cellIndexes[p][i][1]]
           # print('cellIndexes[p][i]',cellIndexes[p][i])
           # print('Loop', i,'r&c',[r,c])
            for x in range(-1,2):
                for y in range(-1,2):
                    if x == 0 and y == 0:
                        continue #skip the center cell
                    if (r+y) >= (numrows-1) or (r+y)<0 or (c+x) >= (numcols-1) or (c+x)< 0:
                        continue #skip neighbors outside of the dem range
                    if np.isnan(dem[r+y][c+x]):
                        continue
                    if pits[r+y][c+x] != pits[r][c]:
                        pairs[p][l] = [r,c,r+y,c+x]
                        l = l + 1
        pairs[p] = np.delete(pairs[p],range(l,np.shape(pairs[p])[0]),axis = 0)
        
        interior_rc =pairs[p][:,0:2]
        exterior_rc = pairs[p][:,2:4]
        #print('interior_rc',interior_rc,'exterior_rc',exterior_rc)
        interiorDEM = dem[interior_rc[:,0],interior_rc[:,1]]
        exteriorDEM = dem[exterior_rc[:,0],exterior_rc[:,1]]
        #print('exteriorDEM',exteriorDEM)
        #print('interiorDEM',interiorDEM)
        
        cmax = np.empty(np.shape(interiorDEM))
        for i in range(0,len(interiorDEM)):
            cmax[i] = np.max([exteriorDEM[i],interiorDEM[i]])
        #print('MAX',cmax)
        [val,cord] = [np.min(cmax), np.argmin(cmax)] 
        #print([val,cord])
        spilloverElevation[p] = val
        cellOverflowInto[p] = exterior_rc[cord]
        
        #print(dem[cellIndexes[p].astype(int)])
        lessThans = [dem[cellIndexes[p][:,0],cellIndexes[p][:,1]] <= spilloverElevation[p]] 
        lessThans = cellIndexes[p][lessThans]
        #print('lessThans',lessThans)
        #print('DEM',dem[lessThans[:,0],lessThans[:,1]])
        volume[p] = np.sum((spilloverElevation[p] - dem[lessThans[:,0],lessThans[:,1]])*cellSize*cellSize)
        #print('loop', p, 'VOLUME',volume)
        #print('pits',pits)
        #print('Spill',spilloverElevation)
        
        filledVolume[p] = 0
        vca[p] = volume[p]/((cellSize*cellSize)*areaCount[p])
        #print(vca[p])
        
        if vca[p] < 0:
            vca[p] = np.infty
        #print(pits)
    return pits, pairs, cellIndexes, pitID, pitCell, areaCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto
        
        

fileName = 'CedarUpper_30m.tif'
from dem import elevationfile
dem,cellSize = elevationfile(fileName)
dem = np.array(dem[230:241][:,540:551])

from flow_dir import flow_direction
flow_direction = flow_direction(dem)
test_flow_direction = flow_direction.astype(float)

from d8FlowDirectionParents import d8FlowDirectionParents
flow_direction_parent = d8FlowDirectionParents(dem)

getDepression(dem, flow_direction, flow_direction_parent, cellSize)
