# scripts
Visualization scrips which can be used to create a series of pictures in ParaView, e.g., coming from AMR setup.  
The scripts are designed to work for vector or scalar data in \*.vtk format which have been produced by 
CFOSLS/mfem visualization routines. 

Examples can be found, for instance, in https://github.com/CFOSLS/mfem/examples/cfosls_hyperbolic_adref_Hcurl_new.cpp with
output_solution = true, which produces the correct input data for paraview_draw.py. Or, by https://github.com/CFOSLS/mfem/examples/cfosls_hyperbolic.cpp which produces correct input for paraview_draw_sliceprint.py.

Two main scripts:
1) paraview_draw.py (it's components are three_slices_sigma_withfunc.py and three_slices_u_withfunc.py)
This script can be used to visualize 3D data produced from SaveVTK() and PrintVTK() routines from MFEM.
2) paraview_draw_sliceprint.py (it's components are mesh_sliceprint.py and grfun_sliceprint.py)
This script can be used to visualize 3D data produced from ComputeSlices() from CFOSLS MFEM which produce 3D slices of 4D mesh and grid function slices.
Scripts work with output from either serial or parallel runs.
Main body of the scripts was produced by automatically created python traces in ParaView (thus, not optimal).

Prerequisites: ParaView (with a shell), version 5.3.0 (at least the scripts worked for this version), Python 2.7

Example runs:
1) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py $(SOME_DIR)/filename_root_ --type 1 --step 5 --nsteps 3
--iso-bot 0.1 --iso-top 1.0 --iso-relative 
(having files SOMEDIR/filename_root_0.vtk, SOMEDIR/filename_root_5.vtk and SOMEDIR/filename_root_10.vtk produced by serial runs)

2) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py $(SOME_DIR)/filename_root_ --type 1 --step 5 --nsteps 3 
--iso-bot 0.1 --iso-top 1.0 --iso-relative --parallel --nprocs 4
(if the output has format SOMEDIR/filename_root_N_proc_M.vtk)

3) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw_sliceprint.py $(SOME_DIR)/filename_root_ --type 0 --step 5 --nsteps 3
(having files SOMEDIR/filename_root_0.vtk, SOMEDIR/filename_root_5.vtk and SOMEDIR/filename_root_10.vtk produced by serial runs)
Notice: type 0 is for sliced meshes produced by ComputeSlices() for a Mesh object. Then, no isovolume is created.

4) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw_sliceprint.py $(SOME_DIR)/filename_root_ --type 1 --step 5 --nsteps 3 
--iso-bot 0.1 --iso-top 1.0 --iso-relative --parallel --nprocs 4 --with-slices 
(if the output has format SOMEDIR/filename_root_N_proc_M.vtk)
Notice: type 1 is for slices of grid functions produced by ComputeSlices() for a GridFunction object.

To look at all possible input options:
./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py --help
or
./pvpython $(PATH_TO_SCRIPTS)/paraview_draw_sliceprint.py --help

