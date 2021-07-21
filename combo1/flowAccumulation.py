import numpy as np 
def flowAccumulation(flow_direction):
    #ii = []
    #for i in range(0,np.shape(flow_direction)[0]):
     #   for j in range(0,np.shape(flow_direction)[1]):
     #       if ~np.isnan(flow_direction[i][j]) and flow_direction[i][j] > 0:
      #          ii.append(flow_direction[i][j])
    jj = np.array([jj for (jj, val) in enumerate(np.ravel(flow_direction, order = 'F')) if (val > 0)])
    ii = np.array([val for (jj, val) in enumerate(np.ravel(flow_direction, order = 'F')) if (val > 0)])
    
    flow_direction_parent = np.empty(np.shape(flow_direction),dtype = object)
    for i in np.ndindex(flow_direction_parent.shape): flow_direction_parent[i] = []

    #for i in range(0,len(ii)):
        #flow_direction_parent[ii[i]] = [flow_direction_parent[ii[i]],jj[i]]
    flow_accumulation = np.empty((np.shape(flow_direction)))
    flow_accumulation[:] = np.NaN
    flow_accumulation[~np.isnan(flow_direction)] = 0
    #for i in range(0,len(ii)):
        #if flow_accumulation[ii[i]] == 0:
            #parentSum = recursionThree[ii[i]]
    

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
print(flowAccumulation(flow_direction))