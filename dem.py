import rasterio
import georasters as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#from rasterio.plot import show
#demfile = r'CedarUpper_30m.tif'
#img = rasterio.open(demfile)
#show(img)

file = gr.from_file('CedarUpper_30m.tif')
print(gr.get_geo_info('CedarUpper_30m.tif'))
NDV, xsize, ysize, GeoT, Projection,  DataType= gr.get_geo_info('CedarUpper_30m.tif')
print('xsize',xsize, 'ysize', ysize)
file = file.to_pandas()
file = file.loc[:,['row','col','value']].to_numpy()
print('file',file)
dem = np.empty((ysize, xsize), dtype = float)

for i in range(0,len(file)):
    dem[int(file[i][0])][int(file[i][1])] = file[i][2]
plt.imshow(dem)
plt.show()

