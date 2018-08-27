# scripts
Visualization scrips which can be used to create a series of pictures in ParaView, e.g., coming from AMR setup.  
The scripts are designed to work for vector or scalar data in *.vtk format which have been produced by 
CFOSLS/mfem visualization routines. For example, look at CFOSLS/mfem/examples/cfosls_hyperbolic_adref_Hcurl_new.cpp with
output_solution = true, which produces the correct input data.

Prerequisites: ParaView (with a shell), version 5.3.0 (at least the scripts worked for this version), Python 2.7

Example runs:
1) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py $(SOME_DIR)/filename_root_it_ --type 1 --step 5 --nsteps 3
--iso-bot 0.1 --iso-top 1.0 --iso-relative True 
(having files SOMEDIR/filename_root_it_0.vtk, SOMEDIR/filename_root_it_5.vtk and SOMEDIR/filename_root_it_10.vtk produced by serial runs)

2) ./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py $(SOME_DIR)/filename_root_it_ --type 1 --step 5 --nsteps 3 
--iso-bot 0.1 --iso-top 1.0 --iso-relative True --parallel True --nprocs 4
(if the output has format SOMEDIR/filename_root_it_N_proc_M.vtk)

To look at all possible input options:
./pvpython $(PATH_TO_SCRIPTS)/paraview_draw.py --help

