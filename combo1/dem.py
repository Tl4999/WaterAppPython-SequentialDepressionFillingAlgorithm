
def elevationfile(fileName):
    import rasterio
    import georasters as gr
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    file = gr.from_file(fileName)
    NDV, xsize, ysize, GeoT, Projection,  DataType= gr.get_geo_info(fileName)
    cellSize = GeoT[1]
    file = file.to_pandas()
    file = file.loc[:,['row','col','value']].to_numpy()
    dem = np.empty((ysize, xsize))
    dem[:] = np.NaN
    for i in range(0,np.shape(file)[0]):
        dem[int(file[i][0])][int(file[i][1])] = file[i][2]
    return dem,cellSize
      
dem = elevationfile('cedarUpper_30m.tif')
