import three_slices_sigma_withfunc
import three_slices_u_withfunc
import argparse
import os.path
import sys
from paraview.simple import *

def ResetSession():
    pxm = servermanager.ProxyManager()
    pxm.UnRegisterProxies()
    del pxm
    Disconnect()
    Connect()

# calls drawing script for scalar(u) or vector(sigma) data
# obtained from MFEM's extension example cfosls_hyperbolic_adref_hcurl_new.cpp
# by calls like
'''
           std::string field_name_sigma("sigma_h");
           sigma->SaveVTK(fp_sigma, field_name_sigma, ref);

           //std::ofstream fp_S("u_test_it0.vtk");
           std::string filename_S;
           filename_S = "u_it_";
           filename_S.append(std::to_string(it));
           if (num_procs > 1)
           {
               filename_S.append("_proc_");
               filename_S.append(std::to_string(myid));
           }
           filename_S.append(".vtk");
           std::ofstream fp_S(filename_S);

           pmesh->PrintVTK(fp_S, ref, true);
           //pmesh->PrintVTK(fp_S);

           std::string field_name_S("u_h");
           S->SaveVTK(fp_S, field_name_S, ref);

'''
# names 'sigma_h' and 'u_h' are for now required (but you can modify the script to provide them as an additional parameter)
# the current script is to be run by pvpython with parameters from the command line
# typical filename_root is:
# 1) sigma_it_N.vtk for serial run output
# 2) sigma_it_ for parallel output, with actual files in the form sigma_it_N_proc_M.vtk where
# N is the iteration number, M is the number of processes
if __name__ == '__main__':
	# Parsing the script input arguments
	parser = argparse.ArgumentParser(description='Processing multiple VTK outputs from MFEM for visualization via ParaView.')

	parser.add_argument('filename_root', type=str, help='filename root (for input)')

	parser.add_argument('-o','--out', dest='output_filename', type=str,
		           help='output filename', default="")

	parser.add_argument('-st','--step', dest='step', type=int,
		           help='step for the pictures', default="1")

	parser.add_argument('-stcnt','--start-count', dest='start_count', type=int,
		           help='starting count', default="0")

	parser.add_argument('-nst','--nsteps', dest='nsteps', type=int,
		           help='nsteps', default="1")

	parser.add_argument('-t','--type', dest='type', type=int,
		           help='type: 0(scalar) or 1(vector)', required=True,
			   default=0)

	parser.add_argument('-bot','--iso-bot', dest='iso_bot', type=float,
		           help='lowest margin for the iso volume', default=0)

	parser.add_argument('-top','--iso-top', dest='iso_top', type=float,
		           help='highest margin for the iso volume', default=10000)

	parser.add_argument('-rel','--iso-relative', dest='relative', type=bool,
		           help='Flag to treat iso-volume bounds as relative to data range if true, or as absolute values otherwise.', default=False)

	parser.add_argument('-par','--parallel', dest='parallel', type=bool,
		           help='Flag to define whether the input is from a group of parallel processes.', default=False)

	parser.add_argument('-np','--nprocs', dest='nprocs', type=int,
		           help='Number of processes.', default=1)

	args = parser.parse_args()

	for i in xrange(args.start_count, args.start_count + args.nsteps*args.step, args.step):
		# if input comes from a sequential run
		if args.parallel == False:
			filename = args.filename_root + str(i) + '.vtk'
			print(filename)
			if os.path.exists(filename):
				if args.type == 0:
					#sequential version for u
					three_slices_u_withfunc.draw(filename,"",
					args.iso_bot, args.iso_top, args.relative)
				else:
					#sequential version for sigma
					three_slices_sigma_withfunc.draw(filename,"", 					args.iso_bot, args.iso_top, args.relative)
			else:
				sys.exit("File cannot be opened")
		# if input comes from a parallel run
		else:
			# for parallel version we actually need a filename root
			fileroot = args.filename_root + str(i) + '_proc_'

			if args.type == 0:
				#parallel version for u
				three_slices_u_withfunc.draw_par(args.nprocs,
				fileroot,"", args.iso_bot, args.iso_top,
				args.relative)
			else:
				#parallel version for sigma
				three_slices_sigma_withfunc.draw_par(args.nprocs,
				fileroot,"",args.iso_bot, args.iso_top, 				args.relative)

		# otherwise python actually doesn't get rid of the previous iteration correctly (i.e. next pictures somehow are influenced by the previous ones which is wrong)			
		ResetSession()
	

