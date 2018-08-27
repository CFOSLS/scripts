import argparse
#### import the simple module from the paraview
from paraview.simple import *
import os.path

# parallel version
def draw_par(nprocs, input_fname, output_fname, iso_bot, iso_top, relative):
	print 'draw in three_slices_sigma_withfunc.py, parallel version'

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

	sigma_dataarr = []

	for procid in range (0, nprocs):
		input_fname_proc = input_fname_root + str(procid) + ".vtk"
		print(input_fname_proc)
		if not os.path.exists(input_fname_proc):
			print('procid = %d' % procid)
			sys.exit("File cannot be opened")
		sigma_data_proc = LegacyVTKReader(FileNames=[input_fname_proc])
		sigma_dataarr.append(sigma_data_proc)

	# set active source
	SetActiveSource(sigma_dataarr[0])

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [895, 810]

	# get color transfer function/color map for 'material'
	materialLUT = GetColorTransferFunction('material')

	for procid in range (0, nprocs):
		print(procid)
		# show data in view
		sigma_data_proc_Display = Show(sigma_dataarr[procid], renderView1)
		# trace defaults for the display properties.
		sigma_data_proc_Display.Representation = 'Surface'
		sigma_data_proc_Display.ColorArrayName = ['CELLS', 'material']
		sigma_data_proc_Display.LookupTable = materialLUT
		sigma_data_proc_Display.OSPRayScaleArray = 'material'
		sigma_data_proc_Display.OSPRayScaleFunction = 'PiecewiseFunction'
		sigma_data_proc_Display.SelectOrientationVectors = 'sigma_h'
		sigma_data_proc_Display.ScaleFactor = 0.2
		sigma_data_proc_Display.SelectScaleArray = 'material'
		sigma_data_proc_Display.GlyphType = 'Arrow'
		sigma_data_proc_Display.PolarAxes = 'PolarAxesRepresentation'
		sigma_data_proc_Display.ScalarOpacityUnitDistance = 0.3210323936677311
		sigma_data_proc_Display.GaussianRadius = 0.1
		sigma_data_proc_Display.SetScaleArray = ['POINTS', 'material']
		sigma_data_proc_Display.ScaleTransferFunction = 'PiecewiseFunction'
		sigma_data_proc_Display.OpacityArray = ['POINTS', 'material']
		sigma_data_proc_Display.OpacityTransferFunction = 'PiecewiseFunction'

		# reset view to fit data
		renderView1.ResetCamera()		

	# create a new 'Group Datasets'
	groupDatasets1 = GroupDatasets(Input=sigma_dataarr)

	# show data in view
	groupDatasets1Display = Show(groupDatasets1, renderView1)
	# trace defaults for the display properties.
	groupDatasets1Display.Representation = 'Surface'
	groupDatasets1Display.ColorArrayName = ['CELLS', 'material']
	groupDatasets1Display.LookupTable = materialLUT
	groupDatasets1Display.OSPRayScaleArray = 'material'
	groupDatasets1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	groupDatasets1Display.SelectOrientationVectors = 'sigma_h'
	groupDatasets1Display.ScaleFactor = 0.2
	groupDatasets1Display.SelectScaleArray = 'material'
	groupDatasets1Display.GlyphType = 'Arrow'
	groupDatasets1Display.PolarAxes = 'PolarAxesRepresentation'
	groupDatasets1Display.ScalarOpacityUnitDistance = 0.23829607324923416
	groupDatasets1Display.GaussianRadius = 0.1
	groupDatasets1Display.SetScaleArray = ['POINTS', 'material']
	groupDatasets1Display.ScaleTransferFunction = 'PiecewiseFunction'
	groupDatasets1Display.OpacityArray = ['POINTS', 'material']
	groupDatasets1Display.OpacityTransferFunction = 'PiecewiseFunction'

	for procid in range (0, nprocs):
		Hide(sigma_dataarr[procid], renderView1)

	# show color bar/color legend
	groupDatasets1Display.SetScalarBarVisibility(renderView1, True)

	# set scalar coloring
	ColorBy(groupDatasets1Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	groupDatasets1Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	groupDatasets1Display.SetScalarBarVisibility(renderView1, True)

	# get color transfer function/color map for 'sigma_h'
	sigma_hLUT = GetColorTransferFunction('sigma_h')

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=groupDatasets1)
	isoVolume1.InputScalars = ['POINTS', 'sigma_h_Magnitude']
	isoVolume1.ThresholdRange = [0.01799034365376233, 0.036714549203638605]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)
	# trace defaults for the display properties.
	isoVolume1Display.Representation = 'Surface'
	isoVolume1Display.ColorArrayName = ['CELLS', 'material']
	isoVolume1Display.LookupTable = materialLUT
	isoVolume1Display.OSPRayScaleArray = 'material'
	isoVolume1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	isoVolume1Display.SelectOrientationVectors = 'sigma_h'
	isoVolume1Display.ScaleFactor = 0.2
	isoVolume1Display.SelectScaleArray = 'material'
	isoVolume1Display.GlyphType = 'Arrow'
	isoVolume1Display.PolarAxes = 'PolarAxesRepresentation'
	isoVolume1Display.ScalarOpacityUnitDistance = 0.5277265674729354
	isoVolume1Display.GaussianRadius = 0.1
	isoVolume1Display.SetScaleArray = ['POINTS', 'material']
	isoVolume1Display.ScaleTransferFunction = 'PiecewiseFunction'
	isoVolume1Display.OpacityArray = ['POINTS', 'material']
	isoVolume1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# show color bar/color legend
	#isoVolume1Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(groupDatasets1)

	# change representation type
	groupDatasets1Display.SetRepresentationType('Outline')

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# current camera placement for renderView1
	renderView1.CameraPosition = [5.63, 1.68, 4.204]
	renderView1.CameraFocalPoint = [0.0, 0.0, 1.0]
	renderView1.CameraViewUp = [-0.462, -0.126, 0.878]
	renderView1.CameraParallelScale = 1.7320508075688772
	renderView1.CameraViewAngle = 30.00

	isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [794, 699]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)

	# set active source
	SetActiveSource(isoVolume1)

	smallest_arr = []
	largest_arr = []
	for procid in range (0, nprocs):

		# create a new 'Calculator'
		calculator1 = Calculator(Input=sigma_dataarr[procid])
		calculator1.Function = 'mag(sigma_h)'

		# Properties modified on calculator1
		calculator1.ResultArrayName = 'sigma_h_mag'

		# get active view
		renderView1 = GetActiveViewOrCreate('RenderView')

		# get color transfer function/color map for 'Result'
		resultLUT = GetColorTransferFunction('Result')

		# hide data in view
		Hide(calculator1, renderView1)

		auto_data = servermanager.Fetch(calculator1)
		#print(auto_data.GetPointData().GetNumberOfArrays())
		#print(auto_data.GetPointData().GetArrayName(0))

		smallest_arr.append(auto_data.GetPointData().GetArray('sigma_h_mag').GetRange()[0])
		largest_arr.append(auto_data.GetPointData().GetArray('sigma_h_mag').GetRange()[1])

		
	smallest = min(smallest_arr)
	largest = max(largest_arr)
	
	if relative == True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		print("new iso-volume bounds: %0.2f %0.2f \n" % (iso_bot, iso_top))
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
	slice1Display.ColorArrayName = ['CELLS', 'material']
	slice1Display.LookupTable = materialLUT
	slice1Display.OSPRayScaleArray = 'material'
	slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice1Display.SelectOrientationVectors = 'sigma_h'
	slice1Display.ScaleFactor = 0.2
	slice1Display.SelectScaleArray = 'material'
	slice1Display.GlyphType = 'Arrow'
	slice1Display.PolarAxes = 'PolarAxesRepresentation'
	slice1Display.GaussianRadius = 0.1
	slice1Display.SetScaleArray = ['POINTS', 'material']
	slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice1Display.OpacityArray = ['POINTS', 'material']
	slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# show color bar/color legend
	#slice1Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice1Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice1Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice1Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice1Display.SetScalarBarVisibility(renderView1, True)

	# get color transfer function/color map for 'sigma_h'
	sigma_hLUT = GetColorTransferFunction('sigma_h')

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

	# Properties modified on slice2
	slice2.Triangulatetheslice = 0

	# show data in view
	slice2Display = Show(slice2, renderView1)
	# trace defaults for the display properties.
	slice2Display.Representation = 'Surface'
	slice2Display.ColorArrayName = ['CELLS', 'material']
	slice2Display.LookupTable = materialLUT
	slice2Display.OSPRayScaleArray = 'material'
	slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice2Display.SelectOrientationVectors = 'sigma_h'
	slice2Display.ScaleFactor = 0.2
	slice2Display.SelectScaleArray = 'material'
	slice2Display.GlyphType = 'Arrow'
	slice2Display.PolarAxes = 'PolarAxesRepresentation'
	slice2Display.GaussianRadius = 0.1
	slice2Display.SetScaleArray = ['POINTS', 'material']
	slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice2Display.OpacityArray = ['POINTS', 'material']
	slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# show color bar/color legend
	#slice2Display.SetScalarBarVisibility(renderView1, True)

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice2.SliceType)

	# change representation type
	slice2Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice2Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice2Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice2Display.SetScalarBarVisibility(renderView1, True)

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
	slice3Display.ColorArrayName = ['CELLS', 'material']
	slice3Display.LookupTable = materialLUT
	slice3Display.OSPRayScaleArray = 'material'
	slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice3Display.SelectOrientationVectors = 'sigma_h'
	slice3Display.ScaleFactor = 0.2
	slice3Display.SelectScaleArray = 'material'
	slice3Display.GlyphType = 'Arrow'
	slice3Display.PolarAxes = 'PolarAxesRepresentation'
	slice3Display.GaussianRadius = 0.1
	slice3Display.SetScaleArray = ['POINTS', 'material']
	slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice3Display.OpacityArray = ['POINTS', 'material']
	slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(groupDatasets1, renderView1)

	# show color bar/color legend
	#slice3Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice3Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice3Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice3Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice3Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(groupDatasets1)

	print(output_filename)

	# save screenshot
	SaveScreenshot(output_filename, magnification=1, quality=100, view=renderView1)

# sequential version
def draw(input_fname, output_fname, iso_bot, iso_top, relative):
	print 'draw in three_slices_sigma_withfunc.py'

	if len(output_fname) == 0:
		#print("No output filename was provided as an input!")
		output_filename = ".".join(input_fname.split(".")[:-1]) + ".png"
	else:
		output_filename = output_fname

	#### disable automatic camera reset on 'Show'
	paraview.simple._DisableFirstRenderCameraReset()

	# create a new 'Legacy VTK Reader'
	sigma_test_it0vtk = LegacyVTKReader(FileNames=[input_fname])

	# set active source
	SetActiveSource(sigma_test_it0vtk)

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [794, 699]

	# get display properties
	sigma_test_it0vtkDisplay = GetDisplayProperties(sigma_test_it0vtk, view=renderView1)

	# change representation type
	sigma_test_it0vtkDisplay.SetRepresentationType('Outline')

	# Properties modified on renderView1.AxesGrid
	renderView1.AxesGrid.Visibility = 1

	# get color transfer function/color map for 'material'
	materialLUT = GetColorTransferFunction('material')

	# show data in view
	sigma_test_it0vtkDisplay = Show(sigma_test_it0vtk, renderView1)
	# trace defaults for the display properties.
	sigma_test_it0vtkDisplay.Representation = 'Surface'
	sigma_test_it0vtkDisplay.ColorArrayName = ['CELLS', 'material']
	sigma_test_it0vtkDisplay.LookupTable = materialLUT
	sigma_test_it0vtkDisplay.OSPRayScaleArray = 'material'
	sigma_test_it0vtkDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
	sigma_test_it0vtkDisplay.SelectOrientationVectors = 'sigma_h'
	sigma_test_it0vtkDisplay.ScaleFactor = 0.2
	sigma_test_it0vtkDisplay.SelectScaleArray = 'material'
	sigma_test_it0vtkDisplay.GlyphType = 'Arrow'
	sigma_test_it0vtkDisplay.PolarAxes = 'PolarAxesRepresentation'
	sigma_test_it0vtkDisplay.ScalarOpacityUnitDistance = 0.23829607324923416
	sigma_test_it0vtkDisplay.GaussianRadius = 0.1
	sigma_test_it0vtkDisplay.SetScaleArray = ['POINTS', 'material']
	sigma_test_it0vtkDisplay.ScaleTransferFunction = 'PiecewiseFunction'
	sigma_test_it0vtkDisplay.OpacityArray = ['POINTS', 'material']
	sigma_test_it0vtkDisplay.OpacityTransferFunction = 'PiecewiseFunction'

	# show color bar/color legend
	sigma_test_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# reset view to fit data
	renderView1.ResetCamera()

	# show data in view
	sigma_test_it0vtkDisplay = Show(sigma_test_it0vtk, renderView1)

	# reset view to fit data
	renderView1.ResetCamera()

	# show color bar/color legend
	sigma_test_it0vtkDisplay.SetScalarBarVisibility(renderView1, True)

	# create a new 'Slice'
	slice1 = Slice(Input=sigma_test_it0vtk)
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
	slice1Display.ColorArrayName = ['CELLS', 'material']
	slice1Display.LookupTable = materialLUT
	slice1Display.OSPRayScaleArray = 'material'
	slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice1Display.SelectOrientationVectors = 'sigma_h'
	slice1Display.ScaleFactor = 0.2
	slice1Display.SelectScaleArray = 'material'
	slice1Display.GlyphType = 'Arrow'
	slice1Display.PolarAxes = 'PolarAxesRepresentation'
	slice1Display.GaussianRadius = 0.1
	slice1Display.SetScaleArray = ['POINTS', 'material']
	slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice1Display.OpacityArray = ['POINTS', 'material']
	slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(sigma_test_it0vtk, renderView1)

	# show color bar/color legend
	slice1Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice1Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice1Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice1Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice1Display.SetScalarBarVisibility(renderView1, True)

	# get color transfer function/color map for 'sigma_h'
	sigma_hLUT = GetColorTransferFunction('sigma_h')

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice1.SliceType)

	# set active source
	SetActiveSource(sigma_test_it0vtk)

	# create a new 'Slice'
	slice2 = Slice(Input=sigma_test_it0vtk)
	slice2.SliceType = 'Plane'
	slice2.SliceOffsetValues = [0.0]

	# init the 'Plane' selected for 'SliceType'
	slice2.SliceType.Origin = [0.0, 0.0, 1.0]

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
	slice2Display.ColorArrayName = ['CELLS', 'material']
	slice2Display.LookupTable = materialLUT
	slice2Display.OSPRayScaleArray = 'material'
	slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice2Display.SelectOrientationVectors = 'sigma_h'
	slice2Display.ScaleFactor = 0.2
	slice2Display.SelectScaleArray = 'material'
	slice2Display.GlyphType = 'Arrow'
	slice2Display.PolarAxes = 'PolarAxesRepresentation'
	slice2Display.GaussianRadius = 0.1
	slice2Display.SetScaleArray = ['POINTS', 'material']
	slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice2Display.OpacityArray = ['POINTS', 'material']
	slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(sigma_test_it0vtk, renderView1)

	# show color bar/color legend
	slice2Display.SetScalarBarVisibility(renderView1, True)

	# toggle 3D widget visibility (only when running from the GUI)
	Hide3DWidgets(proxy=slice2.SliceType)

	# change representation type
	slice2Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice2Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice2Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice2Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(sigma_test_it0vtk)

	# create a new 'Slice'
	slice3 = Slice(Input=sigma_test_it0vtk)
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
	slice3Display.ColorArrayName = ['CELLS', 'material']
	slice3Display.LookupTable = materialLUT
	slice3Display.OSPRayScaleArray = 'material'
	slice3Display.OSPRayScaleFunction = 'PiecewiseFunction'
	slice3Display.SelectOrientationVectors = 'sigma_h'
	slice3Display.ScaleFactor = 0.2
	slice3Display.SelectScaleArray = 'material'
	slice3Display.GlyphType = 'Arrow'
	slice3Display.PolarAxes = 'PolarAxesRepresentation'
	slice3Display.GaussianRadius = 0.1
	slice3Display.SetScaleArray = ['POINTS', 'material']
	slice3Display.ScaleTransferFunction = 'PiecewiseFunction'
	slice3Display.OpacityArray = ['POINTS', 'material']
	slice3Display.OpacityTransferFunction = 'PiecewiseFunction'

	# hide data in view
	Hide(sigma_test_it0vtk, renderView1)

	# show color bar/color legend
	slice3Display.SetScalarBarVisibility(renderView1, True)

	# change representation type
	slice3Display.SetRepresentationType('Surface With Edges')

	# set scalar coloring
	ColorBy(slice3Display, ('POINTS', 'sigma_h', 'Magnitude'))

	# Hide the scalar bar for this color map if no visible data is colored by it.
	HideScalarBarIfNotNeeded(materialLUT, renderView1)

	# rescale color and/or opacity maps used to include current data range
	slice3Display.RescaleTransferFunctionToDataRange(True, False)

	# show color bar/color legend
	slice3Display.SetScalarBarVisibility(renderView1, True)

	# set active source
	SetActiveSource(sigma_test_it0vtk)

	#### saving camera placements for all active views

	# current camera placement for renderView1
	renderView1.CameraPosition = [5.63, 1.68, 4.204]
	renderView1.CameraFocalPoint = [0.0, 0.0, 1.0]
	renderView1.CameraViewUp = [-0.462, -0.126, 0.878]
	renderView1.CameraParallelScale = 1.7320508075688772
	renderView1.CameraViewAngle = 30.00

	

	# create a new 'Iso Volume'
	isoVolume1 = IsoVolume(Input=sigma_test_it0vtk)
	isoVolume1.InputScalars = ['POINTS', 'sigma_h_Magnitude']
	isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# get active view
	renderView1 = GetActiveViewOrCreate('RenderView')
	# uncomment following to set a specific view size
	# renderView1.ViewSize = [794, 699]

	# show data in view
	isoVolume1Display = Show(isoVolume1, renderView1)

	# set active source
	SetActiveSource(isoVolume1)

	its_data = servermanager.Fetch(sigma_test_it0vtk)
	#print(its_data.GetPointData().GetArray('sigma_h_Magnitude').GetRange().GetValue(0))
	print(its_data.GetPointData().GetNumberOfArrays())
	print(its_data.GetPointData().GetArrayName(1))

	smallest = its_data.GetPointData().GetArray('sigma_h_Magnitude').GetRange()[0]
	largest = its_data.GetPointData().GetArray('sigma_h_Magnitude').GetRange()[1]
	
	if relative ==True:
		print("Recomputing iso-volume using input args as relative (from 0.0 to 1.0) to the data range")
		iso_bot = smallest + (largest - smallest) * iso_bot
		iso_top = smallest + (largest - smallest) * iso_top
		print("new iso-volume bounds: %0.2f %0.2f \n" % (iso_bot, iso_top))
		isoVolume1.ThresholdRange = [iso_bot, iso_top]

	# set active source
	SetActiveSource(sigma_test_it0vtk)

	# get color transfer function/color map for 'sigma_h_Magnitude'
	sigma_h_MagnitudeLUT = GetColorTransferFunction('sigma_h_Magnitude')

	# set scalar coloring
	#ColorBy(isoVolume1Display, ('POINTS', 'sigma_h_Magnitude'))

	# get color transfer function/color map for 'element_coloring'
	#element_coloringLUT = GetColorTransferFunction('element_coloring')

	# Hide the scalar bar for this color map if no visible data is colored by it.
	#HideScalarBarIfNotNeeded(element_coloringLUT, renderView1)


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

	parser.add_argument('-rel','--iso-relative', dest='relative', type=bool,
		           help='Flag to treat iso-volume bounds as relative to data range if true, or not otherwise.', default=False)

	args = parser.parse_args()

	draw(args.input_filename, args.output_filename, args.iso_bot, args.iso_top, args.relative)


