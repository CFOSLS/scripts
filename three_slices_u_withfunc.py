import argparse
#### import the simple module from the paraview
from paraview.simple import *
import os.path

# parallel version
def draw_par(nprocs, input_fname, output_fname, iso_bot, iso_top, relative):
	print 'draw in three_slices_u_withfunc.py, parallel version'

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

	u_dataarr = []

	for procid in range (0, nprocs):
		input_fname_proc = input_fname_root + str(procid) + ".vtk"
		print(input_fname_proc)
		if not os.path.exists(input_fname_proc):
			print('procid = %d' % procid)
			sys.exit("File cannot be opened")
		u_data_proc = LegacyVTKReader(FileNames=[input_fname_proc])
		u_dataarr.append(u_data_proc)

	# set active source
	SetActiveSource(u_dataarr[0])

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [895, 810]

	# get color transfer function/color map for 'u_h'
	u_hLUT = GetColorTransferFunction('u_h')


	for procid in range (0, nprocs):
		#print(procid)

		# show data in view
		u_data_procDisplay = Show(u_dataarr[procid], renderView1)
		# trace defaults for the display properties.
		u_data_procDisplay.Representation = 'Surface'
		u_data_procDisplay.ColorArrayName = ['POINTS', 'u_h']
		u_data_procDisplay.LookupTable = u_hLUT
		u_data_procDisplay.OSPRayScaleArray = 'u_h'
		u_data_procDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
		u_data_procDisplay.SelectOrientationVectors = 'None'
		u_data_procDisplay.ScaleFactor = 0.2
		u_data_procDisplay.SelectScaleArray = 'u_h'
		u_data_procDisplay.GlyphType = 'Arrow'
		u_data_procDisplay.PolarAxes = 'PolarAxesRepresentation'
		u_data_procDisplay.ScalarOpacityUnitDistance = 0.3160479011877636
		u_data_procDisplay.GaussianRadius = 0.1
		u_data_procDisplay.SetScaleArray = ['POINTS', 'u_h']
		u_data_procDisplay.ScaleTransferFunction = 'PiecewiseFunction'
		u_data_procDisplay.OpacityArray = ['POINTS', 'u_h']
		u_data_procDisplay.OpacityTransferFunction = 'PiecewiseFunction'

		# reset view to fit data
		renderView1.ResetCamera()		

	# create a new 'Group Datasets'
	groupDatasets1 = GroupDatasets(Input=u_dataarr)

	# show data in view
	groupDatasets1Display = Show(groupDatasets1, renderView1)
	# trace defaults for the display properties.
	groupDatasets1Display.Representation = 'Surface'
	groupDatasets1Display.ColorArrayName = ['POINTS', 'u_h']
	groupDatasets1Display.LookupTable = u_hLUT
	groupDatasets1Display.OSPRayScaleArray = 'u_h'
	groupDatasets1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	groupDatasets1Display.SelectOrientationVectors = 'None'
	groupDatasets1Display.ScaleFactor = 0.2
	groupDatasets1Display.SelectScaleArray = 'u_h'
	groupDatasets1Display.GlyphType = 'Arrow'
	groupDatasets1Display.PolarAxes = 'PolarAxesRepresentation'
	groupDatasets1Display.ScalarOpacityUnitDistance = 0.23829607324923416
	groupDatasets1Display.GaussianRadius = 0.1
	groupDatasets1Display.SetScaleArray = ['POINTS', 'u_h']
	groupDatasets1Display.ScaleTransferFunction = 'PiecewiseFunction'
	groupDatasets1Display.OpacityArray = ['POINTS', 'u_h']
	groupDatasets1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# show color bar/color legend
	groupDatasets1Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(groupDatasets1)

	# show data in view
	groupDatasets1Display = Show(groupDatasets1, renderView1)

	for procid in range (0, nprocs):
		Hide(u_dataarr[procid], renderView1)

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(u_hLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	groupDatasets1Display.RescaleTransferFunctionToDataRange(True, False)

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# get color transfer function/color map for 'u_h'
	u_hLUT = GetColorTransferFunction('u_h')

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=groupDatasets1)
	isoVolume1.InputScalars = ['POINTS', 'u_h']
	isoVolume1.ThresholdRange = [-0.0031424, 0.0308287]

	# Properties modified on isoVolume1
	isoVolume1.ThresholdRange = [0.013163728000000003, 0.0308287]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)
	# trace defaults for the display properties.
	isoVolume1Display.Representation = 'Surface'
	isoVolume1Display.ColorArrayName = ['POINTS', 'u_h']
	isoVolume1Display.LookupTable = u_hLUT
	isoVolume1Display.OSPRayScaleArray = 'u_h'
	isoVolume1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	isoVolume1Display.SelectOrientationVectors = 'None'
	isoVolume1Display.ScaleFactor = 0.2
	isoVolume1Display.SelectScaleArray = 'u_h'
	isoVolume1Display.GlyphType = 'Arrow'
	isoVolume1Display.PolarAxes = 'PolarAxesRepresentation'
	isoVolume1Display.ScalarOpacityUnitDistance = 0.471876117335155
	isoVolume1Display.GaussianRadius = 0.1
	isoVolume1Display.SetScaleArray = ['POINTS', 'u_h']
	isoVolume1Display.ScaleTransferFunction = 'PiecewiseFunction'
	isoVolume1Display.OpacityArray = ['POINTS', 'u_h']
	isoVolume1Display.OpacityTransferFunction = 'PiecewiseFunction'

	smallest_arr = []
	largest_arr = []
	for procid in range (0, nprocs):

		auto_data = servermanager.Fetch(u_dataarr[procid])
		#print(auto_data.GetPointData().GetNumberOfArrays())
		#print(auto_data.GetPointData().GetArrayName(0))

		smallest_arr.append(auto_data.GetPointData().GetArray('u_h').GetRange()[0])
		largest_arr.append(auto_data.GetPointData().GetArray('u_h').GetRange()[1])

		
	smallest = min(smallest_arr)
	largest = max(largest_arr)
	
	if relative == True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# create a new 'Slice'
	slice1 = Slice(Input=groupDatasets1)
	slice1.SliceType = 'Plane'
	slice1.SliceOffsetValues = [0.0]

	# init the 'Plane' selected for 'SliceType'
	slice1.SliceType.Origin = [0.0, 0.0, 0.01]
	slice1.SliceType.Normal = [0.0, 0.0, 1.0]

	# Properties modified on slice1
	slice1.Triangulatetheslice = 0

	# show data in view
	slice1Display = Show(slice1, renderView1)
	# trace defaults for the display properties.
	slice1Display.Representation = 'Surface'
	slice1Display.ColorArrayName = ['POINTS', 'u_h']
	slice1Display.LookupTable = u_hLUT
	slice1Display.OSPRayScaleArray = 'u_h'
	slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice1Display.SelectOrientationVectors = 'None'
	slice1Display.ScaleFactor = 0.2
	slice1Display.SelectScaleArray = 'u_h'
	slice1Display.GlyphType = 'Arrow'
	slice1Display.PolarAxes = 'PolarAxesRepresentation'
	slice1Display.GaussianRadius = 0.1
	slice1Display.SetScaleArray = ['POINTS', 'u_h']
	slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice1Display.OpacityArray = ['POINTS', 'u_h']
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
	slice2.SliceType.Origin = [0.0, 0.0, 1.0]
	slice2.SliceType.Normal = [0.0, 0.0, 1.0]

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice2.SliceType)

	# Properties modified on slice2
	slice2.Triangulatetheslice = 0

	# show data in view
	slice2Display = Show(slice2, renderView1)
	# trace defaults for the display properties.
	slice2Display.Representation = 'Surface'
	slice2Display.ColorArrayName = ['POINTS', 'u_h']
	slice2Display.LookupTable = u_hLUT
	slice2Display.OSPRayScaleArray = 'u_h'
	slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice2Display.SelectOrientationVectors = 'None'
	slice2Display.ScaleFactor = 0.2
	slice2Display.SelectScaleArray = 'u_h'
	slice2Display.GlyphType = 'Arrow'
	slice2Display.PolarAxes = 'PolarAxesRepresentation'
	slice2Display.GaussianRadius = 0.1
	slice2Display.SetScaleArray = ['POINTS', 'u_h']
	slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice2Display.OpacityArray = ['POINTS', 'u_h']
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
	slice3.SliceType.Origin = [0.0, 0.0, 2.0]
	slice3.SliceType.Normal = [0.0, 0.0, 1.0]

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice3.SliceType)

	# Properties modified on slice3
	slice3.Triangulatetheslice = 0

	# show data in view
	slice3Display = Show(slice3, renderView1)
	# trace defaults for the display properties.
	slice3Display.Representation = 'Surface'
	slice3Display.ColorArrayName = ['POINTS', 'u_h']
	slice3Display.LookupTable = u_hLUT
	slice3Display.OSPRayScaleArray = 'u_h'
	slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice3Display.SelectOrientationVectors = 'None'
	slice3Display.ScaleFactor = 0.2
	slice3Display.SelectScaleArray = 'u_h'
	slice3Display.GlyphType = 'Arrow'
	slice3Display.PolarAxes = 'PolarAxesRepresentation'
	slice3Display.GaussianRadius = 0.1
	slice3Display.SetScaleArray = ['POINTS', 'u_h']
	slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice3Display.OpacityArray = ['POINTS', 'u_h']
	slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# show color bar/color legend
	slice3Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice3Display.SetRepresentationType('Surface With Edges')

	# set active source
	SetActiveSource(groupDatasets1)

	# current camera placement for renderView1
	renderView1.CameraPosition = [5.63, 1.68, 4.204]
	renderView1.CameraFocalPoint = [0.0, 0.0, 1.0]
	renderView1.CameraViewUp = [-0.462, -0.126, 0.878]
	renderView1.CameraParallelScale = 1.7320508075688772
	renderView1.CameraViewAngle = 30.00

	# save screenshot
	SaveScreenshot(output_filename, magnification=1, quality=100, view=renderView1)

def draw(input_fname, output_fname, iso_bot, iso_top, relative):
	print 'draw in three_slices_u_withfunc.py'

	if len(output_fname) == 0:
		#print("No output filename was provided as an input!")
		output_filename = ".".join(input_fname.split(".")[:-1]) + ".png"
	else:
		output_filename = output_fname

	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# create a new 'Legacy VTK Reader'
	u_test_it0vtk = LegacyVTKReader(FileNames=[input_fname])

	# set active source
	SetActiveSource(u_test_it0vtk)

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [895, 810]

	# get color transfer function/color map for 'u_h'
	u_hLUT = GetColorTransferFunction('u_h')

	# show data in view
	u_test_it0vtkDisplay = Show(u_test_it0vtk, renderView1)
	# trace defaults for the display properties.
	u_test_it0vtkDisplay.Representation = 'Surface'
	u_test_it0vtkDisplay.ColorArrayName = ['POINTS', 'u_h']
	u_test_it0vtkDisplay.LookupTable = u_hLUT
	u_test_it0vtkDisplay.OSPRayScaleArray = 'u_h'
	u_test_it0vtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
	u_test_it0vtkDisplay.SelectOrientationVectors = 'None'
	u_test_it0vtkDisplay.ScaleFactor = 0.2
	u_test_it0vtkDisplay.SelectScaleArray = 'u_h'
	u_test_it0vtkDisplay.GlyphType = 'Arrow'
	u_test_it0vtkDisplay.PolarAxes = 'PolarAxesRepresentation'
	u_test_it0vtkDisplay.ScalarOpacityUnitDistance = 0.23829607324923416
	u_test_it0vtkDisplay.GaussianRadius = 0.1
	u_test_it0vtkDisplay.SetScaleArray = ['POINTS', 'u_h']
	u_test_it0vtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
	u_test_it0vtkDisplay.OpacityArray = ['POINTS', 'u_h']
	u_test_it0vtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'

	# show color bar/color legend
	u_test_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# reset view to fit data
	renderView1.ResetCamera()

	# show data in view
	u_test_it0vtkDisplay = Show(u_test_it0vtk, renderView1)

	# reset view to fit data
	renderView1.ResetCamera()

	# show color bar/color legend
	u_test_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# Rescale transfer function
	u_hLUT.RescaleTransferFunction(-0.00314239, 0.0308278)

	# get opacity transfer function/opacity map for 'u_h'
	u_hPWF = GetOpacityTransferFunction('u_h')

	# Rescale transfer function
	u_hPWF.RescaleTransferFunction(-0.00314239, 0.0308278)

	# create a new 'Slice'
	slice1 = Slice(Input=u_test_it0vtk)
	slice1.SliceType = 'Plane'
	slice1.SliceOffsetValues = [0.0]

	# init the 'Plane' selected for 'SliceType'
	slice1.SliceType.Origin = [0.0, 0.0, 1.0]

	# Properties modified on slice1.SliceType
	slice1.SliceType.Origin = [0.0, 0.0, 0.01]
	slice1.SliceType.Normal = [0.0, 0.0, 1.0]

	# Properties modified on slice1
	slice1.Triangulatetheslice = 0

	# Properties modified on slice1.SliceType
	slice1.SliceType.Origin = [0.0, 0.0, 0.01]
	slice1.SliceType.Normal = [0.0, 0.0, 1.0]

	# show data in view
	slice1Display = Show(slice1, renderView1)
	# trace defaults for the display properties.
	slice1Display.Representation = 'Surface'
	slice1Display.ColorArrayName = ['POINTS', 'u_h']
	slice1Display.LookupTable = u_hLUT
	slice1Display.OSPRayScaleArray = 'u_h'
	slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice1Display.SelectOrientationVectors = 'None'
	slice1Display.ScaleFactor = 0.2
	slice1Display.SelectScaleArray = 'u_h'
	slice1Display.GlyphType = 'Arrow'
	slice1Display.PolarAxes = 'PolarAxesRepresentation'
	slice1Display.GaussianRadius = 0.1
	slice1Display.SetScaleArray = ['POINTS', 'u_h']
	slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice1Display.OpacityArray = ['POINTS', 'u_h']
	slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(u_test_it0vtk, renderView1)

	# show color bar/color legend
	slice1Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice1Display.SetRepresentationType('Surface With Edges')

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice1.SliceType)

	# set active source
	SetActiveSource(u_test_it0vtk)

	# create a new 'Slice'
	slice2 = Slice(Input=u_test_it0vtk)
	slice2.SliceType = 'Plane'
	slice2.SliceOffsetValues = [0.0]

	# init the 'Plane' selected for 'SliceType'
	slice2.SliceType.Origin = [0.0, 0.0, 1.0]

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
	slice2Display.ColorArrayName = ['POINTS', 'u_h']
	slice2Display.LookupTable = u_hLUT
	slice2Display.OSPRayScaleArray = 'u_h'
	slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice2Display.SelectOrientationVectors = 'None'
	slice2Display.ScaleFactor = 0.2
	slice2Display.SelectScaleArray = 'u_h'
	slice2Display.GlyphType = 'Arrow'
	slice2Display.PolarAxes = 'PolarAxesRepresentation'
	slice2Display.GaussianRadius = 0.1
	slice2Display.SetScaleArray = ['POINTS', 'u_h']
	slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice2Display.OpacityArray = ['POINTS', 'u_h']
	slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(u_test_it0vtk, renderView1)

	# show color bar/color legend
	slice2Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice2Display.SetRepresentationType('Surface With Edges')

	# set active source
	SetActiveSource(u_test_it0vtk)

	# create a new 'Slice'
	slice3 = Slice(Input=u_test_it0vtk)
	slice3.SliceType = 'Plane'
	slice3.SliceOffsetValues = [0.0]

	# init the 'Plane' selected for 'SliceType'
	slice3.SliceType.Origin = [0.0, 0.0, 1.0]

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice3.SliceType)

	# Properties modified on slice3.SliceType
	slice3.SliceType.Origin = [0.0, 0.0, 2.0]
	slice3.SliceType.Normal = [0.0, 0.0, 1.0]

	# Properties modified on slice3
	slice3.Triangulatetheslice = 0

	# Properties modified on slice3.SliceType
	slice3.SliceType.Origin = [0.0, 0.0, 2.0]
	slice3.SliceType.Normal = [0.0, 0.0, 1.0]

	# show data in view
	slice3Display = Show(slice3, renderView1)
	# trace defaults for the display properties.
	slice3Display.Representation = 'Surface'
	slice3Display.ColorArrayName = ['POINTS', 'u_h']
	slice3Display.LookupTable = u_hLUT
	slice3Display.OSPRayScaleArray = 'u_h'
	slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice3Display.SelectOrientationVectors = 'None'
	slice3Display.ScaleFactor = 0.2
	slice3Display.SelectScaleArray = 'u_h'
	slice3Display.GlyphType = 'Arrow'
	slice3Display.PolarAxes = 'PolarAxesRepresentation'
	slice3Display.GaussianRadius = 0.1
	slice3Display.SetScaleArray = ['POINTS', 'u_h']
	slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice3Display.OpacityArray = ['POINTS', 'u_h']
	slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(u_test_it0vtk, renderView1)

	# show color bar/color legend
	slice3Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice3Display.SetRepresentationType('Surface With Edges')

	# set active source
	SetActiveSource(u_test_it0vtk)

	# change representation type
	u_test_it0vtkDisplay.SetRepresentationType('Outline')

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# set active source
	SetActiveSource(u_test_it0vtk)

	# show data in view
	u_test_it0vtkDisplay = Show(u_test_it0vtk, renderView1)

	# show color bar/color legend
	u_test_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=u_test_it0vtk)
	isoVolume1.InputScalars = ['POINTS', 'u_h']
	isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)
	# trace defaults for the display properties.
	isoVolume1Display.Representation = 'Surface'
	isoVolume1Display.ColorArrayName = ['POINTS', 'u_h']
	isoVolume1Display.LookupTable = u_hLUT
	isoVolume1Display.OSPRayScaleArray = 'u_h'
	isoVolume1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	isoVolume1Display.SelectOrientationVectors = 'None'
	isoVolume1Display.ScaleFactor = 0.2
	isoVolume1Display.SelectScaleArray = 'u_h'
	isoVolume1Display.GlyphType = 'Arrow'
	isoVolume1Display.PolarAxes = 'PolarAxesRepresentation'
	isoVolume1Display.ScalarOpacityUnitDistance = 0.4193304265375669
	isoVolume1Display.GaussianRadius = 0.1
	isoVolume1Display.SetScaleArray = ['POINTS', 'u_h']
	isoVolume1Display.ScaleTransferFunction = 'PiecewiseFunction'
	isoVolume1Display.OpacityArray = ['POINTS', 'u_h']
	isoVolume1Display.OpacityTransferFunction = 'PiecewiseFunction'

	SetActiveSource(isoVolume1)

	its_data = servermanager.Fetch(u_test_it0vtk)
	print(its_data.GetPointData().GetNumberOfArrays())
	print(its_data.GetPointData().GetArrayName(0))

	smallest = its_data.GetPointData().GetArray('u_h').GetRange()[0]
	largest = its_data.GetPointData().GetArray('u_h').GetRange()[1]
	
	if relative == True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		isoVolume1.ThresholdRange = [iso_bot, iso_top]


	# set active source
	SetActiveSource(u_test_it0vtk)

	# show color bar/color legend
	isoVolume1Display.SetScalarBarVisibility(renderView1, True)

	# Rescale transfer function
	u_hLUT.RescaleTransferFunction(-0.00314239, 0.0308278)

	# Rescale transfer function
	u_hPWF.RescaleTransferFunction(-0.00314239, 0.0308278)

	#### saving camera placements for all active views

	# current camera placement for renderView1
	renderView1.CameraPosition = [5.63, 1.68, 4.204]
	renderView1.CameraFocalPoint = [0.0, 0.0, 1.0]
	renderView1.CameraViewUp = [-0.462, -0.126, 0.878]
	renderView1.CameraParallelScale = 1.7320508075688772
	renderView1.CameraViewAngle = 30.00

	# save screenshot
	SaveScreenshot(output_filename, magnification=1, quality=100, view=renderView1)

	#### uncomment the following to render all views
	# RenderAllViews()
	# alternatively, if you want to write images, you can use SaveScreenshot(...).

if __name__ == '__main__':
	# test1.py executed as script
	# do something
	# Parsing the script input arguments
	parser = argparse.ArgumentParser(description='Processing VTK output from MFEM for visualization via ParaView.')

	parser.add_argument('input_filename', type=str, help='input filename')

	parser.add_argument('-o','--out', dest='output_filename', type=str,
		           help='output filename', default="")

	parser.add_argument('-bot','--iso-bot', dest='iso_bot', type=float,
		           help='lowest margin for the iso volume', default=0)

	parser.add_argument('-top','--iso-top', dest='iso_top', type=float,
		           help='highest margin for the iso volume', default=10000)

	parser.add_argument('-rel','--iso-relative', dest='relative', 
		           help='Flag to treat iso-volume bounds as relative to data range if true, or not otherwise.', default=False, action='store_true')

	args = parser.parse_args()

	draw(args.input_filename, args.output_filename, args.iso_bot, args.iso_top, args.relative)


