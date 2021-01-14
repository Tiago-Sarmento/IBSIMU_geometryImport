# IBSIMU Geometry Import

Python scripts to easily import geometry into IBSIMU particle tracking simulations

These scripts were originally written so an assembly in solid edge could be easily imported into IBSIMU.

## Basic usage:


(From solid edge)
Save assembly as translated, as separate STL files in mm under 'options...' 

Select relevant assembly parts and right click to get occurence properties

Copy and paste the columns up to ZRot into the second row of the positioning.csv file in this repo

If you have electric potentials to add to each part, populate the voltage column in Volts but without writing units in the csv file. Note: all rows must have a value unless all are empty

Open and run renderSTL.py

Use any CAD software top open the newly created combinedObject.stl and verify the positioning. It should match your assembly in solid edge

renderSTL.py prints an array [xmin,xmax,ymin,ymax,zmin,zmax] to be copied and pasted into makeIBSIMU.py

Run makeIBSIMU.py

Use a text editor to open the newly created IBSIMU_GeomtryImport.cpp 

Run this with IBSIMU, and verify the newly created png files to check geometry is imported correctly.


## Troubleshooting

Positioning in combinedObject.stl is incorrect:

Check values in positioning.csv. Note that a solid edge assembly containining subassemblies will export values relative to each respective subassembly's coordinate system. 

To fix this, move all the parts to the same assembly, also referred to as 'flattening' the assembly.


If alignment appears ok but separation distances are unusual, verify that STL file was exported in mm. Alternatively, put a scaling factor in renderSTL.py and translateToIBSIMU.py



