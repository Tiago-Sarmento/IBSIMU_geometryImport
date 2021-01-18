# include <cstdlib>
# include <sstream>
# include <fstream>
# include <iomanip>
# include "epot_gssolver.hpp"
# include "epot_solver.hpp"
# include "epot_bicgstabsolver.hpp"
# include "epot_mgsolver.hpp"
# include "particledatabase.hpp"
# include "geometry.hpp"
# include "convergence.hpp"
# include "func_solid.hpp"
# include "epot_efield.hpp"
# include "meshvectorfield.hpp"
# include "meshvectorfield.hpp"
# include "ibsimu.hpp"
# include "error.hpp"
# include "particlediagplotter.hpp"
# include "gtkplotter.hpp"
# include "geomplotter.hpp"
# include "random.hpp"
# include "readascii.hpp"
# include "stl_solid.hpp"
# include "stlfile.hpp"
# include <math.h>
using namespace std;


double xMin = -0.075;
double xMax = 0.093;
double yMin = -0.01;
double yMax = 0.01;
double zMin = -0.08;
double zMax = 0.09;
double theMesh = 0.001;

void simu(int argc, char **argv )	{

	double sizeX = xMax - xMin;
	double sizeY = yMax - yMin;
	double sizeZ = zMax - zMin;
	int pointsX = round(sizeX / theMesh) + 1;
	int pointsY = round(sizeY / theMesh) + 1;
	int pointsZ = round(sizeZ / theMesh) + 1; //number of mesh points in each plane == 1 for 2D sims
	Geometry geom(MODE_3D, Int3D(pointsX,pointsY, pointsZ), Vec3D(xMin,yMin,zMin), theMesh);//define a 3D E-field problem. Dimensions of B-field and particle tracker also need to be defined

	Transformation TBase_1_A;
	TBase_1_A.rotate_x(-1.570796326795);
	TBase_1_A.rotate_y(0.0);
	TBase_1_A.rotate_z(-1.570796326795);
	TBase_1_A.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TBase_1_A.translate(Vec3D(-0.25, 0.0, 0.010060000000000001));
	STLFile *f_Base_1_A = new STLFile("parts/Base 1-A.stl");
	STLSolid *geom_Base_1_A = new STLSolid;
	geom_Base_1_A->set_transformation(TBase_1_A);
	geom_Base_1_A->add_stl_file(f_Base_1_A);
	geom.set_solid(7, geom_Base_1_A);
	
	
	Transformation TBase_1_A;
	TBase_1_A.rotate_x(-1.570796326795);
	TBase_1_A.rotate_y(-3.14159265359);
	TBase_1_A.rotate_z(0.0);
	TBase_1_A.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TBase_1_A.translate(Vec3D(0.0, -0.25, 0.010060000000000001));
	STLFile *f_Base_1_A = new STLFile("parts/Base 1-A.stl");
	STLSolid *geom_Base_1_A = new STLSolid;
	geom_Base_1_A->set_transformation(TBase_1_A);
	geom_Base_1_A->add_stl_file(f_Base_1_A);
	geom.set_solid(8, geom_Base_1_A);
	
	
	Transformation TMiddle_pole;
	TMiddle_pole.rotate_x(0.0);
	TMiddle_pole.rotate_y(3.14159265359);
	TMiddle_pole.rotate_z(0.0);
	TMiddle_pole.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TMiddle_pole.translate(Vec3D(0.0, 0.0, 0.52006));
	STLFile *f_Middle_pole = new STLFile("parts/Middle pole.stl");
	STLSolid *geom_Middle_pole = new STLSolid;
	geom_Middle_pole->set_transformation(TMiddle_pole);
	geom_Middle_pole->add_stl_file(f_Middle_pole);
	geom.set_solid(9, geom_Middle_pole);
	
	
	Transformation TUpper_plate_1;
	TUpper_plate_1.rotate_x(3.14159265359);
	TUpper_plate_1.rotate_y(0.0);
	TUpper_plate_1.rotate_z(-1.0471975511966667);
	TUpper_plate_1.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TUpper_plate_1.translate(Vec3D(-1e-05, 4e-05, 1.03065));
	STLFile *f_Upper_plate_1 = new STLFile("parts/Upper plate 1.stl");
	STLSolid *geom_Upper_plate_1 = new STLSolid;
	geom_Upper_plate_1->set_transformation(TUpper_plate_1);
	geom_Upper_plate_1->add_stl_file(f_Upper_plate_1);
	geom.set_solid(10, geom_Upper_plate_1);
	
	
	Transformation TPin_A;
	TPin_A.rotate_x(0.0);
	TPin_A.rotate_y(0.0);
	TPin_A.rotate_z(-1.9444713196470105);
	TPin_A.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TPin_A.translate(Vec3D(0.016050000000000002, -0.20777, 1.03006));
	STLFile *f_Pin_A = new STLFile("parts/Pin A.stl");
	STLSolid *geom_Pin_A = new STLSolid;
	geom_Pin_A->set_transformation(TPin_A);
	geom_Pin_A->add_stl_file(f_Pin_A);
	geom.set_solid(11, geom_Pin_A);
	
	
	Transformation TPin_A;
	TPin_A.rotate_x(0.0);
	TPin_A.rotate_y(0.0);
	TPin_A.rotate_z(-1.9500563732533929);
	TPin_A.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TPin_A.translate(Vec3D(-0.016059999999999998, -0.20777, 1.03006));
	STLFile *f_Pin_A = new STLFile("parts/Pin A.stl");
	STLSolid *geom_Pin_A = new STLSolid;
	geom_Pin_A->set_transformation(TPin_A);
	geom_Pin_A->add_stl_file(f_Pin_A);
	geom.set_solid(12, geom_Pin_A);
	
	
	Transformation TPin_A;
	TPin_A.rotate_x(0.0);
	TPin_A.rotate_y(0.0);
	TPin_A.rotate_z(-2.3513075682869156);
	TPin_A.scale(Vec3D(0.001, 0.001, 0.001));// STL files in mm
	TPin_A.translate(Vec3D(-0.17195, -0.11777, 1.03006));
	STLFile *f_Pin_A = new STLFile("parts/Pin A.stl");
	STLSolid *geom_Pin_A = new STLSolid;
	geom_Pin_A->set_transformation(TPin_A);
	geom_Pin_A->add_stl_file(f_Pin_A);
	geom.set_solid(13, geom_Pin_A);
	
	
	geom.set_boundary( 1, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 2, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 3, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 4, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 5, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 6, Bound(BOUND_NEUMANN,    0.0 ) );
	geom.set_boundary( 7, Bound(BOUND_DIRICHLET,  200) ); // Base 1-A
	geom.set_boundary( 8, Bound(BOUND_DIRICHLET,  300) ); // Base 1-A
	geom.set_boundary( 9, Bound(BOUND_DIRICHLET,  400) ); // Middle pole
	geom.set_boundary( 10, Bound(BOUND_DIRICHLET,  500) ); // Upper plate 1
	geom.set_boundary( 11, Bound(BOUND_DIRICHLET,  600) ); // Pin A
	geom.set_boundary( 12, Bound(BOUND_DIRICHLET,  700) ); // Pin A
	geom.set_boundary( 13, Bound(BOUND_DIRICHLET,  800) ); // Pin A
	geom.build_mesh();
	
	
	GeomPlotter pregeomplotter( geom );
	pregeomplotter.set_mesh(true);
	pregeomplotter.set_size( 4*1024, 2*768 );
	pregeomplotter.set_font_size( 20 );
	pregeomplotter.set_view_si( VIEW_XY, 0 ); 
	pregeomplotter.plot_png( "XYview.png" );
	pregeomplotter.set_view_si( VIEW_XZ, 0 ); 
	pregeomplotter.plot_png( "XZview.png" );
	pregeomplotter.set_view_si( VIEW_YZ, 0 ); 
	pregeomplotter.plot_png( "YZview.png" );
	
	
}
int main( int argc, char **argv )			//main executable function call
{ 
	    try
	    {
			    ibsimu.set_message_threshold( MSG_VERBOSE, 1 );
		    	ibsimu.set_thread_count( 4 );
			    simu( argc, argv );				//run the simulation
	    }
	    catch( Error e )
	    {
		        e.print_error_message( cout );		//catch and report any errors
		        exit( 1 );
	    }
	    return( 0 );
}