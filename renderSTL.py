### Written by Tiago Sarmento - December 2020
# Combines separate stL files in positions defined by a csv file.
#
# Originally designed to take data from a solid edge assembly.
# csv file is populated using occurrence properties in solid edge. All the parts in a solid edge may be saved to STL
#
# Outputs a new STL file to be used as a preview of the final 3D positionings which will be imported to IBSIMU
# in the accompanying makeIBSIMU.py script


import numpy as np
from stl import mesh
import pandas as pd
import math

prefix = 'exampleAssembly/'
exportedFile = 'positioning.csv'

data = []
df = pd.read_csv(prefix + exportedFile)
for index, part in df.iterrows():

   # get transformation information from data frame
   X,Y,Z = float(part['X'].split(' ')[0]),float(part['Y'].split(' ')[0]),float(part['Z'].split(' ')[0])
   Xrot, Yrot, Zrot = float(part['Xdeg'].split(' ')[0]), float(part['Ydeg'].split(' ')[0]), float(part['Zdeg'].split(' ')[0])
   partName = part['partnames'].split('.')[0]
   #print(partName)
   # get mesh from stl file
   part_mesh = mesh.Mesh.from_file(prefix + partName + '.stl')

   # rotate in the correct order - note rotation in stl package is defined to be in the opposite direction to solid edge
   part_mesh.rotate([1,0,0], -math.radians(Xrot))
   part_mesh.rotate([0,1,0], -math.radians(Yrot))
   part_mesh.rotate([0,0,1], -math.radians(Zrot))
   # translate mesh
   part_mesh.x += X
   part_mesh.y += Y
   part_mesh.z += Z
   # put this part's mesh data in a list with other parts
   data = data + [part_mesh.data]

# combine all the parts
combined_parts = mesh.Mesh(np.concatenate(data))
# print boundaries of final combined assembly, to input in makeIBSIMU.py
xmin,xmax,ymin,ymax = combined_parts.x.min(),combined_parts.x.max(),combined_parts.y.min(),combined_parts.y.max()
zmin,zmax = combined_parts.z.min(),combined_parts.z.max()
print('xmin = ' + str(xmin) + ', xmax = ' + str(xmax))
print('ymin = ' + str(ymin) + ', ymax = ' + str(ymax))
print('zmin = ' + str(zmin) + ', zmax = ' + str(zmax))
limits = (xmin,xmax,ymin,ymax,zmin,zmax)
limits = [0.001*n for n in limits] ## scale limits to mm
print('limits in metres, to use in makeIBSIMU:')
print(limits)
# save as a single file to view relative positioning
combined_parts.save(prefix + 'combinedObject.stl') # this STL file will contain all the parts properly positioned
