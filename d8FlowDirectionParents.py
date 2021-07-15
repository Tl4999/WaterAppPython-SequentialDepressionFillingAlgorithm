import numpy as np
import math as math
import pandas as pd

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

from flow_dir import flow_direction
flow_dir_var = np.array(flow_direction(dem))
print(flow_dir_var)

#[frol,fcol] = np.shape(ii)
#FlowDirectionParent = []
#for i in range(0,frol):
 #   for j in range(0,fcol):
  #     FlowDirectionParent.append(ii[i][j])

FlowDirectionParent = np.empty(np.shape(flow_dir_var), dtype = object)
for i in np.ndindex(FlowDirectionParent.shape): FlowDirectionParent[i] = []

 

for i in range(0, np.shape(FlowDirectionParent)[0]):
    for j in range(0,np.shape(FlowDirectionParent)[1]):
         if np.isnan(flow_dir_var[i][j]) or (flow_dir_var[i][j] < 0) :
             continue 
         child = np.array(flow_dir_var[i][j], dtype = int)
         #print('child', child)
         [r, c] = np.unravel_index(child,np.shape(flow_dir_var))
         parent = np.ravel_multi_index([i,j], np.shape(flow_dir_var))
         #print('parent',parent)
         FlowDirectionParent[r][c].append(parent)
         #print('rol&col',r,c,'FLow',FlowDirectionParent)
#print('FINALFLOW PARENT',FlowDirectionParent)
#print('FINAL FLOW', flow_dir_var)
 

        #child = ii[i][j]
        #print('child',child)
        #parent = np.ravel_multi_index([i,j], np.shape(flow_dir_var)) #ind2sub in MatLab
        #print('parent',parent)
        #[r,c] = np.unravel_index(parent,np.shape(flow_dir_var))
        #print('rol & col',[r,c])
        #np.append(FlowDirectionParent, parent)
                                         
