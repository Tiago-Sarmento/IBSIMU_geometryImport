def startPreamble(minMaxArray,meshsize):
    libraryArray = ['<cstdlib>','<sstream>','<fstream>','<iomanip>','"epot_gssolver.hpp"','"epot_solver.hpp"','"epot_bicgstabsolver.hpp"','"epot_mgsolver.hpp"','"particledatabase.hpp"','"geometry.hpp"','"convergence.hpp"','"func_solid.hpp"','"epot_efield.hpp"','"meshvectorfield.hpp"','"meshvectorfield.hpp"','"ibsimu.hpp"','"error.hpp"','"particlediagplotter.hpp"','"gtkplotter.hpp"','"geomplotter.hpp"','"random.hpp"','"readascii.hpp"','"stl_solid.hpp"','"stlfile.hpp"','<math.h>']
    libstring = ''
    for library in libraryArray:
        libstring = libstring + '# include ' + library + '\n'
    stdString = 'using namespace std;\n'
    variables = ['xMin', 'xMax', 'yMin', 'yMax', 'zMin', 'zMax']
    initString = '\n\n'
    for i in range(0,len(minMaxArray)):
        initString = initString + 'double ' + variables[i] + ' = ' + str(minMaxArray[i]) + ';\n'

    meshString = 'double theMesh = ' + str(meshsize) + ';\n\n'
    return libstring + stdString + initString + meshString

def startSimu():
    defineSimu = 'void simu(int argc, char **argv )	{\n\n\t'
    return defineSimu

def closeSimu():
    return '\n}\n'

def defineGeom(nDimensions):

    geomString =  'double sizeX = xMax - xMin;\n\t' + \
    'double sizeY = yMax - yMin;\n\t' + \
	'double sizeZ = zMax - zMin;\n\t' + \
    'int pointsX = round(sizeX / theMesh) + 1;\n\t' + \
    'int pointsY = round(sizeY / theMesh) + 1;\n\t' + \
    'int pointsZ = round(sizeZ / theMesh) + 1; //number of mesh points in each plane == 1 for 2D sims\n\t'
    if nDimensions == 2:
        geometryLine = 'Geometry geom(MODE_2D, Int3D(pointsX,pointsY, 1), Vec3D(xMin,yMin,0), theMesh);//define a 2D E-field problem. Dimensions of B-field and particle tracker also need to be defined\n\n\t'
    elif nDimensions == 3:
        geometryLine = 'Geometry geom(MODE_3D, Int3D(pointsX,pointsY, pointsZ), Vec3D(xMin,yMin,zMin), theMesh);//define a 3D E-field problem. Dimensions of B-field and particle tracker also need to be defined\n\n\t'

    return geomString + geometryLine


def createTranslationVector(partName, x,y,z):
    partName = partName.replace('-', '_')
    string = 'Vec3D ' + partName + 'Translation(' + x + ', ' + y + ', ' + z + ');\n\t'
    return string

def createRotation(partName, xrot,yrot,zrot):
    partName = partName.replace('-', '_')
    string = 'Vec3D ' + partName + 'Translation(' + x + ', ' + y + ', ' + z + ');'
    return string



def createTransformation(partName, solidNumber, x, y, z, xrot, yrot, zrot):
    varName = partName.replace('-','_')
    scale = 1/1000 # STL files typically in mm
    T = 'T' + varName
    Solid = 'geom_' + varName

    defineTransformation = 'Transformation T' + partName + ';\n\t'
    rotationX = T + '.rotate_x(' + str(xrot) + ');\n\t'
    rotationY = T + '.rotate_y(' + str(yrot) + ');\n\t'
    rotationZ = T + '.rotate_z(' + str(zrot) + ');\n\t'
    scaler = T + '.scale(' + 'Vec3D(' + str(scale) + ', ' + str(scale) + ', ' + str(scale) + '));// STL files in mm\n\t'
    scale = 1 / 1000
    translation = T + '.translate(' + 'Vec3D(' + str(x*scale) + ', ' + str(y*scale) + ', ' + str(z*scale) + '));\n\t'
    importSTL = 'STLFile *f_' + varName + ' = new STLFile("parts/'+ partName +'.stl");\n\t'
    defineSolid = 'STLSolid *' + Solid + ' = new STLSolid;\n\t'
    setTransformation = Solid + '->set_transformation(' + T + ');\n\t'
    addFile = Solid + '->add_stl_file(f_' + partName + ');\n\t'
    setInGeom = 'geom.set_solid(' + str(solidNumber+6) + ', ' + Solid + ');\n\t\n\t\n\t'
    return defineTransformation + rotationX + rotationY + rotationZ + scaler + translation + importSTL + defineSolid + setTransformation + addFile + setInGeom

def initialBoundaryConditions():
    bcString = ''
    for i in range(1,7):
        bcString = bcString + 'geom.set_boundary( '+ str(i)+ ', Bound(BOUND_NEUMANN,    0.0 ) );\n\t'
    return bcString

def partBoundaryConditions(solidNumber, partName, volts):
    bcString = 'geom.set_boundary( ' + str(solidNumber+6) +', Bound(BOUND_DIRICHLET,  ' + str(volts) + ') ); // ' + partName + '\n\t'
    return bcString

def buildMesh():
    return 'geom.build_mesh();\n\t'

def createPNG():
    pngString = '\n\t\n\tGeomPlotter pregeomplotter( geom );\n\t' +\
                'pregeomplotter.set_mesh(true);\n\t'+\
                'pregeomplotter.set_size( 4*1024, 2*768 );\n\t' +\
                'pregeomplotter.set_font_size( 20 );\n\t' +\
                'pregeomplotter.set_view_si( VIEW_XY, 0 ); \n\t'+\
                'pregeomplotter.plot_png( "XYview.png" );\n\t' +\
                'pregeomplotter.set_view_si( VIEW_XZ, 0 ); \n\t' +\
                'pregeomplotter.plot_png( "XZview.png" );\n\t' +\
                'pregeomplotter.set_view_si( VIEW_YZ, 0 ); \n\t' +\
                'pregeomplotter.plot_png( "YZview.png" );\n\t\n\t'
    return pngString

def createMain():
    mainString = "int main( int argc, char **argv )			//main executable function call\n\
{ \n\t\
    try\n\t\
    {\n\t\t\
	    ibsimu.set_message_threshold( MSG_VERBOSE, 1 );\n\t\t\
    	ibsimu.set_thread_count( 4 );\n\t\t\
	    simu( argc, argv );				//run the simulation\n\t\
    }\n\t\
    catch( Error e )\n\t\
    {\n\t\t\
        e.print_error_message( cout );		//catch and report any errors\n\t\t\
        exit( 1 );\n\t\
    }\n\t\
    return( 0 );\n\
}"
    return mainString