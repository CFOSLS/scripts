import grfun_sliceprint
import mesh_sliceprint
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

# calls drawing script for data output from ComputeSlices()
# obtained from MFEM's extension with CFOSLS
# by calls like
'''
           // gridfunction slices
           ComputeSlices (*grfun, t0, ntsteps, tstep, myid, nprocs, forvideo, filename_root)
 
           // mesh slices
           ComputeSlices (*pmesh, t0, ntsteps, tstep, myid, nprocs, filename_root);
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
		           help='type: 0(mesh) or 1(grid function)', required=True,
			   default=0)

	parser.add_argument('-bot','--iso-bot', dest='iso_bot', type=float,
		           help='lowest margin for the iso volume', default=0)

	parser.add_argument('-top','--iso-top', dest='iso_top', type=float,
		           help='highest margin for the iso volume', default=10000)

	parser.add_argument('-rel','--iso-relative', dest='relative', 
		           help='Flag to treat iso-volume bounds as relative to data range (if active) or as absolute values (default).', default=False, action='store_true')

	parser.add_argument('-slices','--with-slices', dest='with_slices', 
		           help='Flag to visualize with slices (default is a transparent volume instead).', default=False, action='store_true')

	parser.add_argument('-par','--parallel', dest='parallel',  
		           help='Flag to be used if the input comes from a group of parallel processes (changes the expected input filename(s) format). Switched off by default. ', default=False, action='store_true')

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
					mesh_sliceprint.draw(filename,"", args.with_slices)
				else:
					#sequential version for sigma
					grfun_sliceprint.draw(filename,"", args.iso_bot, args.iso_top, args.relative, args.with_slices)
			else:
				sys.exit("File cannot be opened")
		# if input comes from a parallel run
		else:
			# for parallel version we actually need a filename root
			fileroot = args.filename_root + str(i) + '_proc_'

			if args.type == 0:
				#parallel version for u
				mesh_sliceprint.draw_par(args.nprocs,
				fileroot,"", args.with_slices)
			else:
				#parallel version for sigma
				grfun_sliceprint.draw_par(args.nprocs,
				fileroot,"",args.iso_bot, args.iso_top, args.relative, args.with_slices)

		# otherwise python actually doesn't get rid of the previous iteration correctly (i.e. next pictures somehow are influenced by the previous ones which is wrong)			
		ResetSession()
	

