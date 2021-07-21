import numpy as np
def fillDepression(fillRainfallExcess, dem, flow_direction, pits, pairs, cellIndexes, pitID, pitCell, areaCellCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto, cellSize):
        import numpy as np
        #Prealllocate 
        max_id = max(pitID)
        rainfall_excess = np.zeros([max_id,1]) 
        times = np.zeros([max_id,1])
        finalOrder = np.empty([max_id, 1])
        finalOrder[:] = np.NaN
        runoff = np.zeros([max_id, 1])
        #Initial Value
        rainfall_excess[0] = 0
        runoff[0] = sum(sum(pits<0))
        
        idx = 1
        
        firstpit = np.argmin(vca) #indexes of the first pit
        secondpits = pits[cellOverflowInto[firstpit][0]][cellOverflowInto[firstpit][1]]
        
        #while vca[firstpit] <= (fillRainfallExcess/1000) and (idx <= max_id):
            #finalOrder[idx -1] = firstpit
            #rainfall_excess[idx] = vca[firstpit][:]
            #runoff[idx] = sum(sum(pits<0))
            
            #lessThanSpillover = [dem[cellIndexes[firstpit][:,0],cellIndexes[firstpit][:,1]] <= spilloverElevation[firstpit]] 
            #lessThanSpillover = cellIndexes[firstpit][lessThanSpillover]
            #dem[lessThanSpillover[:,0],lessThanSpillover[:,1]] = secondpits
            #flow_direction[pitCell[firstpit]]
            
from getDepression import getDepression
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

flow_direction = np.array([[10., 10., 12.,  2., 13., 15.,  7., -2.,  7., 19.],
 [-2., 10., -1., 12., 25., 25., 17.,  7., 17., -2.],
 [10., 31., 32., 32., 25., -1., 25., 17., 17., 19.],
 [31., 32., -1., 32., 25., 25., 25., 27., 49., 49.],
 [50., 31., 32., 53., 53., 55., 56., 57., 49., -2.],
 [-2., 50., 53., -1., 53., -1., 55., 56., 57., 49.],
 [50., 51., 53., 53., 74., 55., 76., 76., 67., 78.],
 [80., 80., 62., 74., -1., 76., -1., 76., -1., 78.],
 [-2., 80., 81., 84., -1., 84., 76., 76., 78., 88.],
 [80., 81., 81., 84., 84., 84., 95., 87., 88., 88.]])

flow_direction_parent = np.array([[list([]), list([]), list([3]), list([]), list([]), list([]), list([]),
  list([6, 8, 17]), list([]), list([])],
 [list([0, 1, 11, 20]), list([]), list([2, 13]), list([4]), list([]),
  list([5]), list([]), list([16, 18, 27, 28]), list([]), list([9, 29])],
 [list([]), list([]), list([]), list([]), list([]),
  list([14, 15, 24, 26, 34, 35, 36]), list([]), list([37]), list([]),
  list([])],
 [list([]), list([21, 30, 41]), list([22, 23, 31, 33, 42]), list([]),
  list([]), list([]), list([]), list([]), list([]), list([])],
 [list([]), list([]), list([]), list([]), list([]), list([]), list([]), list([]),
  list([]), list([38, 39, 48, 59])],
 [list([40, 51, 60]), list([61]), list([]), list([43, 44, 52, 54, 62, 63]),
  list([]), list([45, 56, 65]), list([46, 57]), list([47, 58]), list([]),
  list([])],
 [list([]), list([]), list([72]), list([]), list([]), list([]), list([]),
  list([68]), list([]), list([])],
 [list([]), list([]), list([]), list([]), list([64, 73]), list([]),
  list([66, 67, 75, 77, 86, 87]), list([]), list([69, 79, 88]), list([])],
 [list([70, 71, 81, 90]), list([82, 91, 92]), list([]), list([]),
  list([83, 85, 93, 94, 95]), list([]), list([]), list([97]),
  list([89, 98, 99]), list([])],
 [list([]), list([]), list([]), list([]), list([]), list([96]), list([]),
  list([]), list([]), list([])]], dtype = object)

cellSize = 10
pits, pairs, cellIndexes, pitID, pitCell, areaCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto = getDepression(dem, flow_direction, flow_direction_parent, cellSize)

fillDepression(3000, dem, flow_direction, pits, pairs, cellIndexes, pitID, pitCell, areaCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto, cellSize)
