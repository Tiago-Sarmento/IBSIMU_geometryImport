### Written by Tiago Sarmento December 2020
# Outputs an IBSIMU script filled with the required commands to import and position stl files defined in the
# accompanying csv file.
# The CSV file can be produced from a solid edge assembly using 'occurrence properties'.
# Functions defining the strings to be written are defined in translateToIBSIMU.py


import pandas as pd
import translateToIBSIMU as ib
pi = 3.14159265359

prefix = 'parts/pullerElectrodes/'
positionFile = 'positioning.csv'
writeFile = 'IBSIMU_GeometryImport.cpp'
nDimensions = 3

df = pd.read_csv(prefix + positionFile) # read csv into a database

minMaxArray = [-0.075,0.093,-0.01,0.01,-0.08,0.09] # run renderSTL with your settings to get these values [xmin,xmax,ymin,ymax,zmin,zmax]
meshSize = 0.001
with open(prefix + writeFile, 'w') as f:
    preambString = ib.startPreamble(minMaxArray, meshSize)
    f.write(preambString)
    f.write(ib.startSimu())
    f.write(ib.defineGeom(nDimensions))


i = 0
for index, part in df.iterrows(): # put each part in ibsimu, with positioning
   i = i + 1
   X,Y,Z = float(part['X'].split(' ')[0]),float(part['Y'].split(' ')[0]),float(part['Z'].split(' ')[0])
   Xrot, Yrot, Zrot = part['Xdeg'].split(' ')[0], part['Ydeg'].split(' ')[0], part['Zdeg'].split(' ')[0]
   Xrot, Yrot, Zrot = float(Xrot)*(pi/180), float(Yrot)*(pi/180), float(Zrot)*(pi/180)
   partName = part['partnames'].split('.')[0]
   with open(prefix + writeFile,'a+') as f:
       transformationString = ib.createTransformation(partName,i,X,Y,Z,Xrot,Yrot,Zrot)
       f.write(transformationString)

i = 0
if df['volts'].isnull().values.any(): #if volts column is empty
    a=1 # do nothing
else: # if volts column is populated, write IBSIMU code setting volts for each part
    with open(prefix + writeFile, 'a+') as f:
        f.write(ib.initialBoundaryConditions())
    for index, part in df.iterrows():
        i = i + 1
        partName = part['partnames'].split('.')[0]
        with open(prefix + writeFile,'a+') as f:
            bcString = ib.partBoundaryConditions(i,partName, part['volts'])
            f.write(bcString)


with open(prefix + writeFile,'a+') as f: # wrap up
    f.write(ib.buildMesh())
    pngString = ib.createPNG()
    f.write(pngString)
    f.write(ib.closeSimu())
    f.write(ib.createMain())

