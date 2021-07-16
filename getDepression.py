import numpy as np

def getDepression(dem, flow_direction, flow_direction_parent, cellSize):
   #Define variable
    pits = np.array(np.empty((np.shape(dem)[0],np.shape(dem)[1])))
    pits[:]=np.NaN
    pit_count = np.nansum(flow_direction == -1)
    pitID = np.int32(np.array(range(1,pit_count + 1), dtype = int)) # pit cellID
    #pit bottom cell index
    #pitCell = [pitCell for (pitCell, val) in enumerate(np.ravel(flow_direction, order = 'F')) if (val == -1)]
    pitCell = np.where(flow_direction == -1)
    areaCount = np.zeros((pit_count,1),dtype = int) #integer number of cell
    spilloverElevation = np.zeros((pit_count,1),dtype = float)#meter
    vca = np.zeros((pit_count,1),dtype = float)#volume to contributing area ratio (hours)
    volume = np.zeros((pit_count,1),dtype = float)#cubic meters
    filledVolume = np.zeros((pit_count,1),dtype = float)#cubic meters
    cellOverflowInto = np.int32(np.zeros((pit_count,1),dtype = float))#cell index of overflow location
    
    #Pits must be identified in the pit matrix in order to return the 
    #correct pit ID that each pit flows into (if not, many of these pits will 
    #flow into yet unidentifed pits that have ID 0)
    
    #Fill out the pit ID image/matrix
    print('pit', pits,'type', type(pits),'shape',np.shape(pits))
    print('pitCell',pitCell,'type', type(pitCell),'shape',np.shape(pitCell))
    print('pitID', pitID,'type', type(pitID),'shape',np.shape(pitID))
    pits[~np.isnan(dem)] = 0
    pits[pitCell] = pitID
    cellIndexes = [ [] for _ in range(pit_count)] #create a list within an list
    #print(np.shape(pitCell)[1])
    for p in range(0,np.shape(pitCell)[1]):
        id = p +1
        j = 0
        i = 0
        chunk = 50
        cellIndexes[p] = np.empty((chunk,2), dtype = int) 
        
        cellIndexes[p][0][0] = pitCell[0][p]
        cellIndexes[p][0][1] = pitCell[1][p]
        
        while i <= j:
            print('first',cellIndexes[p][i][0])
            print('second',cellIndexes[p][i][1])
            parent = flow_direction_parent[cellIndexes[p][i][0]][cellIndexes[p][i][1]]
            uparent = np.unravel_index(parent,np.shape(dem) )
            pits[uparent] = 1
            k = j + np.size(parent)
            if k > (chunk-1):
                cellIndexes[p].append(np.empty((chunk,2), dtype = int))
                chunk += 50 
            print('j+1',j+1,'k+1',k+1,'uparent',uparent)
            print('cellIndexes',cellIndexes)
            cellIndexes[p][j+1:k+1] = np.swapaxes(uparent,0,1)
            j = k 
            i = i + 1
        #np.remove(cellIndexes[p][j+1]) Delete Empty or NaN array 
        #cellIndexes[0][5:np.size(cellIndexes[0])]
        #areaCellCount[p] = j
    print(pits)
                 

dem = np.array([[4, 7, 3, 7, 8, 8, 5, 2, 9, 8],
 [0, 8, 2, 4, 6, 4, 7, 3, 8, 5],
 [4, 5, 9, 9, 8, 3, 6, 4, 6, 6],
 [6, 1, 0, 5, 7, 7, 5, 8, 8, 7],
 [9, 9, 3, 5, 9, 7, 6, 9, 7, 2],
 [0, 2, 8, 0, 4, 0, 1, 2, 8, 7],
 [6, 9, 2, 9, 5, 5, 9, 1, 5, 9],
 [4, 3, 6, 9, 1, 3, 0, 8, 1, 5],
 [0, 1, 3, 7, 1, 9, 9, 4, 2, 8],
 [1, 4, 4, 6, 4, 4, 8, 9, 5, 9]])

flow_direction = np.array([[10., 10., 12., 12., 13., 15.,  7.,  7., 17., 19.],
 [10., 10., -1., 12., 25., 25.,  7.,  7., 7., 19.],
 [31., 10., 31., 32., 13., -1., 17., 17., 17., 19.],
 [31., 32., -1., 32., 25., 25., 25., 27., 49., 49.],
 [31., 32., 53., 32., 53., 56., 55., 56., 57., 49.],
 [50., 50., 53., -1., 53., -1., 55., 56., 67., 49.],
 [50., 50., 53., 74., 53., 76., 55., 76., 57., 78.],
 [81., 80., 81., 84., -1., 76., -1., 88., -1., 88.],
 [80., 80., 81., 74., -1., 76., 76., 76., 78., 78.],
 [80., 80., 81., 84., 84., 84., 87., 88., 88., 88.]])

flow_direction_parent = np.array([[list([]), list([]), list([]), list([]), list([]), list([]), list([]),
  list([6, 7, 16, 17, 18]), list([]), list([])],
 [list([0, 1, 10, 11, 21]), list([]), list([2, 3, 13]), list([4, 24]),
  list([]), list([5]), list([]), list([8, 26, 27, 28]), list([]),
  list([9, 19, 29])],
 [list([]), list([]), list([]), list([]), list([]), list([14, 15, 34, 35, 36]),
  list([]), list([37]), list([]), list([])],
 [list([]), list([20, 22, 30, 40]), list([23, 31, 33, 41, 43]), list([]),
  list([]), list([]), list([]), list([]), list([]), list([])],
 [list([]), list([]), list([]), list([]), list([]), list([]), list([]), list([]),
  list([]), list([38, 39, 49, 59])],
 [list([50, 51, 60, 61]), list([]), list([]), list([42, 44, 52, 54, 62, 64]),
  list([]), list([46, 56, 66]), list([45, 47, 57]), list([48, 68]), list([]),
  list([])],
 [list([]), list([]), list([]), list([]), list([]), list([]), list([]),
  list([58]), list([]), list([])],
 [list([]), list([]), list([]), list([]), list([63, 83]), list([]),
  list([65, 67, 75, 85, 86, 87]), list([]), list([69, 88, 89]), list([])],
 [list([71, 80, 81, 90, 91]), list([70, 72, 82, 92]), list([]), list([]),
  list([73, 93, 94, 95]), list([]), list([]), list([96]),
  list([77, 79, 97, 98, 99]), list([])],
 [list([]), list([]), list([]), list([]), list([]), list([]), list([]), list([]),
  list([]), list([])]], dtype = object)

cellSize = 10
getDepression(dem, flow_direction, flow_direction_parent, cellSize)