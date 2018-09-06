import argparse
#### import the simple module from the paraview
from paraview.simple import *
import os.path

# parallel version
def draw_par(nprocs, input_fname, output_fname, iso_bot, iso_top, relative, with_slices):
	print 'draw in grfun_sliceprint.py, parallel version'

	input_fname_root = "_".join(input_fname.split("_")[:-1]) + "_"
	print(input_fname_root)

	if len(output_fname) == 0:
		#print("No output filename was provided as an input!")
		output_filename = input_fname_root + ".png"
		output_filename = "_proc_".join(input_fname_root.split("_proc_")[:-1]) + ".png"
	else:
		output_filename = output_fname

	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	grfun_dataarr = []

	for procid in range (0, nprocs):
		input_fname_proc = input_fname_root + str(procid) + ".vtk"
		print(input_fname_proc)
		if not os.path.exists(input_fname_proc):
			print('procid = %d' % procid)
			sys.exit("File cannot be opened")
		grfun_data_proc = LegacyVTKReader(FileNames=[input_fname_proc])
		grfun_dataarr.append(grfun_data_proc)

	# set active source
	SetActiveSource(grfun_dataarr[0])

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [895, 810]

	# get color transfer function/color map for 'cell_scalars'
	grfun_LUT = GetColorTransferFunction('cell_scalars')

	for procid in range (0, nprocs):
		#print(procid)

		# show data in view
		grfun_data_procDisplay = Show(grfun_dataarr[procid], renderView1)
		# trace defaults for the display properties.
		grfun_data_procDisplay.Representation = 'Surface'
		grfun_data_procDisplay.ColorArrayName = ['POINTS', 'cell_scalars']
		grfun_data_procDisplay.LookupTable = grfun_LUT
		grfun_data_procDisplay.OSPRayScaleArray = 'cell_scalars'
		grfun_data_procDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
		grfun_data_procDisplay.SelectOrientationVectors = 'None'
		grfun_data_procDisplay.ScaleFactor = 0.2
		grfun_data_procDisplay.SelectScaleArray = 'cell_scalars'
		grfun_data_procDisplay.GlyphType = 'Arrow'
		grfun_data_procDisplay.PolarAxes = 'PolarAxesRepresentation'
		grfun_data_procDisplay.ScalarOpacityUnitDistance = 0.3160479011877636
		grfun_data_procDisplay.GaussianRadius = 0.1
		grfun_data_procDisplay.SetScaleArray = ['POINTS', 'cell_scalars']
		grfun_data_procDisplay.ScaleTransferFunction = 'PiecewiseFunction'
		grfun_data_procDisplay.OpacityArray = ['POINTS', 'cell_scalars']
		grfun_data_procDisplay.OpacityTransferFunction = 'PiecewiseFunction'

		# reset view to fit data
		renderView1.ResetCamera()		

	# create a new 'Group Datasets'
	groupDatasets1 = GroupDatasets(Input=grfun_dataarr)

	# show data in view
	groupDatasets1Display = Show(groupDatasets1, renderView1)
	# trace defaults for the display properties.
	groupDatasets1Display.Representation = 'Surface'
	groupDatasets1Display.ColorArrayName = ['POINTS', 'cell_scalars']
	groupDatasets1Display.LookupTable = grfun_LUT
	groupDatasets1Display.OSPRayScaleArray = 'cell_scalars'
	groupDatasets1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	groupDatasets1Display.SelectOrientationVectors = 'None'
	groupDatasets1Display.ScaleFactor = 0.2
	groupDatasets1Display.SelectScaleArray = 'cell_scalars'
	groupDatasets1Display.GlyphType = 'Arrow'
	groupDatasets1Display.PolarAxes = 'PolarAxesRepresentation'
	groupDatasets1Display.ScalarOpacityUnitDistance = 0.23829607324923416
	groupDatasets1Display.GaussianRadius = 0.1
	groupDatasets1Display.SetScaleArray = ['POINTS', 'cell_scalars']
	groupDatasets1Display.ScaleTransferFunction = 'PiecewiseFunction'
	groupDatasets1Display.OpacityArray = ['POINTS', 'cell_scalars']
	groupDatasets1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# show color bar/color legend
	groupDatasets1Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(groupDatasets1)

	# show data in view
	groupDatasets1Display = Show(groupDatasets1, renderView1)

	for procid in range (0, nprocs):
		Hide(grfun_dataarr[procid], renderView1)

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(grfun_LUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	#groupDatasets1Display.RescaleTransferFunctionToDataRange(True, False)

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# current camera placement for renderView1
	renderView1.CameraPosition = [1.429153224460805, -5.992468570970181, 2.6138957855611755]
	renderView1.CameraViewUp = [-0.0920643033105146, 0.3795899568888681, 0.9205626696130237]
	renderView1.CameraParallelScale = 1.7320508075688772

	# get color transfer function/color map for 'cell_scalars'
	grfun_LUT = GetColorTransferFunction('cell_scalars')

	# hide data in view
	#Hide(groupDatasets1, renderView1)

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=groupDatasets1)
	isoVolume1.InputScalars = ['POINTS', 'cell_scalars']
	isoVolume1.ThresholdRange = [-0.0031424, 0.0308287]

	# Properties modified on isoVolume1
	isoVolume1.ThresholdRange = [0.013163728000000003, 0.0308287]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)
	# trace defaults for the display properties.
	isoVolume1Display.Representation = 'Surface'
	isoVolume1Display.ColorArrayName = ['POINTS', 'cell_scalars']
	isoVolume1Display.LookupTable = grfun_LUT
	isoVolume1Display.OSPRayScaleArray = 'cell_scalars'
	isoVolume1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	isoVolume1Display.SelectOrientationVectors = 'None'
	isoVolume1Display.ScaleFactor = 0.2
	isoVolume1Display.SelectScaleArray = 'cell_scalars'
	isoVolume1Display.GlyphType = 'Arrow'
	isoVolume1Display.PolarAxes = 'PolarAxesRepresentation'
	isoVolume1Display.ScalarOpacityUnitDistance = 0.471876117335155
	isoVolume1Display.GaussianRadius = 0.1
	isoVolume1Display.SetScaleArray = ['POINTS', 'cell_scalars']
	isoVolume1Display.ScaleTransferFunction = 'PiecewiseFunction'
	isoVolume1Display.OpacityArray = ['POINTS', 'cell_scalars']
	isoVolume1Display.OpacityTransferFunction = 'PiecewiseFunction'

	smallest_arr = []
	largest_arr = []
	for procid in range (0, nprocs):

		auto_data = servermanager.Fetch(grfun_dataarr[procid])
		#print(auto_data.GetPointData().GetNumberOfArrays())
		#print(auto_data.GetPointData().GetArrayName(0))
		#print(auto_data.GetCellData().GetNumberOfArrays())
		#print(auto_data.GetCellData().GetArrayName(0))

		smallest_arr.append(auto_data.GetCellData().GetArray('cell_scalars').GetRange()[0])
		largest_arr.append(auto_data.GetCellData().GetArray('cell_scalars').GetRange()[1])
		
	smallest = min(smallest_arr)
	largest = max(largest_arr)
	
	#print(smallest)
	#print(largest)

	if relative == True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		#print(iso_bot)
		#print(iso_top)
		isoVolume1.ThresholdRange = [iso_bot, iso_top]
	
	# set active source
	SetActiveSource(groupDatasets1)

	if with_slices == True:
		# create a new 'Slice'
		slice1 = Slice(Input=groupDatasets1)
		slice1.SliceType = 'Plane'
		slice1.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice1.SliceType.Origin = [0.0, 0.0, -0.99]
		slice1.SliceType.Normal = [0.0, 0.0, 1.0]

		# Properties modified on slice1
		slice1.Triangulatetheslice = 0

		# show data in view
		slice1Display = Show(slice1, renderView1)
		# trace defaults for the display properties.
		slice1Display.Representation = 'Surface'
		slice1Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice1Display.LookupTable = grfun_LUT
		slice1Display.OSPRayScaleArray = 'cell_scalars'
		slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice1Display.SelectOrientationVectors = 'None'
		slice1Display.ScaleFactor = 0.2
		slice1Display.SelectScaleArray = 'cell_scalars'
		slice1Display.GlyphType = 'Arrow'
		slice1Display.PolarAxes = 'PolarAxesRepresentation'
		slice1Display.GaussianRadius = 0.1
		slice1Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice1Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(groupDatasets1, renderView1)

		# show color bar/color legend
		slice1Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice1Display.SetRepresentationType('Surface With Edges')

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice1.SliceType)

		# set active source
		SetActiveSource(groupDatasets1)

		# create a new 'Slice'
		slice2 = Slice(Input=groupDatasets1)
		slice2.SliceType = 'Plane'
		slice2.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice2.SliceType.Origin = [0.0, 0.0, 0.0]
		slice2.SliceType.Normal = [0.0, 0.0, 1.0]

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice2.SliceType)

		# Properties modified on slice2
		slice2.Triangulatetheslice = 0

		# show data in view
		slice2Display = Show(slice2, renderView1)
		# trace defaults for the display properties.
		slice2Display.Representation = 'Surface'
		slice2Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice2Display.LookupTable = grfun_LUT
		slice2Display.OSPRayScaleArray = 'cell_scalars'
		slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice2Display.SelectOrientationVectors = 'None'
		slice2Display.ScaleFactor = 0.2
		slice2Display.SelectScaleArray = 'cell_scalars'
		slice2Display.GlyphType = 'Arrow'
		slice2Display.PolarAxes = 'PolarAxesRepresentation'
		slice2Display.GaussianRadius = 0.1
		slice2Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice2Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(groupDatasets1, renderView1)

		# show color bar/color legend
		slice2Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice2Display.SetRepresentationType('Surface With Edges')

		# set active source
		SetActiveSource(groupDatasets1)

		# create a new 'Slice'
		slice3 = Slice(Input=groupDatasets1)
		slice3.SliceType = 'Plane'
		slice3.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice3.SliceType.Origin = [0.0, 0.0, 1.0]
		slice3.SliceType.Normal = [0.0, 0.0, 1.0]

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice3.SliceType)

		# Properties modified on slice3
		slice3.Triangulatetheslice = 0

		# show data in view
		slice3Display = Show(slice3, renderView1)
		# trace defaults for the display properties.
		slice3Display.Representation = 'Surface'
		slice3Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice3Display.LookupTable = grfun_LUT
		slice3Display.OSPRayScaleArray = 'cell_scalars'
		slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice3Display.SelectOrientationVectors = 'None'
		slice3Display.ScaleFactor = 0.2
		slice3Display.SelectScaleArray = 'cell_scalars'
		slice3Display.GlyphType = 'Arrow'
		slice3Display.PolarAxes = 'PolarAxesRepresentation'
		slice3Display.GaussianRadius = 0.1
		slice3Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice3Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(groupDatasets1, renderView1)

		# show color bar/color legend
		slice3Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice3Display.SetRepresentationType('Surface With Edges')

		# set active source
		SetActiveSource(groupDatasets1)

		# change representation type
		groupDatasets1Display.SetRepresentationType('Outline')
	else:
		# set active source
		SetActiveSource(groupDatasets1)

		# change representation type
		groupDatasets1Display.SetRepresentationType('Surface With Edges')

		# Modifying opacity
		groupDatasets1Display.Opacity = 0.25

	# set active source
	SetActiveSource(groupDatasets1)

	# current camera placement for renderView1
	#renderView1.CameraPosition = [1.429153224460805, -5.992468570970181, 2.6138957855611755]
	#renderView1.CameraViewUp = [-0.0920643033105146, 0.3795899568888681, 0.9205626696130237]
	#renderView1.CameraParallelScale = 1.7320508075688772

	# save screenshot
	SaveScreenshot(output_filename, magnification=1, quality=100, view=renderView1)

def draw(input_fname, output_fname, iso_bot, iso_top, relative, with_slices):
	print 'draw in grfun_sliceprint.py'

	if len(output_fname) == 0:
		#print("No output filename was provided as an input!")
		output_filename = ".".join(input_fname.split(".")[:-1]) + ".png"
	else:
		output_filename = output_fname

	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# create a new 'Legacy VTK Reader'
	grfun_it0vtk = LegacyVTKReader(FileNames=[input_fname])

	# set active source
	SetActiveSource(grfun_it0vtk)

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [895, 810]

	# get color transfer function/color map for 'cell_scalars'
	grfun_LUT = GetColorTransferFunction('cell_scalars')

	# show data in view
	grfun_it0vtkDisplay = Show(grfun_it0vtk, renderView1)
	# trace defaults for the display properties.
	grfun_it0vtkDisplay.Representation = 'Surface'
	grfun_it0vtkDisplay.ColorArrayName = ['POINTS', 'cell_scalars']
	grfun_it0vtkDisplay.LookupTable = grfun_LUT
	grfun_it0vtkDisplay.OSPRayScaleArray = 'cell_scalars'
	grfun_it0vtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
	grfun_it0vtkDisplay.SelectOrientationVectors = 'None'
	grfun_it0vtkDisplay.ScaleFactor = 0.2
	grfun_it0vtkDisplay.SelectScaleArray = 'cell_scalars'
	grfun_it0vtkDisplay.GlyphType = 'Arrow'
	grfun_it0vtkDisplay.PolarAxes = 'PolarAxesRepresentation'
	grfun_it0vtkDisplay.ScalarOpacityUnitDistance = 0.23829607324923416
	grfun_it0vtkDisplay.GaussianRadius = 0.1
	grfun_it0vtkDisplay.SetScaleArray = ['POINTS', 'cell_scalars']
	grfun_it0vtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
	grfun_it0vtkDisplay.OpacityArray = ['POINTS', 'cell_scalars']
	grfun_it0vtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# show color bar/color legend
	#grfun_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(grfun_it0vtk)

	# show data in view
	grfun_it0vtkDisplay = Show(grfun_it0vtk, renderView1)

	# get color transfer function/color map for 'cell_scalars'
	grfun_LUT = GetColorTransferFunction('cell_scalars')

	# Rescale transfer function
	grfun_LUT.RescaleTransferFunction(-0.00314239, 0.0308278)

	#### saving camera placements for all active views

	# current camera placement for renderView1
	renderView1.CameraPosition = [1.429153224460805, -5.992468570970181, 2.6138957855611755]
	renderView1.CameraViewUp = [-0.0920643033105146, 0.3795899568888681, 0.9205626696130237]
	renderView1.CameraParallelScale = 1.7320508075688772

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=grfun_it0vtk)
	isoVolume1.InputScalars = ['POINTS', 'cell_scalars']
	isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)
	# trace defaults for the display properties.
	isoVolume1Display.Representation = 'Surface'
	isoVolume1Display.ColorArrayName = ['POINTS', 'cell_scalars']
	isoVolume1Display.LookupTable = grfun_LUT
	isoVolume1Display.OSPRayScaleArray = 'cell_scalars'
	isoVolume1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	isoVolume1Display.SelectOrientationVectors = 'None'
	isoVolume1Display.ScaleFactor = 0.2
	isoVolume1Display.SelectScaleArray = 'cell_scalars'
	isoVolume1Display.GlyphType = 'Arrow'
	isoVolume1Display.PolarAxes = 'PolarAxesRepresentation'
	isoVolume1Display.ScalarOpacityUnitDistance = 0.4193304265375669
	isoVolume1Display.GaussianRadius = 0.1
	isoVolume1Display.SetScaleArray = ['POINTS', 'cell_scalars']
	isoVolume1Display.ScaleTransferFunction = 'PiecewiseFunction'
	isoVolume1Display.OpacityArray = ['POINTS', 'cell_scalars']
	isoVolume1Display.OpacityTransferFunction = 'PiecewiseFunction'

	its_data = servermanager.Fetch(grfun_it0vtk)
	print(its_data.GetCellData().GetNumberOfArrays())
	print(its_data.GetCellData().GetArrayName(0))

	smallest = its_data.GetCellData().GetArray('cell_scalars').GetRange()[0]
	largest = its_data.GetCellData().GetArray('cell_scalars').GetRange()[1]
	
	if relative == True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# set active source
	SetActiveSource(grfun_it0vtk)

	if with_slices == True:
		# create a new 'Slice'
		slice1 = Slice(Input=grfun_it0vtk)
		slice1.SliceType = 'Plane'
		slice1.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice1.SliceType.Origin = [0.0, 0.0, -1.0]

		# Properties modified on slice1.SliceType
		slice1.SliceType.Origin = [0.0, 0.0, -0.99]
		slice1.SliceType.Normal = [0.0, 0.0, 1.0]

		# Properties modified on slice1
		slice1.Triangulatetheslice = 0

		# Properties modified on slice1.SliceType
		slice1.SliceType.Origin = [0.0, 0.0, -0.99]
		slice1.SliceType.Normal = [0.0, 0.0, 1.0]

		# show data in view
		slice1Display = Show(slice1, renderView1)
		# trace defaults for the display properties.
		slice1Display.Representation = 'Surface'
		slice1Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice1Display.LookupTable = grfun_LUT
		slice1Display.OSPRayScaleArray = 'cell_scalars'
		slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice1Display.SelectOrientationVectors = 'None'
		slice1Display.ScaleFactor = 0.2
		slice1Display.SelectScaleArray = 'cell_scalars'
		slice1Display.GlyphType = 'Arrow'
		slice1Display.PolarAxes = 'PolarAxesRepresentation'
		slice1Display.GaussianRadius = 0.1
		slice1Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice1Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(grfun_it0vtk, renderView1)

		# show color bar/color legend
		slice1Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice1Display.SetRepresentationType('Surface With Edges')

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice1.SliceType)

		# set active source
		SetActiveSource(grfun_it0vtk)

		# create a new 'Slice'
		slice2 = Slice(Input=grfun_it0vtk)
		slice2.SliceType = 'Plane'
		slice2.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice2.SliceType.Origin = [0.0, 0.0, 0.0]

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice2.SliceType)

		# Properties modified on slice2.SliceType
		slice2.SliceType.Normal = [0.0, 0.0, 1.0]

		# Properties modified on slice2
		slice2.Triangulatetheslice = 0

		# Properties modified on slice2.SliceType
		slice2.SliceType.Normal = [0.0, 0.0, 1.0]

		# show data in view
		slice2Display = Show(slice2, renderView1)
		# trace defaults for the display properties.
		slice2Display.Representation = 'Surface'
		slice2Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice2Display.LookupTable = grfun_LUT
		slice2Display.OSPRayScaleArray = 'cell_scalars'
		slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice2Display.SelectOrientationVectors = 'None'
		slice2Display.ScaleFactor = 0.2
		slice2Display.SelectScaleArray = 'cell_scalars'
		slice2Display.GlyphType = 'Arrow'
		slice2Display.PolarAxes = 'PolarAxesRepresentation'
		slice2Display.GaussianRadius = 0.1
		slice2Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice2Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(grfun_it0vtk, renderView1)

		# show color bar/color legend
		slice2Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice2Display.SetRepresentationType('Surface With Edges')

		# set active source
		SetActiveSource(grfun_it0vtk)

		# create a new 'Slice'
		slice3 = Slice(Input=grfun_it0vtk)
		slice3.SliceType = 'Plane'
		slice3.SliceOffsetValues = [0.0]

		# init the 'Plane' selected for 'SliceType'
		slice3.SliceType.Origin = [0.0, 0.0, 1.0]

		# toggle 3D widget visibility (only when running from the GUI)
		Hide3DWidgets(proxy=slice3.SliceType)

		# Properties modified on slice3.SliceType
		slice3.SliceType.Origin = [0.0, 0.0, 1.0]
		slice3.SliceType.Normal = [0.0, 0.0, 1.0]

		# Properties modified on slice3
		slice3.Triangulatetheslice = 0

		# Properties modified on slice3.SliceType
		slice3.SliceType.Origin = [0.0, 0.0, 1.0]
		slice3.SliceType.Normal = [0.0, 0.0, 1.0]

		# show data in view
		slice3Display = Show(slice3, renderView1)
		# trace defaults for the display properties.
		slice3Display.Representation = 'Surface'
		slice3Display.ColorArrayName = ['POINTS', 'cell_scalars']
		slice3Display.LookupTable = grfun_LUT
		slice3Display.OSPRayScaleArray = 'cell_scalars'
		slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
		slice3Display.SelectOrientationVectors = 'None'
		slice3Display.ScaleFactor = 0.2
		slice3Display.SelectScaleArray = 'cell_scalars'
		slice3Display.GlyphType = 'Arrow'
		slice3Display.PolarAxes = 'PolarAxesRepresentation'
		slice3Display.GaussianRadius = 0.1
		slice3Display.SetScaleArray = ['POINTS', 'cell_scalars']
		slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
		slice3Display.OpacityArray = ['POINTS', 'cell_scalars']
		slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

		# hide data in view
		Hide(grfun_it0vtk, renderView1)

		# show color bar/color legend
		slice3Display.SetScalarBarVisibility(renderView1, True)

		# change representation type
		slice3Display.SetRepresentationType('Surface With Edges')

		# set active source
		SetActiveSource(grfun_it0vtk)

		# change representation type
		grfun_it0vtkDisplay.SetRepresentationType('Outline')

	else:
		# set active source
		SetActiveSource(grfun_it0vtk)

		# change representation type
		grfun_it0vtkDisplay.SetRepresentationType('Surface With Edges')

		# Modifying opacity
		grfun_it0vtkDisplay.Opacity = 0.25

	# set active source
	SetActiveSource(grfun_it0vtk)

	# save screenshot
	SaveScreenshot(output_filename, magnification=1, quality=100, view=renderView1)

	#### uncomment the following to render all views
	# RenderAllViews()
	# alternatively, if you want to write images, you can use SaveScreenshot(...).

if __name__ == '__main__':
	# Parsing the script input arguments
	parser = argparse.ArgumentParser(description='Processing VTK output from sliced MFEM grid functions for visualization via ParaView.')

	parser.add_argument('input_filename', type=str, help='input filename')

	parser.add_argument('-o','--out', dest='output_filename', type=str,
		           help='output filename', default="")

	parser.add_argument('-bot','--iso-bot', dest='iso_bot', type=float,
		           help='lowest margin for the iso volume', default=0)

	parser.add_argument('-top','--iso-top', dest='iso_top', type=float,
		           help='highest margin for the iso volume', default=10000)

	parser.add_argument('-rel','--iso-relative', dest='relative', 
		           help='Flag to treat iso-volume bounds as relative to data range (if active) or as absolute values (default).', default=False, action='store_true')

	parser.add_argument('-slices','--with-slices', dest='with_slices', 
		           help='Flag to visualize with slices (default is a transparent volume instead).', default=False, action='store_true')

	args = parser.parse_args()

	draw(args.input_filename, args.output_filename, args.iso_bot, args.iso_top, args.relative, args.with_slices)


