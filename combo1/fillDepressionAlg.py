import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def fillDepression(fillRainfallExcess, dem, flow_direction, pits, pairs, cellIndexes, pitID, pitCell, areaCellCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto, cellSize):
        import numpy as np
        #Prealllocate 
        fillDem = np.copy(dem)
        max_id = max(pitID)
        print(max(pitID))
        rainfall_excess = np.zeros([max_id,1]) 
        times = np.zeros([max_id,1])
        finalOrder = np.empty([max_id, 1])
        finalOrder[:] = np.NaN
        runoff = np.zeros([max_id, 1])
        #Initial Value
        #rainfall_excess[0] = 0
        #runoff[0] = sum(sum(pits<0))
        
        idx = 1
        
        firstpit = np.argmin(vca) #indexes of the first pit (scalar)
        secondpit = int(pits[cellOverflowInto[firstpit][0]][cellOverflowInto[firstpit][1]] - 1)#indexes of the second pit (scalar)
        
        pitCell = np.array(pitCell) #Unravel_index return tupel. Turn tuple to array
                      
        while (vca[firstpit] <= fillRainfallExcess/1000) and (idx <= max_id):
            print('line27',idx)
            finalOrder[idx -1] = firstpit
            #print('firstpit', firstpit, 'secondpit',secondpit, 'idx', idx)
            rainfall_excess[idx - 1] = vca[firstpit][:]
            #print('input',vca)
            #print('output',rainfall_excess)
            runoff[idx - 1] = sum(sum(pits<0))
            
            #re_ID first pit, raise/ fill first pit cells
            lessThanSpillover = [fillDem[cellIndexes[firstpit][:,0],cellIndexes[firstpit][:,1]] <= spilloverElevation[firstpit]] 
            lessThanSpillover = cellIndexes[firstpit][lessThanSpillover]
            fillDem[lessThanSpillover[:,0],lessThanSpillover[:,1]] = spilloverElevation[firstpit] 
            
            
            #Update Flow Direction
            flow_direction[pitCell[:,firstpit][0]][pitCell[:,firstpit][1]] = spilloverElevation[firstpit]
            pits[cellIndexes[firstpit][:,0],cellIndexes[firstpit][:,1]] = secondpit + 1
            
            #HANDLE PITS CONNECTED TO THE EDGE OF DEM
            if secondpit > 0:
                
                areaCount[secondpit] = areaCount[firstpit] + areaCount[secondpit]
                pairs[secondpit] = np.append(pairs[secondpit],pairs[firstpit],axis = 0)
                a = pairs[secondpit][:,2:4]
                keeper = pits[a[:,0],a[:,1]] != (secondpit + 1)
                pairs[secondpit] = pairs[secondpit][keeper]
                
                interior_rc = pairs[secondpit][:,0:2]
                exterior_rc = pairs[secondpit][:,2:4]
                interiorDEM = fillDem[interior_rc[:,0],interior_rc[:,1]]
                exteriorDEM = fillDem[exterior_rc[:,0],exterior_rc[:,1]]
                cmax = np.empty(np.shape(interiorDEM))
                for i in range(0,len(interiorDEM)):
                    cmax[i] = np.max([exteriorDEM[i],interiorDEM[i]])
        
                [val,cord] = [np.min(cmax), np.argmin(cmax)] 
                
                spilloverElevation[secondpit] = val
                cellOverflowInto[secondpit] = exterior_rc[cord]
                 
                #compute filled volume and initialize volume calculation (more below)
                filledVolume[secondpit] = volume[firstpit] + filledVolume[secondpit];
                volume[secondpit] = filledVolume[secondpit];
                cellIndexes[secondpit] = np.append(cellIndexes[secondpit],cellIndexes[firstpit],axis = 0)
                
                lessThans = [fillDem[cellIndexes[secondpit][:,0],cellIndexes[secondpit][:,1]] <= spilloverElevation[secondpit]];
                lessThans = cellIndexes[secondpit][lessThans]
                
                tempSpill = fillDem[lessThans[:,0],lessThans[:,1]]
                volume[secondpit] = volume[secondpit] + sum((spilloverElevation[secondpit] - tempSpill)*cellSize*cellSize);
                lessThans = [];

                vca[secondpit] = volume[secondpit]/((cellSize*cellSize)*areaCount[secondpit]);
                if vca[secondpit] < 0:
                    vca[secondpit] = np.Inf;
                    
            vca[firstpit] = np.NAN;
            if np.nansum(vca) == 0:
                print('line83',idx - 1)
                break
                
            cellIndexes[firstpit] = [];
            pairs[firstpit] = [];
        
            idx += 1
            firstpit = np.nanargmin(vca) #indexes of the first pit (scalar)
            secondpit = int(pits[cellOverflowInto[firstpit][0]][cellOverflowInto[firstpit][1]] - 1)#indexes of the second pit (scalar)
            print('cond1', vca[firstpit])
            print('cond2', fillRainfallExcess/1000 and (idx <= max_id) )

        return dem, pits, flow_direction, rainfall_excess, runoff, fillDem
        
fileName = 'Feldun.tif'
from dem import elevationfile
dem,cellSize = elevationfile(fileName)
#dem = np.array(dem[230:241][:,540:551])

from flow_dir import flow_direction
flow_direction = flow_direction(dem)
test_flow_direction = flow_direction.astype(float)

from d8FlowDirectionParents import d8FlowDirectionParents
flow_direction_parent = d8FlowDirectionParents(dem)

from getDepression import getDepression
pits, pairs, cellIndexes, pitID, pitCell, areaCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto = getDepression(dem, flow_direction, flow_direction_parent,cellSize)

fillRainfallExcess = 100000

dem, fillPits, fillFlow_direction, fillRainfall_excess, fillRunoff, fillDem = fillDepression(fillRainfallExcess, dem, flow_direction, pits, pairs, cellIndexes, pitID, pitCell, areaCount, spilloverElevation, vca, volume, filledVolume, cellOverflowInto, cellSize)

fig, ax =plt.subplots(1,2)

sns.heatmap(dem, ax=ax[0])
sns.heatmap(fillDem, ax=ax[1])

plt.show()
